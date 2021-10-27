#!/bin/bash

source util/singularity_scripts/setup_env.sh

# Run standalone config
source util/singularity_scripts/prep_das_run.sh

spark-submit --py-files $ZIPFILE \
    --files $ZIPFILE \
    --conf spark.eventLog.enabled=true \
    --conf spark.eventLog.dir=$LOGDIR \
    --conf spark.executor.memoryOverhead=1g \
    --conf spark.dynamicAllocation.enabled=true \
    --conf spark.network.timeout=3000 \
    --conf spark.driver.maxResultSize=0g \
    --conf spark.python.worker.memory=13g \
    --driver-memory 13g \
    --num-executors 1 \
    --executor-memory 13g \
    das2020_driver.py $1 \
    --loglevel DEBUG \
    --logfilename ~/das_log.log
