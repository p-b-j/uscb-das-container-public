#!/usr/bin/bash

source das_container.conf

if [ ! -d ${container_tmp} ]
then
    echo "Error: could not find tmp directory for container"
    echo "\$container_tmp set as: ${container_tmp}"
    exit 1
fi

if [ ! -d ${das_home} ]
then
    echo "Error: could not find das_home directory for container"
    echo "\$das_home set as: ${das_home}"
    exit 1
fi

if [ ! -f ${das_home}/gurobi.lic ]
then
    echo "Error: could not find gurobi.lic file in \$das_home"
    echo "\$das_home set as: ${das_home}"
    exit 1
fi

if [ ! -d ${das_home}/das_files ]
then
    echo "Error: could not find das_files directory in \$das_home"
    echo "\$das_home set as: ${das_home}"
    exit 1
fi

if [ ! -f ${das_home}/das_files/EXT1940USCB.dat ]
then
    echo "Error: could not find EXT1940USCB.dat input file in \${das_home}/das_files"
    echo "\$das_home set as: ${das_home}"
    exit 1
fi

singularity_cmd="singularity exec --home ${das_home} --bind ${container_tmp}:/tmp census_das.img"