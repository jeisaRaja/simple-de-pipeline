#!/bin/bash

# Log everything to a file (without printing to terminal)
{
  echo "Resetting The ETL Pipeline Process"
  echo "This includes all output and the Docker warehouse"

  # Stop and remove the services
  docker compose -f docker-db/data-warehouse/docker-compose.yml down --volumes

  # Start the services
  docker compose -f docker-db/data-warehouse/docker-compose.yml up -d
} >> logs/reset_log.log 2>&1

