# Minimum Temperature Raster Analysis – Peru
***Intermediate Python Course – Group Project***

Team Members:
- Almenara Espino, Diego Alonso
- Ramirez Zapata, Ivan Andres
- Ramos Vargas, Luis Fernando
- Riega Nuñez, Gabriel Antonio Fermin

## Overview

This project analyzes minimum temperature (Tmin) data for Peru using spatial raster analysis techniques.
It combines geospatial computation, visualization, and policy analysis to identify areas most affected by frost and cold surges (friaje), and proposes evidence-based public policy measures to mitigate their impacts.

The project is implemented in Python and deployed as an interactive Streamlit web application.

👉 Live App: [Streamlit link]

## Repository Structure
```
Minimum-Temperature-Raster/
│
├── app/                     # Streamlit app
│   └── streamlit_app.py
│
├── data/                    # Raster + shapefiles
│   ├── shape_file_distritos/
│   └── tmin_raster.tif
│
├── notebooks/               # EDA and calculations
│   └── tmin_zonalstats.ipynb
│
├── requirements.txt         # Required Python libraries
│
└── README.md                # Instructions and the deployment link
```

## Setup & Reproducibility

To run locally, follow these steps:

1. Clone repository
```
git clone https://github.com/DiegoAlmenara/Minimum-Temperature-Raster.git
cd Minimum-Temperature-Raster
```
2. Create and activate virtual environment
```
python -m venv env
env\Scripts\activate      # for Windows | source venv/bin/activate (Linux/MacOS)
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Run the Streamlit app
```
streamlit run app/app.py
```
This should start a locally hosted server and automatically open a browser tab with the application.
