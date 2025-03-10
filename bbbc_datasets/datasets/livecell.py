import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class LiveCell(BaseBBBCDataset):
    """
    LiveCell Dataset: TODO
    """


def __init__(self, *args, **kwargs):

    # TODO https://www.kaggle.com/datasets/markunys/livecell-dataset

    self.local_path = os.path.join(self.download_dir, "LiveCell")
    self.image_paths = [
        "http://livecell-dataset.s3.eu-central-1.amazonaws.com/LIVECell_dataset_2021/annotations/LIVECell/livecell_coco_train.json",
        "http://livecell-dataset.s3.eu-central-1.amazonaws.com/LIVECell_dataset_2021/annotations/LIVECell/livecell_coco_val.json",
        "http://livecell-dataset.s3.eu-central-1.amazonaws.com/LIVECell_dataset_2021/annotations/LIVECell/livecell_coco_test.json",
    ]
    self.label_path = None
    self.metadata_paths = None
    self.is_3d = False

    super().__init__("Cellpose", *args, **kwargs)
