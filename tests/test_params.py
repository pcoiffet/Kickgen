import pytest
from pydantic import ValidationError

from kickgen.params import KickParams, PitchEnvelope


def test_defaults_are_valid():
    KickParams()


def test_json_round_trip():
    params = KickParams(name="x", duration_s=1.2, pitch={"start_hz": 300, "end_hz": 45})
    assert KickParams.model_validate_json(params.model_dump_json()) == params


@pytest.mark.parametrize(
    "bad",
    [
        {"duration_s": 10.0},
        {"duration_s": 0.0},
        {"pitch": {"end_hz": 5}},
        {"click": {"level": 1.5}},
        {"distortion": {"mode": "fuzz"}},
        {"filter": {"lowpass_hz": 50}},
        {"peak_dbfs": 3.0},
    ],
)
def test_out_of_bounds_rejected(bad):
    with pytest.raises(ValidationError):
        KickParams(**bad)


def test_unknown_fields_rejected():
    with pytest.raises(ValidationError):
        KickParams(reverb=0.5)


def test_upward_sweep_rejected():
    with pytest.raises(ValidationError, match="end_hz"):
        PitchEnvelope(start_hz=50, end_hz=100)
