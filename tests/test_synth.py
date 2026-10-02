import numpy as np
import pytest

from kickgen.params import KickParams
from kickgen.synth import SAMPLE_RATE, render

CLEAN = {"click": {"level": 0.0}, "distortion": {"amount": 0.0}}


def _spectral_centroid(x: np.ndarray, sr: int = SAMPLE_RATE) -> float:
    mag = np.abs(np.fft.rfft(x))
    freqs = np.fft.rfftfreq(x.size, 1 / sr)
    return float(np.sum(freqs * mag) / np.sum(mag))


def _crest_factor(x: np.ndarray) -> float:
    return float(np.max(np.abs(x)) / np.sqrt(np.mean(x**2)))


def test_length_and_finite():
    x = render(KickParams(duration_s=0.75))
    assert x.shape == (round(0.75 * SAMPLE_RATE),)
    assert np.all(np.isfinite(x))


@pytest.mark.parametrize("peak_dbfs", [0.0, -0.3, -6.0])
def test_peak_normalisation(peak_dbfs):
    x = render(KickParams(peak_dbfs=peak_dbfs))
    assert np.max(np.abs(x)) == pytest.approx(10 ** (peak_dbfs / 20))


def test_deterministic():
    params = KickParams(click={"level": 0.8}, distortion={"amount": 0.5})
    np.testing.assert_array_equal(render(params), render(params))


def test_seed_changes_click_only():
    a = render(KickParams(seed=1, click={"level": 0.8}))
    b = render(KickParams(seed=2, click={"level": 0.8}))
    assert not np.array_equal(a, b)
    np.testing.assert_array_equal(render(KickParams(seed=1, **CLEAN)), render(KickParams(seed=2, **CLEAN)))


def test_ends_silent():
    assert render(KickParams())[-1] == 0.0


@pytest.mark.parametrize("end_hz", [43.65, 50.0, 60.0])
def test_tail_settles_on_end_pitch(end_hz):
    params = KickParams(duration_s=1.5, pitch={"end_hz": end_hz, "decay_s": 0.02}, amp={"decay_s": 1.0}, **CLEAN)
    tail = render(params)[int(0.3 * SAMPLE_RATE) :]
    n = 1 << 20  # zero-pad for sub-Hz resolution
    spectrum = np.abs(np.fft.rfft(tail * np.hanning(tail.size), n))
    f0 = np.fft.rfftfreq(n, 1 / SAMPLE_RATE)[np.argmax(spectrum)]
    assert f0 == pytest.approx(end_hz, abs=0.5)


def test_click_adds_high_frequencies():
    dry = render(KickParams(**CLEAN))
    clicky = render(KickParams(click={"level": 1.0, "tone_hz": 6000}, distortion={"amount": 0.0}))
    assert _spectral_centroid(clicky) > _spectral_centroid(dry) * 1.5


def test_distortion_reduces_crest_factor():
    clean = render(KickParams(**CLEAN))
    driven = render(KickParams(click={"level": 0.0}, distortion={"amount": 0.8}))
    assert _crest_factor(driven) < _crest_factor(clean)


def test_lowpass_darkens():
    bright = render(KickParams(click={"level": 1.0}))
    dark = render(KickParams(click={"level": 1.0}, filter={"lowpass_hz": 500}))
    assert _spectral_centroid(dark) < _spectral_centroid(bright)


def test_longer_decay_longer_tail():
    def energy_after(x, t):
        return float(np.sum(x[int(t * SAMPLE_RATE) :] ** 2))

    short = render(KickParams(duration_s=1.0, amp={"decay_s": 0.05}, **CLEAN))
    long = render(KickParams(duration_s=1.0, amp={"decay_s": 0.4}, **CLEAN))
    assert energy_after(long, 0.3) > 10 * energy_after(short, 0.3)
