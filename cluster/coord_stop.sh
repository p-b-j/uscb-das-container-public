#!/usr/bin/bash

source util/load_config.sh

${singularity_cmd} ./cluster/singularity_scripts/coord_stop_spark.sh
