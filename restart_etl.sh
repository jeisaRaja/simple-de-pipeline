#!/bin/bash

# Log everything to a file (without printing to terminal)
{
  echo "Resetting The ETL Pipeline Process"
  echo "This includes all output and the Docker warehouse"

  # Stop and remove the services
  docker compose -f docker-db/data-warehouse/docker-compose.yml down --volumes

  rm ./data/raw/sales_raw.csv
  rm ./data/raw/electronics_raw.csv
  rm ./data/raw/nlp_raw.csv
  rm ./data/transform/sales_transform.csv
  rm ./data/transform/electronics_transform.csv
  rm ./data/load/sales_load.csv
  rm ./data/load/nlp_load.csv
  rm ./data/load/electronics_load.csv

  # Start the services
  docker compose -f docker-db/data-warehouse/docker-compose.yml up -d
  docker compose up -d
} >> logs/reset_log.log 2>&1

