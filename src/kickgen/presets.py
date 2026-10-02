"""Hand-written reference presets.

They exercise each stage of the engine and later serve as few-shot examples
for the LLM layer.
"""

from __future__ import annotations

from kickgen.params import AmpEnvelope, Click, Distortion, Filter, KickParams, PitchEnvelope

PRESETS: dict[str, KickParams] = {
    p.name: p
    for p in [
        KickParams(
            name="techno_tight",  # short, dry, 50 Hz
            duration_s=0.35,
            pitch=PitchEnvelope(start_hz=280, end_hz=50, decay_s=0.025),
            amp=AmpEnvelope(attack_s=0.0005, hold_s=0.01, decay_s=0.09),
            click=Click(level=0.45, tone_hz=4000, decay_s=0.003),
            distortion=Distortion(amount=0.15, mode="soft"),
        ),
        KickParams(
            name="808_long_F",  # long sub tail tuned to F1 (43.65 Hz)
            duration_s=1.8,
            pitch=PitchEnvelope(start_hz=120, end_hz=43.65, decay_s=0.05),
            amp=AmpEnvelope(attack_s=0.002, hold_s=0.05, decay_s=0.6),
            click=Click(level=0.1, tone_hz=2000, decay_s=0.002),
        ),
        KickParams(
            name="hardstyle_distorted",  # heavily saturated, long tail
            duration_s=0.9,
            pitch=PitchEnvelope(start_hz=600, end_hz=55, decay_s=0.03),
            amp=AmpEnvelope(attack_s=0.0005, hold_s=0.15, decay_s=0.3),
            click=Click(level=0.6, tone_hz=5000, decay_s=0.005),
            distortion=Distortion(amount=0.85, mode="hard"),
            filter=Filter(lowpass_hz=9000),
        ),
        KickParams(
            name="lofi_soft",  # rounded, no click, dark
            duration_s=0.5,
            pitch=PitchEnvelope(start_hz=160, end_hz=55, decay_s=0.04),
            amp=AmpEnvelope(attack_s=0.004, hold_s=0.01, decay_s=0.15),
            click=Click(level=0.0),
            distortion=Distortion(amount=0.1, mode="soft"),
            filter=Filter(lowpass_hz=1200),
            peak_dbfs=-1.0,
        ),
        KickParams(
            name="house_punchy",  # classic punch, warm saturation
            duration_s=0.45,
            pitch=PitchEnvelope(start_hz=350, end_hz=58, decay_s=0.035),
            amp=AmpEnvelope(attack_s=0.0005, hold_s=0.03, decay_s=0.13),
            click=Click(level=0.35, tone_hz=3000, decay_s=0.004),
            distortion=Distortion(amount=0.35, mode="soft"),
            filter=Filter(lowpass_hz=12000),
        ),
    ]
}
