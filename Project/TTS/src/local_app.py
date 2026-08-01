from __future__ import annotations

import argparse
import os
import threading
import time
import webbrowser
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field

from interactive_engines import (
    PROJECT_ROOT,
    STAGE_BY_ID,
    InteractiveEngines,
    cache_path,
    result_payload,
    stage_catalog,
    validate_text,
)


app = FastAPI(title="Seven Stages Local TTS", docs_url="/api/docs", redoc_url=None)
engines = InteractiveEngines()
generation_lock = threading.Lock()


class SynthesisRequest(BaseModel):
    stage: int = Field(ge=1, le=7)
    text: str = Field(min_length=1, max_length=500)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(PROJECT_ROOT / "listen.html")


@app.get("/api/stages")
def stages() -> dict[str, object]:
    readiness = engines.readiness()
    items = []
    for item in stage_catalog():
        item.update(readiness[int(item["stage"])])
        items.append(item)
    return {"stages": items, "all_ready": all(value["ready"] for value in readiness.values())}


@app.get("/api/health")
def health() -> dict[str, object]:
    readiness = engines.readiness()
    return {
        "ok": all(value["ready"] for value in readiness.values()),
        "stages": readiness,
        "busy": generation_lock.locked(),
    }


@app.post("/api/synthesize")
def synthesize(request: SynthesisRequest) -> dict[str, object]:
    try:
        text = validate_text(request.text)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    readiness = engines.readiness()[request.stage]
    if not readiness["ready"]:
        raise HTTPException(
            status_code=503,
            detail="此階段尚未安裝完成：" + ", ".join(readiness["missing"]),
        )

    output = cache_path(request.stage, text)
    if output.exists():
        return result_payload(request.stage, text, output, True, 0.0)

    started = time.perf_counter()
    with generation_lock:
        if output.exists():
            return result_payload(request.stage, text, output, True, time.perf_counter() - started)
        temporary = output.with_suffix(".partial.wav")
        try:
            temporary.parent.mkdir(parents=True, exist_ok=True)
            engines.synthesize(request.stage, text, temporary)
            os.replace(temporary, output)
        except Exception as error:
            temporary.unlink(missing_ok=True)
            raise HTTPException(status_code=500, detail=f"Stage {request.stage} 生成失敗：{error}") from error

    return result_payload(request.stage, text, output, False, time.perf_counter() - started)


@app.get("/audio/stage{stage}/{filename}")
def audio(stage: int, filename: str) -> FileResponse:
    if stage not in STAGE_BY_ID or not filename.endswith(".wav") or Path(filename).name != filename:
        raise HTTPException(status_code=404)
    path = PROJECT_ROOT / "output" / "interactive" / f"stage{stage}" / filename
    if not path.exists():
        raise HTTPException(status_code=404)
    return FileResponse(path, media_type="audio/wav", filename=f"stage{stage}_{filename}")


@app.get("/favicon.ico")
def favicon() -> Response:
    return Response(status_code=204)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    if not args.no_browser:
        threading.Timer(1.2, lambda: webbrowser.open(f"http://{args.host}:{args.port}")).start()
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
