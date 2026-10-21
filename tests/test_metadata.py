import json
import unittest

from bbbc_datasets.dataset_manager import DatasetManager
from tests import DATASETS


class TestMetadata(unittest.TestCase):
    def test_all_datasets_have_valid_metadata(self):
        for cls in DATASETS:
            with self.subTest(dataset=cls.__name__):
                meta = cls.METADATA
                self.assertIsNotNone(meta, f"{cls.__name__} has no METADATA")
                self.assertEqual(meta.name, cls.__name__)
                self.assertTrue(meta.title)
                self.assertTrue(meta.source.startswith("http"))
                # dim must agree with is_3d (also enforced by __init__)
                instance = cls(download_files=False)
                self.assertEqual(meta.dim == "3D", instance.is_3d)
                # must be JSON-serializable
                json.dumps(meta.to_dict())

    def test_3d_datasets(self):
        names = {c.__name__ for c in DatasetManager.filter_datasets(dim="3D")}
        self.assertEqual(names, {"BBBC024", "BBBC027", "BBBC044"})

    def test_legacy_filter_3d_matches_dim(self):
        legacy = {c.__name__ for c in DatasetManager.filter_datasets(filter_3d=True)}
        modern = {c.__name__ for c in DatasetManager.filter_datasets(dim="3D")}
        self.assertEqual(legacy, modern)

    def test_combined_filters(self):
        names = {
            c.__name__
            for c in DatasetManager.filter_datasets(imaging_mode="dic", label_type="foreground")
        }
        self.assertIn("BBBC003", names)
        self.assertIn("BBBC019", names)
        self.assertNotIn("BBBC007", names)  # outlines, not foreground

    def test_counting_datasets(self):
        names = {c.__name__ for c in DatasetManager.filter_datasets(task="counting")}
        self.assertEqual(names, {"BBBC001", "BBBC002", "BBBC044"})

    def test_unknown_field_raises(self):
        with self.assertRaises(ValueError):
            DatasetManager.filter_datasets(bogus_field="x")

    def test_filter_3d_dim_conflict(self):
        with self.assertRaises(ValueError):
            DatasetManager.filter_datasets(filter_3d=True, dim="2D")

    def test_get_metadata(self):
        meta = DatasetManager.get_metadata("BBBC044")
        self.assertEqual(meta.dim, "3D")
        self.assertEqual(meta.task, "counting")
        with self.assertRaises(ValueError):
            DatasetManager.get_metadata("BBBC999")

    def test_get_dataset_info_includes_metadata(self):
        info = DATASETS[0](download_files=False).get_dataset_info()
        self.assertIs(info["metadata"], DATASETS[0].METADATA)


if __name__ == "__main__":
    unittest.main()
