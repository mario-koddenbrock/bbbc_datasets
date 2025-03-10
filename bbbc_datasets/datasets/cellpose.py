import os

from bbbc_datasets.datasets.base_dataset import BaseBBBCDataset


class Cellpose(BaseBBBCDataset):
    """
    Cellpose Dataset: TODO
    """

    def __init__(self, *args, **kwargs):
        self.KEY = "Cellpose"
        self.image_paths = [
            "https://www.cellpose.org/train/6f2bc6b4858f3d12129a005fe1d5b5eba0d36f85",
            "https://www.cellpose.org/test/6f2bc6b4858f3d12129a005fe1d5b5eba0d36f85",
            "https://www.cellpose.org/train_cyto2/6f2bc6b4858f3d12129a005fe1d5b5eba0d36f85",
        ]
        self.label_path = None
        self.metadata_paths = None
        self.is_3d = False

        super().__init__(*args, **kwargs)
