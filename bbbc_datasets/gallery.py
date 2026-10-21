"""
Example-image gallery for datasets.

For every dataset, a few representative images are selected (spread
over the full image list), downscaled, and saved as small PNG files —
optionally side by side with their label mask when one is available.
The result is a directory of thumbnails that can be embedded in the
README or used for a quick visual check of the data.

Datasets that are not downloaded locally are skipped and reported.

Command line usage::

    python -m bbbc_datasets.gallery --output gallery --examples 3
"""
import argparse
import os

import numpy as np
from PIL import Image

from bbbc_datasets.dataset_manager import DATASETS, DatasetManager


def _load_image_array(path):
    """
    Loads an image file as a numpy array using the package's standard
    loader (handles .ics via diplib, .tif via tifffile, the rest via
    PIL). Multi-frame TIFF stacks are returned in full and reduced by
    ``_reduce_to_2d``.
    """
    from bbbc_datasets.utils.file_io import load_image

    img = load_image(path)
    if img is None:
        raise ValueError(f"Could not read image {path}")
    return np.asarray(img)


def _reduce_to_2d(img):
    """
    Reduces a loaded array to a 2D (H, W) view:
    - (Z, H, W) volumes: middle z-slice
    - (H, W, C) color images: first channel
    - (C, H, W): first channel
    """
    if img.ndim == 4:  # (Z, H, W, C) or (Z, C, H, W)
        img = img[len(img) // 2]
    if img.ndim == 3:
        if img.shape[2] in (1, 3, 4):  # (H, W, C)
            img = img[:, :, 0]
        else:  # (C, H, W) or ambiguous (H, W, many)
            img = img[0]
    if img.ndim != 2:
        raise ValueError(f"Unsupported image shape {img.shape}")
    return img


def _to_uint8(img, clip=(2, 98)):
    """Normalizes an array to uint8, clipping outliers to the given percentiles."""
    img = np.asarray(img, dtype=np.float32)
    lo, hi = np.percentile(img, clip)
    if hi <= lo:
        hi = lo + 1e-6
    img = (img - lo) / (hi - lo)
    return np.clip(img * 255, 0, 255).astype(np.uint8)


def _downscale(img, max_size):
    """Rescales a 2D uint8 image so its longest side is at most max_size."""
    h, w = img.shape
    longest = max(h, w)
    if longest <= max_size:
        return img
    scale = max_size / float(longest)
    resized = Image.fromarray(img, mode="L").resize(
        (max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS
    )
    return np.array(resized)


def _example_indices(n, examples):
    """Picks up to `examples` indices spread over a list of length n."""
    if n <= 0:
        return []
    if n <= examples:
        return list(range(n))
    return sorted(set(int(round(i)) for i in np.linspace(0, n - 1, examples)))


def pick_examples(dataset, examples=3):
    """
    Returns (image_path, label_array_or_None) pairs for up to
    `examples` images of a (locally downloaded) dataset.

    Label loading failures are tolerated: the label is simply None.
    """
    image_paths = dataset.get_image_paths()
    results = []
    for idx in _example_indices(len(image_paths), examples):
        image_path = image_paths[idx]
        label = None
        try:
            label = dataset.get_label(image_path)
        except Exception:
            label = None
        results.append((image_path, label))
    return results


def render_examples(examples, max_size=300, with_labels=True):
    """
    Renders a list of (image_path, label) pairs to a list of uint8 2D
    images (image side by side with its mask when available).
    """
    rendered = []
    for image_path, label in examples:
        img = _downscale(_to_uint8(_reduce_to_2d(_load_image_array(image_path))), max_size)
        if with_labels and label is not None:
            mask = _to_uint8(_reduce_to_2d(np.asarray(label)))
            mask = _downscale(mask, max_size)
            # match heights, then concatenate horizontally with a 4px gap
            h = min(img.shape[0], mask.shape[0])
            gap = np.full((h, 4), 255, dtype=np.uint8)
            img = img[:h]
            mask = mask[:h]
            img = np.concatenate([img, gap, mask], axis=1)
        rendered.append(img)
    return rendered


def save_gallery(output_dir, names=None, examples=3, max_size=300, with_labels=True):
    """
    Generates example images for the given datasets (default: all).

    Returns a dict mapping dataset name to a list of saved file paths
    (empty list when the dataset is not downloaded locally).
    """
    names = names or [cls.__name__ for cls in DATASETS]
    saved = {}
    for name in names:
        cls = next(c for c in DATASETS if c.__name__ == name)
        dataset = cls(download_files=False)
        if not dataset.get_image_paths():
            saved[name] = []
            continue
        out_dir = os.path.join(output_dir, name)
        os.makedirs(out_dir, exist_ok=True)
        paths = []
        for i, rendered in enumerate(
            render_examples(pick_examples(dataset, examples), max_size, with_labels), 1
        ):
            path = os.path.join(out_dir, f"example-{i}.png")
            Image.fromarray(rendered, mode="L").save(path)
            paths.append(path)
        saved[name] = paths
    return saved


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="gallery", help="output directory")
    parser.add_argument("--examples", type=int, default=3, help="examples per dataset")
    parser.add_argument("--max-size", type=int, default=300, help="longest side in px")
    parser.add_argument("--no-labels", action="store_true", help="skip label masks")
    parser.add_argument("--datasets", nargs="*", help="dataset names (default: all)")
    args = parser.parse_args()

    saved = save_gallery(
        args.output,
        names=args.datasets,
        examples=args.examples,
        max_size=args.max_size,
        with_labels=not args.no_labels,
    )
    for name, paths in saved.items():
        if paths:
            print(f"{name}: {len(paths)} examples -> {os.path.join(args.output, name)}")
        else:
            print(f"{name}: skipped (not downloaded)")


if __name__ == "__main__":
    main()
