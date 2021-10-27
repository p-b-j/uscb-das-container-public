#!/bin/bash

source util/singularity_scripts/setup_env.sh

# Run standalone config
source util/singularity_scripts/prep_das_run.sh

spark-submit --py-files $ZIPFILE \
    --master $1 \
    --files $ZIPFILE \
    --conf spark.eventLog.enabled=true \
    --conf spark.eventLog.dir=$LOGDIR \
    --conf spark.driver.cores=5 \
    --conf spark.driver.memory=8g \
    --conf spark.executor.memory=8g \
    --conf spark.executor.memoryOverhead=1g \
    --conf spark.driver.maxResultSize=0g \
    --conf spark.network.timeout=3000 \
    das2020_driver.py $2 \
    --loglevel DEBUG \
    --logfilename ${HOME}/das_log.log
