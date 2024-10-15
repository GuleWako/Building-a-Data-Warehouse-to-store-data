# **Building a Data Warehouse for Ethiopian Medical Business Data**


## Project Overview

This project involves creating a data warehouse for Kara Solutions, which stores data on Ethiopian medical businesses scraped from Telegram channels. The objective is to enable insights into trends and patterns within the medical sector in Ethiopia. Key tasks included data scraping, cleaning, transformation, object detection, and API development for data access.

## Data Collection

Data was collected from Telegram channels using the Telethon library.

### Steps:

1. **Telethon API:** Connected to Telegram API to extract text and metadata.
2. **Logging:** Implemented to track the scraping process.
3. **Storage:** Temporarily stored raw data before processing.


## Data Cleaning and Transformation

Using DBT, I performed data cleaning and transformations:

1. **Data Cleaning:** Removed duplicates and handled missing values.
2. **Data Transformation:** Utilized DBT models to structure and transform data, ensuring consistency.


## Object Detection with YOLO

Object detection was implemented using YOLO to analyze images for enhanced insights.

### Steps:

1. **Setup:** YOLOv5 was configured, and dependencies like OpenCV and PyTorch were installed.
2. **Detection:** Images were processed to detect objects, with results stored in PostgreSQL.


## API Development with FastAPI

The data warehouse was made accessible via an API developed with FastAPI.


## Installation

1. **Clone the repository:**

   git clone https://github.com/GuleWako/Building-a-Data-Warehouse-to-store-data.git

   cd Building-a-Data-Warehouse-to-store-data
2. pip install -r requirements.txt
3. **Setup PostgreSQL and DBT:**

   Configure your PostgreSQL database.
4. **Run YOLO and FastAPI:**

   Follow the instructions in the `yolo` and `api` directories.
