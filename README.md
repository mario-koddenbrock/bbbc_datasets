# BBBC Datasets - PyTorch Dataset Manager

![BBBC Logo](logo.png)

## 📌 Overview

This package provides a **PyTorch-compatible dataset manager** for **Broad Bioimage Benchmark Collection (BBBC) datasets
**.

It allows users to:

- **Download and manage BBBC datasets automatically** 📥
- **Load datasets as PyTorch `Dataset` objects** 📊
- **Handle 2D & 3D images properly** 🔬
- **Support image augmentations via `torchvision.transforms`** 🎨
- **List and select datasets dynamically** ⚡

## 🚀 Installation

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/mario-koddenbrock/bbbc_datasets.git
cd bbbc_datasets
```

### **2️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

#### 🔹 Dependencies:

- `torch`, `torchvision` (Deep Learning Framework)
- `numpy`, `tifffile`, `opencv-python` (Image Handling)
- `requests`, `matplotlib` (Downloading & Visualization)

---

## 📂 Available Datasets

You can list all available datasets:

```bash
python utils/dataset_manager.py
```

🔹 **Example Output:**

```
📂 Available BBBC Datasets:
- BBBC003: Dataset of Human Embryos (DIC Microscopy)
- BBBC004: Synthetic Nuclei (Varying Clustering)
- BBBC005: Focus Blur Synthetic Cells
...
```

---

## 📥 Download and Load a Dataset

### **1️⃣ Load a Dataset as a PyTorch Dataset**

```python
from utils.dataset_manager import DatasetManager
from torch.utils.data import DataLoader

# Load BBBC003 dataset
dataset = DatasetManager.get_dataset("BBBC003")

# Create a DataLoader
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

# Iterate through data
for images, labels in dataloader:
    print(f"Batch shape: {images.shape}, Labels: {labels.shape if labels is not None else 'None'}")
```

---

## 🎨 Visualizing Dataset Samples

### **2️⃣ Display First Image from Each Dataset**

```bash
python examples/load_dataset.py
```

🔹 **What Happens?**

- **Loads the first image of each dataset** ✅
- **Extracts the middle Z-slice if 3D** ✅
- **Overlays segmentation labels (if available)** ✅

---

## 🛠 Running Tests

### **3️⃣ Validate Dataset URLs**

```bash
python -m unittest tests/test_dataset_urls.py
```

- **Checks if all dataset URLs are reachable** 🌍

### **4️⃣ Verify Dataset Loading**

```bash
python -m unittest tests/test_dataset_loading.py
```

- **Ensures datasets can be loaded and accessed correctly** 🛠

---

## 📝 Roadmap

- ✅ **Support more BBBC datasets**
- ✅ **Improve multi-channel image handling**
- ⏳ **Add segmentation model training examples**
- ⏳ **Extend transformations for data augmentation**

---

## 🙌 Contributing

Contributions are welcome! If you find issues or want to add new features, feel free to:

- **Submit a Pull Request** 🔄
- **Report Issues** in the GitHub Issues section 🚀

---

## 📜 License

This project is licensed under the **MIT License**.
