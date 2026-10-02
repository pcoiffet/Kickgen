"""Deterministic kick drum synthesis engine (no AI involved).

Signal chain:
    sine with pitch sweep x amplitude envelope
    + band-passed noise click
    -> distortion -> low-pass filter -> end fade -> peak normalisation
"""

from __future__ import annotations

import numpy as np
from scipy import signal

from kickgen.params import KickParams

SAMPLE_RATE = 44_100
_END_FADE_S = 0.005


def _time_axis(duration_s: float, sr: int) -> np.ndarray:
    return np.arange(round(duration_s * sr)) / sr


def _body(params: KickParams, t: np.ndarray) -> np.ndarray:
    p = params.pitch
    # Closed-form integral of the exponential pitch sweep: exact phase, no drift.
    phase = 2 * np.pi * (p.end_hz * t + (p.start_hz - p.end_hz) * p.decay_s * (1 - np.exp(-t / p.decay_s)))
    return np.sin(phase) * _amp_envelope(params, t)


def _amp_envelope(params: KickParams, t: np.ndarray) -> np.ndarray:
    a = params.amp
    env = np.ones_like(t)
    if a.attack_s > 0:
        env = np.minimum(env, t / a.attack_s)
    decay_start = a.attack_s + a.hold_s
    tail = t > decay_start
    env[tail] = np.exp(-(t[tail] - decay_start) / a.decay_s)
    return env


def _click(params: KickParams, t: np.ndarray, sr: int) -> np.ndarray:
    c = params.click
    if c.level == 0:
        return np.zeros_like(t)
    noise = np.random.default_rng(params.seed).uniform(-1.0, 1.0, t.size)
    nyquist = sr / 2
    band = [c.tone_hz / 2, min(c.tone_hz * 2, 0.95 * nyquist)]
    sos = signal.butter(2, band, btype="bandpass", fs=sr, output="sos")
    burst = signal.sosfilt(sos, noise) * np.exp(-t / c.decay_s)
    peak = np.max(np.abs(burst))
    return c.level * burst / peak if peak > 0 else burst


def _distort(params: KickParams, x: np.ndarray) -> np.ndarray:
    d = params.distortion
    if d.amount == 0:
        return x
    gain = 1 + 19 * d.amount
    if d.mode == "soft":
        return np.tanh(gain * x)
    return np.clip(gain * x, -1.0, 1.0)


def _lowpass(params: KickParams, x: np.ndarray, sr: int) -> np.ndarray:
    cutoff = params.filter.lowpass_hz
    if cutoff >= 20000 or cutoff >= sr / 2:
        return x
    sos = signal.butter(4, cutoff, btype="lowpass", fs=sr, output="sos")
    return signal.sosfilt(sos, x)


def _fade_out(x: np.ndarray, sr: int) -> np.ndarray:
    n = min(round(_END_FADE_S * sr), x.size)
    out = x.copy()
    out[x.size - n :] *= np.linspace(1.0, 0.0, n)
    return out


def _normalize(x: np.ndarray, peak_dbfs: float) -> np.ndarray:
    peak = np.max(np.abs(x))
    if peak == 0:
        return x
    return x * (10 ** (peak_dbfs / 20) / peak)


def render(params: KickParams, sr: int = SAMPLE_RATE) -> np.ndarray:
    """Render a kick to a mono float64 array in [-1, 1]. Same params -> same samples."""
    t = _time_axis(params.duration_s, sr)
    x = _body(params, t) + _click(params, t, sr)
    x = _distort(params, x)
    x = _lowpass(params, x, sr)
    x = _fade_out(x, sr)
    return _normalize(x, params.peak_dbfs)
