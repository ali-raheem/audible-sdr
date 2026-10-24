<!--
  Audible SDR: all the words on the page.

  Edit the text under each "## key" line, then run ./build.sh to rebuild the page.
  - Leave the "## key" lines alone; the build stops and tells you if one goes missing.
  - Lines starting with a single "#" are signposts and are ignored.
  - A blank line starts a new paragraph (where a paragraph makes sense).
  - Formatting: `code` for formulas, *italic*, **bold**, [link text](https://example.com).
    HTML also works, e.g. f<sub>LO</sub> for a subscript.
  - preset.*.name is the entry in the "Tune to" menu, .title and .desc are the card.
-->


# Introduction

## intro.eyebrow
Quadrature direct-conversion receiver · simulated at 32 kHz · 4.096 s loop

## intro.title
Audible SDR

## intro.p1
By Ali Raheem, **G3ALI** · [g3ali.com](https://g3ali.com/) · [Source on GitHub](https://github.com/ali-raheem/audible-sdr)

## intro.lede
This webpage shows the inner workings of what a basic typical software-defined radio, but with the frequencies shifted to be in the audible range. Instead of tuning to around 7MHz the "RF" is a 32 kHz sampled signal with 6 transmissions between 3 and 15kHz. Each stage is laid out as the waveoform of the signals, audio, spectrum/waterfall or other display as appropriate.

## intro.heading1
On the air

## intro.p2
The page opens as an idealized receiver, withou faults or noise but once you're comfortable you can enable issues to work around.
Active noise/fault panels are marked <b class="adv-badge-inline">active</b>.


# Introduction · Experiments panel

## experiments.title
Experiments

## experiments.summary
Here are some ready made experiments to try, although I'd suggest working through tuning manually first before having a look.

# Introduction

## intro.p3
The play buttons should be comfortable and audible. If you want to compare levels use the spectra and look at the dB scales. Full scale is 0dB.

# 1 · Antenna

## antenna.title
Antenna

## antenna.p1
The entire signal arrives at the antenna at once. The chaos you hear is just what the antenna hears as a mixture of different frequencies in different patterns and encodings.

# 1 · Antenna · Noise panel

## noise.title
Noise

## noise.summary
Real life, even very good setups will have noise either from other signals, atmospheric noise depending on the RF band. Try adding some noise even at a low level (0.015 say).

## noise.p1
Every real receiver adds noise, and noise is spread across the whole band while a signal sits in one place. Each filter that narrows the band removes noise but keeps the signal, so the signal-to-noise ratio improves by 10·log₁₀ of the bandwidth ratio. Going from a 2 kHz SSB-sized mask to 150 Hz for CW gains about 11 dB, which is why CW gets through when voice does not. FM behaves differently: it is clean down to a threshold and then breaks up suddenly. Try the CQ and NBFM presets as you raise the noise.


# 2 · RF preselector

## preselector.title
RF preselector

## preselector.p1
The RF preselector is a bandpass filter before the mixer and rest of the SDR. An ideal multiplier would not need it, but real switching mixers also respond at harmonics of the LO (3×, 5×…; see the panel in section 3) and can be overloaded by strong signals far from the wanted one. The preselector stops the mixer from ever seeing them. The grey trace is the antenna signal and the green curve is the filter. Drag on the spectrum to move it. Real designs for filters quickly become combersome and might be impractical in terms of cost of parts, quality of parts or ease of tuning.


# 3 · Local oscillator

## lo.title
Local oscillator

## lo.p1
One oscillator, two outputs 90° apart: `LO<sub>I</sub> = cos(2πf<sub>LO</sub>t)` and `LO<sub>Q</sub> = −sin(2πf<sub>LO</sub>t)`. Played separately they sound identical. The difference is only phase, which the X–Y plot shows as a circle; with no quadrature it would collapse to a line. The frequency is rounded to a multiple of 0.244 Hz so the loop stays seamless. You can pick between ideal sine waves, and more common square waves. Square waves are the base sine wave with odd harmonics added.


# 3 · LO · Switching mixers panel

## harmonics.title
Switching mixers and LO harmonics

## harmonics.summary
Why a square-wave LO also receives at 3× and 5× its frequency, and how the preselector stops it.

## harmonics.p1
Many SDRs, such as the Tayloe detector in the SoftRock, use switches instead of true multipliers. Switching is the same as multiplying by a square wave, and a square wave contains odd harmonics at 3f<sub>LO</sub>, 5f<sub>LO</sub> and so on, at 1/3, 1/5… of the amplitude. Each harmonic mixes its own part of the spectrum down to baseband, on top of the wanted signal. The preselector in section 2 is what keeps those frequencies out. The square wave here is band-limited below Nyquist.


# 4 · Mixers

## mixer.title
Mixers

## mixer.p1
Each path mixes (multiplies) the preselected signal by its LO, the result of this is signals at frequencies of sum and differences. A station at `f<sub>LO</sub> + Δ` lands at Δ and at `2f<sub>LO</sub> + Δ`. The I output on its own cannot tell `f<sub>LO</sub> + Δ` from `f<sub>LO</sub> − Δ`: both fold onto the same audio frequency. This is called an image. With the ISB preset, play I alone and you hear the melody and the bass line on top of each other. Q has the same spectrum magnitude but a different phase, and that phase is what separates them later.

## mixer.p2
Real mixers are not perfect: the Q branch may have a little more gain than I, the LO split may not be exactly 90°, and LO leakage adds DC. Section 8 covers what that does and how to remove it digitally.


# 5 · IF filter

## if-filter.title
IF filter

## if-filter.p1
The same low-pass filter on I and on Q. In a zero-IF receiver the “IF” is baseband, so this is the channel filter and the ADC’s anti-alias filter in one. It removes the sum products near `2f<sub>LO</sub>` and anything outside the channel. It is also the anti-alias filter for the ADC in the next section: switch it off there and see what folds in. Drag on the spectrum to set the cut-off.


# 6 · ADC and sample rate

## adc.title
ADC and sample rate

## adc.p1
In the ideal receiver the ADC samples at the full 32 kHz, so it changes nothing and you can skip this section.


# 6 · ADC · Sample rate panel

## adc-panel.title
Sample rate and aliasing

## adc-panel.summary
What the ADC sample rate limits, why the IF filter must come before it, and how SDRs lower the rate.

## adc-panel.p1
The IF output is still a continuous voltage. A pair of ADCs samples I and Q at a rate `f<sub>s</sub>`, and from then on the receiver only knows the band `−f<sub>s</sub>/2 … +f<sub>s</sub>/2`. Anything outside it does not vanish. It folds back into the band, which is called aliasing, and once it has folded no later filter can separate it from the wanted signal. Lower the sample rate and the spectrum narrows to the green band. With the IF filter in circuit nothing harmful folds in. Switch it off and stations from all over the 16 kHz “RF” band land on top of the one you wanted.

## adc-panel.p2
Because I and Q are sampled together, the usable band is the full `±f<sub>s</sub>/2`, twice what a single real ADC at the same rate covers. Real SDRs usually sample fast (an RTL-SDR runs at a few MS/s) and then lower the rate digitally in stages with CIC and half-band filters. Each stage follows the same rule as here: filter first, then drop samples. Lower rates make every later step cheaper.


# 7 · Complex baseband

## iq.title
Complex baseband, I + jQ

## iq.p1
The samples are now numbers in a computer. Treat each pair as one complex sample `z = I + jQ`. Its spectrum is no longer mirror-symmetric: whatever was above the LO is now at positive frequencies and whatever was below it is at negative frequencies. The X–Y plot traces z in the complex plane.


# 8 · IQ mismatch

## mismatch.title
IQ mismatch and correction

## mismatch.p1
The ideal receiver has perfectly matched I and Q paths, so there is nothing to correct and you can skip this section on a first pass.


# 8 · IQ mismatch · panel

## mismatch-panel.title
IQ mismatch and its correction

## mismatch-panel.summary
How imperfect mixers leak an image across 0 Hz, and how to measure and remove it using only the received signal.

## mismatch-panel.p1
Everything so far assumed a perfect quadrature mixer. Real ones have two I and Q paths built from separate parts, so they never match exactly. With a gain ratio `g` and a phase error `φ` the Q path delivers `g·sin(θ − φ)` instead of `sin θ`, and the LO leaking into the mixer adds a DC offset to each output. Look back at the LO’s X–Y plot in section 3 while you move the sliders: the circle becomes a tilted ellipse.

## mismatch-panel.p2
The damage shows up as an *image*. A signal at +Δ also appears, weaker, at −Δ, and the other way round. How much weaker is the image rejection ratio. A 1 dB gain error alone limits it to about 25 dB, and 1° of phase error alone to about 41 dB. That is enough to hear the lower sideband of the ISB station leak into the upper one, which is exactly the job the I + jQ receiver was meant to do.

## mismatch-panel.heading1
1 · Inject the fault

## mismatch-panel.p3
These errors are applied in the analog part of the receiver: gain and phase to the Q output of the LO in section 3, and DC offsets at the mixer outputs in section 4. The image is easiest to see with the CQ preset, where two clean tones appear on the positive side, and easiest to hear with the ISB upper preset.

## mismatch-panel.heading2
2 · Estimate it from the signal and correct it

## mismatch-panel.p4
The receiver cannot see the fault directly, but it can measure statistics of the received signal. The means give the DC offsets. The ratio of standard deviations gives the gain error. The correlation between I and Q gives the phase error, because `ρ = sin ψ` with `ψ = −φ`. The correction is then `Q′ = (Q/g − I·sin ψ) / cos ψ`. This assumes the true I and Q are uncorrelated and of equal power. That holds for most signals but not for a lone carrier at exactly 0 Hz, so try the AM preset with a fault and watch the estimate go wrong.


# 9 · DFT, mask and shift

## dft.title
DFT, mask and shift

## dft.p1
Take the DFT of the whole loop of z (131 072 points), multiply it by a mask that keeps only the part you want, then roll the bins to move that part along the frequency axis. Because positive and negative frequencies are now separate, the mask can pick a single sideband. The image that stage 4 could not separate is now simply somewhere else on the axis. Drag on the top spectrum to place the mask. The shift moves every component by the same number of hertz, which changes the pitch you hear, and harmonics stop being harmonic, which is why mistuned SSB sounds like Donald Duck.

## dft.term1
Signal

## dft.term2
Power in the mask

## dft.term3
SNR

## dft.term4
Noise bandwidth

## dft.p2
The S-meter measures the power inside the mask, as a real receiver’s meter measures what gets through its IF filter, so it includes any noise. Each S-unit is 6 dB, and here S9 is −30 dBFS. It moves with the signal while audio plays. The SNR compares the signal with the noise the receiver lets through, which this simulation can work out exactly because it knows the noise it added. With noise switched on (section 1), narrow the mask and watch the SNR rise as the noise bandwidth falls, until the mask starts cutting into the signal itself.


# 9 · DFT · Single-mixer panel

## single-mixer.title
Why Q matters: the single-mixer receiver

## single-mixer.summary
Hear what a receiver with only an I channel can and cannot separate.

## single-mixer.p1
A *single-mixer* receiver only has I, a real signal whose spectrum is always mirror-symmetric. Its mask can only be mirrored too, and it cannot shift: moving a real signal’s positive half up moves its negative half down. A real direct-conversion receiver tunes with its LO instead. Try it with the ISB presets: the melody and the bass line come out together whatever you do with the mask.


# 10 · Inverse DFT and detector

## output.title
Inverse DFT and detector

## output.p1
The inverse DFT gives a complex time signal again, but a speaker needs a real one. Turning z into audio is the detector’s job, and each mode of transmission wants a different one.

## output.term1
Product detector, `Re{z}`

## output.text1
For SSB, CW and FSK. A classic receiver multiplies by a beat-frequency oscillator (BFO) and keeps the real part. Here the shift in section 9 is the BFO.

## output.term2
Envelope, `|z|`

## output.text2
The diode detector of a crystal set. It ignores phase, so tuning errors do not matter, but it distorts when one sideband is missing or the carrier fades.


# 10 · Detector · More detectors panel

## more-detectors.title
More detectors: synchronous AM and FM

## more-detectors.summary
Detectors that use the phase of z: a phase-locked loop for AM and a discriminator for FM.

## more-detectors.term1
Synchronous AM, `Re{z·e<sup>−jφ̂</sup>}`

## more-detectors.text1
A phase-locked loop follows the carrier and rotates it onto the real axis: a product detector that tunes itself. It still works on a single sideband plus carrier, which halves the noise bandwidth and lets you avoid interference on the other side. Try the “Synchronous AM” preset, then switch to the product detector.

## more-detectors.term2
FM discriminator, `arg(z[n]·z*[n−1])`

## more-detectors.text2
The phase step between samples is the instantaneous frequency. This only works with I and Q, because a real signal has no phase to measure. On the FSK station it recovers the data bits as a square wave.


# Footer

## footer.p1
Filters are applied in the frequency domain over the whole 4.096 s loop, so they are zero-phase and the loop repeats without a click. The preselector and IF filters use Butterworth magnitude responses of the chosen order. Mixing happens at the 32 kHz simulation rate, so sum products above 16 kHz alias back down; the IF filter removes them just as it removes the in-band ones. Spectra are Welch averages of 32 Hann-windowed 2048-point DFTs.

## footer.p2
Audible SDR by Ali Raheem, G3ALI. Source code and issues: [github.com/ali-raheem/audible-sdr](https://github.com/ali-raheem/audible-sdr). 73!


# Presets (station cards and the Tune to… menu)

## preset.am.name
AM broadcast · 3.0 kHz

## preset.am.title
Nursery tune on AM

## preset.am.desc
Full carrier with both sidebands. Detected with |z|, so the LO phase does not matter.

## preset.isbU.name
ISB upper sideband · 7.5 kHz

## preset.isbU.title
Arpeggio on the upper sideband

## preset.isbU.desc
Two programmes share one suppressed carrier. The mask keeps positive frequencies only.

## preset.isbL.name
ISB lower sideband · 7.5 kHz

## preset.isbL.title
Bass line on the lower sideband

## preset.isbL.desc
Same tuning, mask moved to negative frequencies. A real-only mixer cannot do this.

## preset.cq.name
G3ALI calling CQ · 11.4 kHz

## preset.cq.title
CQ DE G3ALI

## preset.cq.desc
Two Morse signals 400 Hz apart, both in the IF passband. A 150 Hz mask picks out G3ALI and a −400 Hz shift sets a 700 Hz note.

## preset.cw.name
CW beacon · 11.0 kHz

## preset.cw.title
“SDR” beacon

## preset.cw.desc
Same tuning, mask moved to +700 Hz: now only the slow beacon is heard and the CQ call is gone.

## preset.fm.name
NBFM · 12.75 kHz

## preset.fm.title
A tune on narrowband FM

## preset.fm.desc
Constant amplitude, the tune is in the phase. Only the FM discriminator recovers it; try Re{z} or |z| instead.

## preset.sync.name
Synchronous AM, one sideband

## preset.sync.title
Synchronous AM

## preset.sync.desc
LO 50 Hz low, and the mask keeps only the carrier and upper sideband: half the bandwidth, so half the noise. The PLL finds the carrier and locks. Switch to the product detector to hear the 50 Hz offset it removes.

## preset.fsk.name
FSK data · 15 kHz

## preset.fsk.title
Data at 62.5 baud

## preset.fsk.desc
Mark and space at ±250 Hz, shifted up by 1.2 kHz into a comfortable pitch.

## preset.lowif.name
Low-IF: tuned 500 Hz low

## preset.lowif.title
Low-IF tuning

## preset.lowif.desc
LO at 7.0 kHz puts the upper sideband at +500…+2100 Hz. The DFT stage selects it and shifts it back by −500 Hz.

## preset.trap.name
3rd-harmonic trap

## preset.trap.title
Square LO, no preselector

## preset.trap.desc
A square LO at 5 kHz also mixes at 15 kHz, so the FSK station appears. Narrow the preselector around 5 kHz, or switch to a sine LO, to remove it.

## preset.alias.name
Aliasing: no anti-alias filter

## preset.alias.title
Aliasing

## preset.alias.desc
ISB upper sampled at 4 kHz with the IF filter switched off. Every station folds into the ±2 kHz band. Switch the IF filter back on in section 6.

## preset.real.name
Single-mixer receiver

## preset.real.title
No Q channel

## preset.real.desc
ISB upper heard through I alone. The melody and the bass line cannot be separated. Switch the receiver back to I + jQ in section 9.

## preset.imb.name
Mismatched mixer

## preset.imb.title
Gain and phase errors

## preset.imb.desc
ISB upper with 1.5 dB and 8° of quadrature error plus DC. The bass line leaks into the melody. Turn on correction in section 8.
