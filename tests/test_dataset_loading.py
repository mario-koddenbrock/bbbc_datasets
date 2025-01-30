import os
import unittest

from tests import DATASETS  # Import shared dataset list


class TestDatasetLoading(unittest.TestCase):
    """Test case to check if datasets can be loaded properly."""

    def test_dataset_loading(self):
        """Test if datasets can be instantiated and data files accessed."""
        for dataset_cls in DATASETS:
            with self.subTest(dataset=dataset_cls.__name__):
                dataset = dataset_cls()  # Instantiate the dataset

                # Check that images, masks, and metadata exist
                image_paths = dataset.get_image_paths()
                segmentation_path = dataset.get_segmentation_path()
                metadata_paths = dataset.get_metadata_paths()

                # Ensure at least some data exists
                self.assertTrue(
                    len(image_paths) > 0,
                    msg=f"No images found for {dataset_cls.__name__}",
                )

                # If the dataset has segmentation, ensure it exists
                if segmentation_path:
                    self.assertTrue(
                        os.path.exists(segmentation_path),
                        msg=f"Segmentation file missing for {dataset_cls.__name__}",
                    )

                # If metadata is expected, ensure it exists
                for meta_path in metadata_paths:
                    self.assertTrue(
                        os.path.exists(meta_path),
                        msg=f"Metadata file missing for {dataset_cls.__name__}",
                    )


if __name__ == "__main__":
    unittest.main()
