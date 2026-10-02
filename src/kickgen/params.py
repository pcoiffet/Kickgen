"""Typed, bounded synthesis parameters for a kick drum.

These models are the contract between the (future) LLM layer and the
deterministic synthesis engine: every sound is fully described by a
``KickParams`` instance, and the same instance always renders the same audio.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class PitchEnvelope(_Strict):
    """Exponential pitch sweep: f(t) = end + (start - end) * exp(-t / decay)."""

    start_hz: float = Field(250.0, ge=40.0, le=2000.0, description="Pitch at t=0.")
    end_hz: float = Field(50.0, ge=25.0, le=200.0, description="Pitch the sweep settles to.")
    decay_s: float = Field(0.04, ge=0.002, le=0.5, description="Sweep time constant.")

    @model_validator(mode="after")
    def _sweep_goes_down(self) -> PitchEnvelope:
        if self.end_hz > self.start_hz:
            raise ValueError("end_hz must be <= start_hz (kick pitch sweeps downward)")
        return self


class AmpEnvelope(_Strict):
    """Linear attack, flat hold, then exponential decay."""

    attack_s: float = Field(0.001, ge=0.0, le=0.02)
    hold_s: float = Field(0.02, ge=0.0, le=1.0)
    decay_s: float = Field(0.25, ge=0.01, le=2.0, description="Decay time constant.")


class Click(_Strict):
    """Transient made of band-pass filtered noise with a fast exponential decay."""

    level: float = Field(0.3, ge=0.0, le=1.0, description="0 disables the click.")
    tone_hz: float = Field(3000.0, ge=500.0, le=12000.0, description="Band-pass centre.")
    decay_s: float = Field(0.004, ge=0.0005, le=0.05)


class Distortion(_Strict):
    amount: float = Field(0.0, ge=0.0, le=1.0, description="0 = clean, 1 = heavily driven.")
    mode: Literal["soft", "hard"] = Field("soft", description="tanh saturation or hard clip.")


class Filter(_Strict):
    lowpass_hz: float = Field(20000.0, ge=200.0, le=20000.0, description="20000 = bypass.")


class KickParams(_Strict):
    """Complete description of one kick sound."""

    name: str = Field("kick", min_length=1, max_length=64)
    duration_s: float = Field(0.5, ge=0.05, le=3.0)
    pitch: PitchEnvelope = PitchEnvelope()
    amp: AmpEnvelope = AmpEnvelope()
    click: Click = Click()
    distortion: Distortion = Distortion()
    filter: Filter = Filter()
    peak_dbfs: float = Field(-0.3, ge=-12.0, le=0.0, description="Output peak level.")
    seed: int = Field(0, ge=0, description="Seed for the click noise.")
