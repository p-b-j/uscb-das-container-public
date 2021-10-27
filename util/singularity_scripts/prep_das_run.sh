cd das_decennial

LOGDIR=$HOME/das-log
mkdir -p $LOGDIR || exit 1

ZIPFILE=/tmp/das_decennial$$.zip
export ZIPFILE
zip -r -q $ZIPFILE . || exit 1

export DAS_RUN_UUID=$(cat /proc/sys/kernel/random/uuid)