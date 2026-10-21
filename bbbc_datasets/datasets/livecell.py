import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset
from bbbc_datasets.metadata import DatasetMetadata


class LiveCell(BaseBBBCDataset):
    """
    LiveCell Dataset: TODO
    """

    METADATA = DatasetMetadata(
        name="LiveCell",
        title="LiveCell dataset",
        source="https://www.kaggle.com/datasets/markunys/livecell-dataset",
        dim="2D",
        imaging_mode="fluorescence",
        modality="grayscale",
        resolution_um=None,
        image_size=None,
        data_type="real",
        instrument=None,
        n_images=None,
        task="segmentation",
        label_type="bounding_boxes",
        doi=None,
        license=None,
    )

    def __init__(self, *args, **kwargs):

        # TODO https://www.kaggle.com/datasets/markunys/livecell-dataset

        self.KEY = "LiveCell"
        self.image_paths = [
            "http://livecell-dataset.s3.eu-central-1.amazonaws.com/LIVECell_dataset_2021/annotations/LIVECell/livecell_coco_train.json",
            "http://livecell-dataset.s3.eu-central-1.amazonaws.com/LIVECell_dataset_2021/annotations/LIVECell/livecell_coco_val.json",
            "http://livecell-dataset.s3.eu-central-1.amazonaws.com/LIVECell_dataset_2021/annotations/LIVECell/livecell_coco_test.json",
        ]
        self.label_path = None
        self.metadata_paths = None
        self.is_3d = False

        super().__init__(*args, **kwargs)
