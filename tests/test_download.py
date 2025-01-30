import unittest

import requests

from tests import DATASETS  # Import shared dataset list


class TestDatasetURLs(unittest.TestCase):
    """Test case to check if dataset URLs are reachable."""

    def check_url(self, url):
        """Helper function to check if a URL returns a 200 status code."""
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def test_dataset_urls(self):
        """Test if all dataset URLs are valid and accessible."""
        for dataset_cls in DATASETS:
            with self.subTest(dataset=dataset_cls.__name__):
                dataset = dataset_cls()  # This does NOT download the data

                urls = []
                urls.extend(dataset.dataset_info.get("image_paths", []))
                urls.append(dataset.dataset_info.get("segmentation_path", ""))
                urls.extend(dataset.dataset_info.get("metadata_paths", []))

                for url in urls:
                    if url:  # Ensure the URL is not empty
                        self.assertTrue(
                            self.check_url(url), msg=f"URL not reachable: {url}"
                        )


if __name__ == "__main__":
    unittest.main()
