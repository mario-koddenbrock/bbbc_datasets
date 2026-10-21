from setuptools import setup, find_packages

setup(
    name="bbbc_datasets",
    version="1.0.0",
    author="Mario Koddenbrock",
    author_email="koddenbrock@gmail.com",
    description="PyTorch-compatible dataset manager for BBBC datasets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mario-koddenbrock/bbbc_datasets",
    packages=find_packages(),
    install_requires=[
        "torch~=2.6.0",
        "numpy~=2.2.2",
        "tifffile~=2025.1.10",
        "opencv-python~=4.11.0.86",
        "requests~=2.32.3",
        "matplotlib~=3.10.0",
        "tqdm~=4.66.5",
        "diplib~=3.5.2",
        "pillow~=11.1.0",
        "pandas~=2.2.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
