import os
import requests
import zipfile
from tqdm import tqdm


def download_file(url, save_path):
    """Downloads a file and extracts it if zipped."""
    if os.path.exists(save_path.replace(".zip", "")):
        return  # Already downloaded

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, 'wb') as file, tqdm(
            desc=os.path.basename(save_path),
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))

    # Extract if ZIP
    if save_path.endswith(".zip"):
        with zipfile.ZipFile(save_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(save_path))
        os.remove(save_path)  # Clean up zip file
