# Audio Deepfake Detection

## Speech Deepfake Generation

### Text-to-Speech (<mark>TTS</mark>)

#### Rule-Based

##### Speech Representation: Acoustic parameters

##### Alignment / Timing: Handcrafted rules

##### Generation Method: Rule-based synthesis

##### Speaker Capability: Fixed voice

#### Unit Selection

##### Speech Representation: Recorded units

##### Alignment / Timing: Unit boundaries

##### Generation Method: Search and concatenation

##### Speaker Capability: Fixed database

#### HMM-Based SPSS

##### Speech Representation: Spectrum, F0, duration

##### Alignment / Timing: HMM states

##### Generation Method: Statistical generation

##### Speaker Capability: Speaker adaptation

#### Neural SPSS

##### Speech Representation: Acoustic features

##### Alignment / Timing: Explicit duration

##### Generation Method: Neural prediction

##### Speaker Capability: Multi-speaker

#### Autoregressive TTS

##### Speech Representation: Mel-spectrogram / waveform

##### Alignment / Timing: Attention

##### Generation Method: Sequential generation

##### Speaker Capability: Zero-shot emerging

#### Parallel TTS

##### Speech Representation: Mel / latent / waveform

##### Alignment / Timing: Duration or monotonic alignment

##### Generation Method: Parallel generation

##### Speaker Capability: More controllable

#### Prompt-Based TTS

##### Speech Representation: Codec tokens / latent

##### Alignment / Timing: Prompt-conditioned modeling

##### Generation Method: LM, flow, diffusion, masking

##### Speaker Capability: Zero-shot and cross-lingual

### Voice Conversion (VC)

### Other or Hybrid Methods

## Non-Speech Deepfake Generation

### Music

### Environmental Sounds
