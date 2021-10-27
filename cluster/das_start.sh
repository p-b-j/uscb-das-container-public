#!/usr/bin/bash

source util/load_config.sh

${singularity_cmd} ./cluster/singularity_scripts/das_start.sh "spark://${coord_hostname}:7077" ${config_file}
