# Stage 1 rule controls

`stage1_rule_frontend_frames.csv` contains the 10 ms acoustic-control frames
used for the fixed comparison sentence. The controls were generated from the
rsynth-derived element and transition rules distributed with SoLoud, revision
`e82fd32c1f62183922f08c14c814a02b58db1873`, then passed to Dennis Klatt's
original KLSYN C waveform core.

The fixed phoneme sequence is:

```text
aIwIl kw@Ut &nekstr&kt fr0m D@rivirend dZent@lem&nz @UndZOrn@l.
```

Columns follow SoLoud's `klatt_frame` order:

```text
f0 av F1 b1 F2 b2 F3 b3 F4 b4 F5 b5 f6 b6 fz bz fp bp
ah nopen at tl af sk a1 p1 a2 p2 a3 p3 a4 p4 a5 p5 a6 p6 an ab ap g0
```

The SoLoud speech frontend states that its rsynth-derived data is public domain,
with SoLoud's changes also offered under CC0. The final waveform remains subject
to KLSYN's non-commercial restriction.

Source: https://github.com/jarikomppa/soloud/tree/e82fd32c1f62183922f08c14c814a02b58db1873/src/audiosource/speech
