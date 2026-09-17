# CS180 Project 1 — Colorizing the Prokudin-Gorskii Photo Collection

## Requirements
- Python 3
- numpy
- scikit-image

```bash
pip install numpy scikit-image
```

## Data setup
Place the provided data folder next to `align_images.py` so the structure looks like:

```
.
├── align_images.py
└── CS180_fa2026_proj1_data/
    ├── cathedral.jpg
    ├── monastery.jpg
    ├── tobolsk.jpg
    ├── church.tif
    ├── emir.tif
    └── ...
```

## Running
```bash
python align_images.py
```

The script does two passes:
1. **Single-scale alignment** runs a ±15 pixel search on the `.jpg` images in `CS180_fa2026_proj1_data/`, aligning the Green and Red images to the Blue image using an L2 norm. The output is saved to `single_scale_alignment/`.
2. **Pyramid alignment** recursively downscales each image (by 0.5x with a hard minimum dimension limit of 350px). This image pyramid aligns at the coarsest level and then scales up the estimate and back up for each level, using a ±15 window for each level. The output is saved to `pyramid_alignment/`.

The computed (x, y) alignment for the Green and Red images is written to `alignment_log.txt` in each output folder.

## Output
```
single_scale_alignment/
├── alignment_log.txt
├── cathedral.jpg
├── monastery.jpg
└── tobolsk.jpg

pyramid_alignment/
├── alignment_log.txt
├── church.jpg
├── emir.jpg
├── wharf.jpg
├── ...
└── (extra hand-picked images)
```
- `single_scale_alignment/`: aligned `.jpg` outputs + `alignment_log.txt`
- `pyramid_alignment/`: aligned outputs + `alignment_log.txt` for all `.jpg` and `.tif` images (including the extra hand-picked images)
