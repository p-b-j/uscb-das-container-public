#!/bin/bash

source util/load_config.sh

${singularity_cmd} ./util/singularity_scripts/test_gurobi_lic.sh
