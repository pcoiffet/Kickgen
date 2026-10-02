import numpy as np
import pytest
import soundfile as sf

from kickgen.export import export_kick, write_wav
from kickgen.params import KickParams
from kickgen.synth import render


def test_wav_format_matches_fl_studio_target(tmp_path):
    path = export_kick(KickParams(), tmp_path / "sub" / "kick.wav")
    info = sf.info(path)
    assert info.samplerate == 44_100
    assert info.channels == 1
    assert info.subtype == "PCM_24"
    assert info.format == "WAV"


def test_wav_content_round_trip(tmp_path):
    params = KickParams(distortion={"amount": 0.4})
    path = export_kick(params, tmp_path / "kick.wav")
    data, _ = sf.read(path, dtype="float64")
    np.testing.assert_allclose(data, render(params), atol=2 / 2**23)


def test_rejects_stereo(tmp_path):
    with pytest.raises(ValueError, match="mono"):
        write_wav(np.zeros((10, 2)), tmp_path / "x.wav")
