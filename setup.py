from setuptools import setup, find_packages

setup(
    name="bbbc_datasets",
    version="0.1.2",
    author="Mario Koddenbrock",
    author_email="koddenbrock@gmail.com",
    description="PyTorch-compatible dataset manager for BBBC datasets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mario-koddenbrock/bbbc_datasets",
    packages=find_packages(),
    install_requires=[
        "torch",
        "torchvision",
        "numpy",
        "tifffile",
        "opencv-python",
        "requests",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
