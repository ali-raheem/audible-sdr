# Audible SDR

A quadrature (I/Q) software-defined radio, simulated entirely in the audio band so you can see **and hear** every stage: antenna → RF preselector → quadrature LO → mixers → IF filter → I + jQ (with blind IQ-imbalance correction) → DFT mask & shift → iDFT → audio.

Plain JavaScript, no build step, no dependencies. Open `index.html` in a browser (headphones recommended).

- Simulated at 32 kHz on a 4.096 s loop (2¹⁷ samples); filters are applied in the frequency domain over the whole loop.
- Stations: AM at 3 kHz, ISB at 7.5 kHz (different programmes on each sideband), CW at 11 kHz, FSK at 15 kHz.
- Stage 2: mixer gain/phase/DC errors, estimated from signal statistics (mean, σ, I–Q correlation) and corrected.

`audible-sdr.html` is the same page without the document wrapper (used for the claude.ai artifact); `index.html` is the standalone version.
