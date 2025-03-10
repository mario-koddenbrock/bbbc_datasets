# BBBC Datasets - PyTorch Dataset Manager

## 📌 Overview

This package provides a **PyTorch-compatible dataset manager** for
[Broad Bioimage Benchmark Collection (BBBC) datasets](https://bbbc.broadinstitute.org/image_sets).

It allows users to:

- **Download and manage BBBC datasets automatically**
- **Load datasets as PyTorch `Dataset` objects**
- **Handle 2D & 3D images properly**
- **Support image augmentations via `torchvision.transforms`** (#TODO)

## 🚀 Installation

### **Clone the Repository**

```bash
git clone https://github.com/mario-koddenbrock/bbbc_datasets.git
cd bbbc_datasets
```

### **Install Dependencies**

```bash
pip install -r requirements.txt
```

#### Dependencies:

- `torch`, `torchvision` (Deep Learning Framework)
- `numpy`, `tifffile`, `opencv-python` (Image Handling)
- `requests`, `matplotlib` (Downloading & Visualization)

---

## 📂 Available Datasets

You can list all available datasets without downloading them:

```bash
python examples/load_dataset.py
```

**Output:**

```
📂 Available BBBC Datasets:
- BBBC003: DIC microscopy images of mouse embryos for segmentation analysis.
- BBBC004: Synthetic fluorescence microscopy images of nuclei with varying clustering probabilities.
- BBBC005: Simulated fluorescence microscopy images with varying focus blur.
- BBBC006: Z-stack fluorescence microscopy images of human U2OS cells.
- BBBC008: Dataset: Fluorescence microscopy images of human HT29 colon cancer cells.
- BBBC010: Live/dead assay of C. elegans exposed to pathogens.
- BBBC024: 3D Synthetic HL60 Cell Line Images with Varying Clustering Probability and SNR.
- BBBC027: 3D Synthetic Colon Tissue Images with Varying SNR.
- BBBC028: Polymerized Structures in Differential Interference Contrast (DIC) Microscopy.
- BBBC029: Synthetic Differential Interference Contrast (DIC) Images.
- BBBC032: 3D Mouse Embryo Blastocyst Cells.
- BBBC033: 3D Mouse Trophoblast Stem Cells.
- BBBC034: 3D Induced Pluripotent Human Stem Cells (hiPSC).
- BBBC035: Simulated HL60 Cells from the Cell Tracking Challenge.
- BBBC038: Kaggle 2018 Data Science Bowl - Nuclei Segmentation.
- BBBC039: Nuclei of U2OS Cells in a Chemical Screen.
- BBBC046: FiloData3D - Synthetic 3D Time-Lapse Imaging of A549 Cells with Filopodia.
- BBBC050: Nuclei of Mouse Embryonic Cells.
```

---

## 🎨 Visualizing Dataset Samples

### **Display First Image from Each Dataset**

##### Requires downloading datasets first!

```bash
python examples/load_dataset.py
```

---

## 📥 Download and Load a Dataset

### **Load a Dataset as a PyTorch Dataset**

```python
from bbbc_datasets.datasets.bbbc004 import BBBC004
from torch.utils.data import DataLoader

# Load BBBC004 dataset
dataset = BBBC004()

# Create a DataLoader
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

# Iterate through data
for images, labels in dataloader:
    print(f"Batch shape: {images.shape}, Labels: {labels.shape if labels is not None else 'None'}")
```

---

## 🛠 Running Tests

### **Validate Dataset URLs**

```bash
python -m unittest tests/test_dataset_urls.py
```

- **Checks if all dataset URLs are reachable** 🌍

### **Verify Dataset Loading**

```bash
python -m unittest tests/test_dataset_loading.py
```

- **Ensures datasets can be loaded and accessed correctly** 🛠

---

## 📝 Up-next

- **Thinking of what is up next**
- **Maybe integrating other datasets as cellpose, livecell, etc.**

---

## 🙌 Contributing

Contributions are welcome! If you find issues or want to add new features, feel free to:

- **Submit a Pull Request**
- **Report Issues** in the GitHub Issues section

---

## 📜 License

This project is licensed under the **MIT License**.
