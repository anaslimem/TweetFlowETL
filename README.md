# TweetFlowETL 

An ETL (Extract, Transform, Load) pipeline project that extracts tweets from the Twitter API, transforms the data, and loads it into Azure Blob Storage.

## Project Overview

This project demonstrates an end-to-end data pipeline using **Apache Airflow** to automate the following:

- **Extract** tweet data using Twitter API (e.g., tweets by Elon Musk).
- **Transform** the data (filtering, restructuring, cleaning).
- **Load** the final JSON data into **Azure Blob Storage** (Container: `tweet`).

## Folder Structure

    ├── dags/
     └── twitter_ETL_dag.py # Airflow DAG definition
    ├── logs/ # Airflow logs
    ├── plugins/ # Custom Airflow plugins (if any)
    ├── .env # Environment variables
    ├── docker-compose.yaml # Docker environment setup for Airflow
    ├── elonmusk_tweets.json # Extracted/Transformed data (sample)
    ├── README.md # Project documentation
    ├── requirements.txt # Python dependencies

### Prerequisites

- Docker
- Twitter Developer Account (Bearer Token)
- Azure Blob Storage Account

### Clone the Repo

``` bash

git clone https://github.com/anaslimem/TweetFlowETL.git
cd TweetFlowETL
```

## Set Environment Variables

### Create a .env file and add:

```bash
TWITTER_BEARER_TOKEN=your_token_here
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
```

## Build & Start Airflow

```bash
docker-compose up --build
```

## Output

The transformed tweets are saved as a JSON file and uploaded to Azure Blob Storage in a container named tweet.

## Tools & Technologies

- Python

- Apache Airflow

- Twitter API v2

- Azure Blob Storage

- Docker

## Contact

Made with ❤️ by Anas Limem
    - Linkedin:  
    https://www.linkedin.com/in/anaslimem
