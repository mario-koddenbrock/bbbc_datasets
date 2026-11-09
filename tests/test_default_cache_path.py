import os
import tempfile
import unittest
from unittest import mock

import bbbc_datasets.datasets.base_dataset as base_dataset
from bbbc_datasets.datasets.base_dataset import _default_cache_path


class TestDefaultCachePath(unittest.TestCase):
    """Test the resolution of the default dataset download location."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_root = self._tmp.name
        self.legacy = os.path.join(self.tmp_root, "legacy")
        self.cache = os.path.join(self.tmp_root, "cache")

    def tearDown(self):
        self._tmp.cleanup()

    def resolve(self, create_legacy=False, create_cache=False, home=None):
        """Run _default_cache_path against isolated fake directories."""
        if create_legacy:
            os.makedirs(self.legacy)
        if create_cache:
            os.makedirs(self.cache)
        with mock.patch.object(
            base_dataset, "_LEGACY_CACHE_PATH", self.legacy
        ), mock.patch.object(
            base_dataset, "user_cache_dir", lambda app: self.cache
        ), mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("BBBC_DATASETS_HOME", None)
            if home is not None:
                os.environ["BBBC_DATASETS_HOME"] = home
            return _default_cache_path()

    def test_env_var_takes_precedence(self):
        """BBBC_DATASETS_HOME wins over both legacy and platform dirs."""
        home = os.path.join(self.tmp_root, "custom")
        self.assertEqual(
            self.resolve(create_legacy=True, create_cache=True, home=home),
            home,
        )

    def test_legacy_reused_when_platform_cache_missing(self):
        """Existing downloads in the legacy location are kept."""
        self.assertEqual(self.resolve(create_legacy=True), self.legacy)

    def test_platform_cache_preferred_over_legacy(self):
        """Once the platform cache has data, it wins over the legacy dir."""
        self.assertEqual(
            self.resolve(create_legacy=True, create_cache=True),
            self.cache,
        )

    def test_platform_cache_default(self):
        """Fresh install (no legacy dir) uses the platform cache dir."""
        self.assertEqual(self.resolve(), self.cache)

    def test_dataset_uses_resolved_path(self):
        """Dataset constructors default to the resolved cache path."""
        from tests import DATASETS

        with mock.patch.object(
            base_dataset, "_LEGACY_CACHE_PATH", self.legacy
        ), mock.patch.object(
            base_dataset, "user_cache_dir", lambda app: self.cache
        ), mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("BBBC_DATASETS_HOME", None)
            dataset = DATASETS[0](download_files=False)
            self.assertEqual(dataset.download_dir, self.cache)


if __name__ == "__main__":
    unittest.main()
