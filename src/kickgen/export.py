"""WAV export in the format FL Studio expects: 44.1 kHz, 24-bit PCM, mono."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf

from kickgen.params import KickParams
from kickgen.synth import SAMPLE_RATE, render


def write_wav(audio: np.ndarray, path: str | Path, sr: int = SAMPLE_RATE) -> Path:
    """Write a mono float signal as 24-bit PCM WAV. Creates parent folders."""
    if audio.ndim != 1:
        raise ValueError(f"expected mono 1-D audio, got shape {audio.shape}")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(path, np.clip(audio, -1.0, 1.0), sr, subtype="PCM_24", format="WAV")
    return path


def export_kick(params: KickParams, path: str | Path) -> Path:
    """Render ``params`` and write it to ``path``."""
    return write_wav(render(params), path)
