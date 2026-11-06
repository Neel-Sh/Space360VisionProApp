# 360 VR Image Converter

Python utilities for projecting a flat image onto an equirectangular canvas for experimentation in VR viewers. Despite the repository name, this is **not a native visionOS app**.

The converter rearranges or stretches the supplied image. It does not reconstruct unseen scenery or recover real stereo depth, and viewer compatibility needs testing in the target app.

## Setup

Create a Python environment compatible with the dependencies in `requirements.txt`:

```sh
git clone https://github.com/Neel-Sh/Space360VisionProApp.git
cd Space360VisionProApp
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Convert an image

Start with a small explicit preset; without one, the CLI defaults to **16384 × 8192**, which uses substantial memory.

```sh
python image_to_360vr.py input.jpg --preset mobile --output output.jpg
python image_to_360vr.py input.jpg --preset standard --method spherical
python image_to_360vr.py --help
```

| Preset | Width × height |
| --- | --- |
| `mobile` | 2048 × 1024 |
| `standard` | 4096 × 2048 |
| `high` | 6144 × 3072 |
| `ultra` | 8192 × 4096 |
| `max` | 12288 × 6144 |
| `native` | 16384 × 8192 |
| `extreme` | 20480 × 10240 |

The CLI supports `direct` (default), `simple`, and `spherical` mapping, custom `--width`/`--height`, and top/bottom `--stereoscopic` output. Stereo output is a synthetic image treatment, not measured binocular depth. The parsed `--quality` option is not currently forwarded into the main conversion calls.

## Files and limits

- `image_to_360vr.py`: converter and command-line entry point.
- `example_usage.py`: examples; inspect input paths before running.
- `convert_vr_tiff.py`: helpers expecting locally supplied `deepspace.tiff` or `vr.tiff`.

Input support is defined by the converter: JPG/JPEG, PNG, BMP, `.tiff`, and WebP. Keep source images and generated exports outside version control. See [Contributing](CONTRIBUTING.md) for checks.

## Existing reuse notice

The original README states: "This project is open source. Feel free to modify and distribute." No standalone license file is included.
