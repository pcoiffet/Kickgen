# KickGen

My own little kick plugin for FL Studio.

Honestly, I just wanted my own kick generator because I thought it would be
fun to build. Set a few knobs, hit generate, get a batch of kicks with a bit
of randomness, listen, keep the ones you like and drag them into FL Studio.

And I wanted to plug an LLM into it, because why not. The idea is that you
type something like "short dry techno kick around 50 Hz" and the model sets
the knobs for you.

## How it works

Every kick is synthesized from a small set of parameters: a sine whose pitch
drops quickly, an amplitude envelope, a short noise click on top, some
saturation and a low-pass filter. Those parameters are stored as JSON next to
each WAV, so any kick can be re-rendered exactly or tweaked later.

The language model never makes audio. It only fills in the parameters, which
are checked against a schema (Pydantic, with min/max on every value) before
anything is rendered. Same parameters, same sound, every time.

The plan is to have two engines reading the same JSON:

- **Python** (numpy/scipy) is the reference. It runs the tests, the
  evaluation and the language model side.
- **JavaScript** runs in the browser, so the generator can live on a plain
  static web page. Tests check that it produces the same samples as the
  Python engine.

## Where it's at

Working today:

- the Python synthesis engine
- WAV export at 44.1 kHz, 24-bit, mono (what FL Studio expects)
- 5 hand-made presets: `techno_tight`, `808_long_F`, `hardstyle_distorted`,
  `lofi_soft`, `house_punchy`
- tests that check the sound itself (pitch of the tail measured with an FFT,
  brightness of the click, effect of the saturation), run on every push

Next up, in this order: random generator with locks on each knob, the
JavaScript engine, the web page with knobs and a grid of kicks to audition,
the text-to-knobs part with an LLM, edits like "shorter" or "one semitone
down", and an evaluation on a set of 25 reference descriptions.

## Try it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
python scripts/render_presets.py output/presets
```

In FL Studio, add `output/presets` under *Options > File settings > Browser
extra search folders*, then drag a kick into the Channel Rack.

Or from Python:

```python
from kickgen import KickParams, export_kick

kick = KickParams(
    name="my_kick",
    duration_s=0.4,
    pitch={"start_hz": 300, "end_hz": 50, "decay_s": 0.03},
    distortion={"amount": 0.3},
)
export_kick(kick, "my_kick.wav")
```

## Limits

It's a single oscillator with a noise click, so don't expect layered,
sample-based kicks. And the presets have only been checked with audio
measurements so far, not with a proper listening session.

## License

MIT
