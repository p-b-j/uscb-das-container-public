#!/usr/bin/bash

source util/load_config.sh

${singularity_cmd} ./standalone/singularity_scripts/das_start.sh ${config_file}
