![banner](https://github.com/user-attachments/assets/e69784b9-0392-4de7-a423-e506dd1a0223)
This project is an Extract, Transform, Load (ETL) pipeline designed using Python, Docker, and Luigi. The pipeline automates the process of data extraction from various sources, transformation into a structured format, and loading into a target database or storage system.

## Requirements Gathering & Solution

### Source Data:

- [Amazon Sales Data](https://hub.docker.com/r/shandytp/amazon-sales-data-docker-db)
- [Marketing Data](https://drive.google.com/file/d/1J0Mv0TVPWv2L-So0g59GUiQJBhExPYl6/view?usp=sharing)
- [BBC Sport News Source](https://www.bbc.com/sport)

### Problems:

- **Sales Data**: is stored in a PostgreSQL database, but it contains many missing values and incorrect formats.
- **Product Pricing Data**: is available in CSV file with inconsistent formatting and many missing values.
- **Team Data Scientist**: requires a dataset for Natural Language Processing (NLP) research but currently has no data.

### Proposed Solutions:

- **Data Aggregation and Integration**:

  - **Sales Data**: Extract data from the PostgreSQL database, clean and format it to resolve missing values and formatting issues. Load the cleaned data into a unified database for easy analysis.
  - **Product Pricing Data**: Extract data from the CSV file, clean and standardize it, and then load it into the unified database.
  - **NLP Data**: Perform web scraping to collect text data from news site articles - [BBC Sport News](https://www.bbc.com/sport/football). Clean and prepare the text data for NLP research.

- **Data Pipeline Design**:

  - **Extraction**: Use Python scripts to pull data from PostgreSQL and CSV file, and perform web scraping for the NLP dataset.
  - **Transformation**: Clean and format the data `pandas`. Handle missing values, standardize inconsistent formats, and normalize text data.
  - **Loading**: Insert the cleaned and transformed data into a centralized PostgreSQL database.

- **Scheduling and Automation**:
  - Implement a scheduling system using **Luigi** and **Crontab** to automate the ETL process, ensuring that data is extracted, transformed, and loaded on a regular basis.
  - Use **Docker** to containerize the ETL pipeline, making it easier to deploy and manage across different environments.

## ETL Pipeline Design

![ETL Pipeline Design](https://github.com/user-attachments/assets/a0d16614-bf47-4540-b447-8b6a101aa129)
![Luigi Graph](https://github.com/user-attachments/assets/a88a9923-1027-4ac3-8e45-9496e330a721)

## How To Run:

This snippet will restart/reset the docker warehouse container and remove the output from previous luigi output (csv files).

```bash
sudo ./restart_etl.sh
python3 etl.py --local-scheduler
```

With crontab

```bash
crontab -e
```

And add this snippet to the crontab, fill the working directory and the scheduling frequency.

```bash
* * * * * /bin/bash [Working Directory]/run_etl.sh >> [Working Directory]/logs/cron_output.log 2>&1
```

### Environment Variables

```
export POSTGRES_USER=<your_postgres_username>
export POSTGRES_PASSWORD=<your_postgres_password>
export POSTGRES_DB=<your_postgres_database>
export POSTGRES_HOST=<your_postgres_host_and_port>
export POSTGRES_HOST_WAREHOUSE=<your_warehouse_host_and_port>
export WD=<your_project_working_directory>
```

### Python Libraries

- `pandas` for data manipulation.
- `SQLAlchemy` for database interaction.
- `luigi` for building the etl pipeline.
- `requests` for web scraping.
- `beautifulsoup4` for data extraction from HTML.
- `python-dotenv` for managing loading environment variables.

## Output

### Scenario 1

Running the ETL pipeline, then performing a SELECT query to retrieve the last 5 data entries from the warehouse.

- Amazon Sales
  ![amazon sales data warehouse](https://github.com/user-attachments/assets/8d0fa8a9-7dd0-4240-b806-516e2c6c7323)
- Electronic Products
  ![electronic products data warehouse](https://github.com/user-attachments/assets/91d448ca-b9b0-42f6-a44d-faed89074efc)
- NLP News Articles
  ![NLP News Data Warehouse](https://github.com/user-attachments/assets/56ae1c55-135a-4930-958a-e12c9560e607)

### Scenario 2

Before inserting 'Testing Product' to source database. If we query `SELECT` with name `Testing Product` will yield no results.
![](https://github.com/user-attachments/assets/3ad708fa-1edc-46cd-bef9-286c2f7b8261)
After insert 'Testing Product' to source database.
![](https://github.com/user-attachments/assets/598e8d00-5985-432b-a7ae-3e5a52af2759)

## Snippet

### Extracting Sales Data

![Code Snippet Extracting Sales Data](https://github.com/user-attachments/assets/928af13a-6a99-4131-8480-ba71933d415b)

### Transforming Sales Data

![Code Snippet Transforming Sales Data](https://github.com/user-attachments/assets/812cfe1c-ac7d-40c3-9af9-a9efdacf22bb)

### Extracting Electronic Products

![Code Snippet Extracting Electronic Products](https://github.com/user-attachments/assets/62dadc1d-2fad-4bf9-b875-1af856176c09)

### Transforming Electronics Products

![Code Snippet Transforming Electronic Products](https://github.com/user-attachments/assets/41c6a698-fce3-4aae-8060-cb3c90cc1848)

### Extracting NLP Data

![Code Snippet Extracting NLP Data](https://github.com/user-attachments/assets/4424df36-be60-428e-bce1-3c7a71827042)

### Loading Data

![Code Snippet Loading Data](https://github.com/user-attachments/assets/d2ad562b-2b93-4035-a39c-989bf02e0920)
