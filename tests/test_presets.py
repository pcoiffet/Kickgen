import numpy as np
import pytest

from kickgen.params import KickParams
from kickgen.presets import PRESETS
from kickgen.synth import render


def test_five_presets():
    assert len(PRESETS) == 5


@pytest.mark.parametrize("name", PRESETS)
def test_preset_renders(name):
    params = PRESETS[name]
    assert params.name == name
    x = render(params)
    assert np.all(np.isfinite(x)) and np.max(np.abs(x)) > 0.5


@pytest.mark.parametrize("name", PRESETS)
def test_preset_json_round_trip(name):
    params = PRESETS[name]
    assert KickParams.model_validate_json(params.model_dump_json()) == params
