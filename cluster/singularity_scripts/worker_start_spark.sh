#!/bin/bash

# Env setup
source util/singularity_scripts/setup_env.sh

# Start worker
spark-class org.apache.spark.deploy.worker.Worker -d spark_work $@
