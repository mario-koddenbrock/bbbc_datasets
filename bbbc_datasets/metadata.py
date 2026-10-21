"""
Fixed-schema metadata for datasets.

Every dataset class declares a ``METADATA`` class attribute of type
``DatasetMetadata``. The schema is fixed — extending it is a breaking
change, so prefer adding values (``None`` = unknown / not applicable)
over new ad-hoc fields.

Values are only filled in from sources that can be verified (the
dataset code, the downloaded data, or the official dataset page);
unknown values stay ``None`` instead of being guessed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

DIMENSIONS = ("2D", "3D")
IMAGING_MODES = ("fluorescence", "dic", "brightfield", "brightfield_fluorescence")
MODALITIES = ("grayscale", "rgb", "multichannel")
DATA_TYPES = ("synthetic", "real")
TASKS = ("segmentation", "counting", "detection", "classification")
LABEL_TYPES = (
    "foreground",
    "instance",
    "outlines",
    "counts",
    "bounding_boxes",
    "biological",
)


@dataclass(frozen=True)
class DatasetMetadata:
    """
    Fixed metadata describing one dataset. Unknown values are None.

    - ``resolution_um``: (dx, dy[, dz]) in micrometers, None when the
      pixel spacing is not uniform across the dataset.
    - ``image_size``: (H, W) or (Z, H, W) in pixels, None when image
      sizes vary within the dataset.
    - ``modality``: logical channel content of an image file
      (a single fluorescence channel is "grayscale", even if the file
      is stored in a multi-channel container).
    - ``label_type``: the kind of supervision ``get_label`` returns.
    """

    # Identity
    name: str
    title: str
    source: str

    # Geometry / imaging
    dim: str
    imaging_mode: str
    modality: str
    resolution_um: tuple | None
    image_size: tuple | None

    # Provenance
    data_type: str
    instrument: str | None
    n_images: int | None

    # Content
    task: str
    label_type: str | None

    # References
    doi: str | None
    license: str | None

    def __post_init__(self):
        self._validate()

    def _validate(self):
        for field, allowed in (
            ("dim", DIMENSIONS),
            ("imaging_mode", IMAGING_MODES),
            ("modality", MODALITIES),
            ("data_type", DATA_TYPES),
            ("task", TASKS),
        ):
            value = getattr(self, field)
            if value not in allowed:
                raise ValueError(
                    f"{self.name}: invalid {field}={value!r}; "
                    f"expected one of {allowed}"
                )
        if self.label_type is not None and self.label_type not in LABEL_TYPES:
            raise ValueError(
                f"{self.name}: invalid label_type={self.label_type!r}; "
                f"expected one of {LABEL_TYPES} or None"
            )

    @property
    def is_3d(self) -> bool:
        return self.dim == "3D"

    def to_dict(self) -> dict:
        return asdict(self)

    def matches(self, **filters) -> bool:
        """
        Returns True when every filter equals the value of the
        corresponding field. Raises ValueError for unknown fields.
        """
        for key, value in filters.items():
            if not hasattr(self, key):
                raise ValueError(f"Unknown metadata field: {key!r}")
            if getattr(self, key) != value:
                return False
        return True
