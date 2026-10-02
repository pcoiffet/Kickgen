"""Render every preset to WAV (+ its parameters as JSON).

Usage: python scripts/render_presets.py [output_dir]
"""

from __future__ import annotations

import sys
from pathlib import Path

from kickgen import PRESETS, export_kick


def main(out_dir: Path) -> None:
    for name, params in PRESETS.items():
        wav = export_kick(params, out_dir / f"{name}.wav")
        wav.with_suffix(".json").write_text(params.model_dump_json(indent=2) + "\n")
        print(wav)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("output/presets"))
