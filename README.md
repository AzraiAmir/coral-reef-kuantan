\# Azr.AI — Coral Reef Monitoring



\*\*An Integrated Deep Learning Framework for Coral Species Detection, Health Assessment, and Connectivity Modelling\*\*



\*Azr.AI = Automated Zonation \& Reef Artificial Intelligence\*



\[!\[Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

\[!\[PyTorch](https://img.shields.io/badge/PyTorch-2.5-red.svg)](https://pytorch.org/)

\[!\[YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green.svg)](https://github.com/ultralytics/ultralytics)



\## Overview



Azr.AI is a PhD research framework for automated coral reef monitoring in the turbid nearshore waters of Kuantan, Pahang, Malaysia. It integrates:



1\. \*\*Deep Learning Detection\*\* — YOLOv8 multi-label detection of coral species, growth forms, and anthropogenic debris

2\. \*\*Automated Health Assessment\*\* — Coral-CRCA colour analysis for bleaching severity (KBI)

3\. \*\*Environmental Integration\*\* — Correlation of health metrics with environmental parameters

4\. \*\*Biophysical Connectivity Modelling\*\* — Lagrangian particle tracking for source-sink dynamics

5\. \*\*Standard Monitoring Criteria\*\* — Validated protocol for turbid reef environments



\## Repository Structure

coral-reef-kuantan/

├── .streamlit/ # Dashboard theme config

├── src/ # 87 Python modules

│ ├── data\_acquisition/ # Appendix F (7 files)

│ ├── preprocessing/ # Appendix G (15 files)

│ ├── detection/ # Appendix H (14 files)

│ ├── health\_assessment/ # Appendix I (8 files)

│ ├── connectivity/ # Appendix I (10 files)

│ ├── environmental/ # Appendix I (1 file)

│ ├── spatial\_analysis/ # Appendix J (10 files)

│ ├── validation/ # Appendix J (2 files)

│ ├── visualization/ # Appendix J (3 files)

│ ├── standards/ # Appendix K (1 file)

│ └── utils/ # Appendix K (3 files)

├── tests/ # Unit tests

├── setup.py # Package install

├── .gitignore

└── README.md





\## Installation



```bash

\# Clone

git clone -b src https://github.com/AzraiAmir/coral-reef-kuantan.git

cd coral-reef-kuantan



\# Environment

conda create -n azrai python=3.10 -y

conda activate azrai



\# Geospatial (conda only)

conda install -c conda-forge gdal geopandas rasterio fiona shapely contextily -y



\# PyTorch (CPU)

pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1



\# Core libraries

pip install numpy pandas scipy scikit-learn scikit-image matplotlib seaborn pyyaml tqdm

pip install opencv-python opencv-contrib-python Pillow albumentations easyocr exifread

pip install ultralytics

pip install parcels xarray netCDF4 cartopy networkx

pip install statsmodels lime grad-cam

pip install streamlit plotly folium streamlit-folium

pip install meshkernel xugrid



\# Install package

pip install -e .

