# Audible SDR

A quadrature (I/Q) software-defined radio, simulated entirely in the audio band so you can see **and hear** every stage: antenna → RF preselector → quadrature LO → mixers → IF filter → I + jQ (with blind IQ-imbalance correction) → DFT mask & shift → iDFT → audio.

Plain JavaScript, no build step, no dependencies. Open `index.html` in a browser (headphones recommended).

- Simulated at 32 kHz on a 4.096 s loop (2¹⁷ samples); filters are applied in the frequency domain over the whole loop.
- Stations: AM at 3 kHz, ISB at 7.5 kHz (different programmes on each sideband), CW at 11 kHz, FSK at 15 kHz.
- Stage 2: mixer gain/phase/DC errors, estimated from signal statistics (mean, σ, I–Q correlation) and corrected.

By Ali Raheem, G3ALI — https://g3ali.com/sdr/ (mirror: https://ali-raheem.github.io/audible-sdr/)

## Editing

- **Words:** everything you read on the page is in [`text.md`](text.md), one `## key` block per paragraph, heading or caption, grouped by section. Light formatting works: `` `code` ``, `*italic*`, `**bold**`, `[link](url)`, and inline HTML such as `f<sub>LO</sub>`.
- **Layout, controls and DSP:** [`src/page.html`](src/page.html). The `{{key}}` markers in it are filled from `text.md`.
- **Build:** `./build.sh` (Python 3, no packages) writes `audible-sdr.html` (the page body, also used for the claude.ai artifact) and the standalone `index.html`. It stops if a key used by the page is missing from `text.md`. Don't edit those two generated files by hand.
