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
                dataset = dataset_cls(download_files=False)

                urls = []

                if dataset.image_paths:
                    if isinstance(dataset.image_paths, list):
                        urls.extend(dataset.image_paths)
                    else:
                        urls.append(dataset.image_paths)

                if dataset.label_path:
                    if isinstance(dataset.label_path, list):
                        urls.extend(dataset.label_path)
                    else:
                        urls.append(dataset.label_path)

                if dataset.metadata_paths:
                    if isinstance(dataset.metadata_paths, list):
                        urls.extend(dataset.metadata_paths)
                    else:
                        urls.append(dataset.metadata_paths)

                for url in urls:
                    if url:  # Ensure the URL is not empty
                        self.assertTrue(
                            self.check_url(url), msg=f"URL not reachable: {url}"
                        )


if __name__ == "__main__":
    unittest.main()
