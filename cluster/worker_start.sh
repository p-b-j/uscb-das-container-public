#!/usr/bin/bash

source util/load_config.sh

${singularity_cmd} ./cluster/singularity_scripts/worker_start_spark.sh $@ "${coord_hostname}:7077"