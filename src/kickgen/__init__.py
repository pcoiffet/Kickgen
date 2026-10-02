"""KickGen: text-to-kick-drum generator for FL Studio."""

from kickgen.export import export_kick, write_wav
from kickgen.params import KickParams
from kickgen.presets import PRESETS
from kickgen.synth import SAMPLE_RATE, render

__all__ = ["KickParams", "PRESETS", "SAMPLE_RATE", "export_kick", "render", "write_wav"]
__version__ = "0.1.0"
