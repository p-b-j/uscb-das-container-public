# NOTE: This script is only to be run on an EC2 instance using Amazon Linux 2 AMI (HVM), SSD Volume Type - ami-0de53d8956e8dcf80

# Provision EC2 instance [m5.xlarge or m5.2xlarge, ami-02da3a138888ced85 (64-bit x86)]
# This document is predicated on the fact that you'll be using the $USER account in the listed image.

# Install dependencies (Anaconda, Spark, Hadoop, Gurobi...)
BASEDIR=$(dirname "$0")
echo "$BASEDIR"

sudo $BASEDIR/aws_prep.sh || exit 1
sudo $BASEDIR/gurobi_install.sh || exit 1

cd ~
mkdir das_files
mkdir das_files/output

# Add to ~/.bashrc:
if ! grep DAS_VERSION $HOME/.bashrc >/dev/null 2>&1 ; then
  echo 'export LD_LIBRARY_PATH=/usr/local/gurobi911/linux64/lib:/usr/local/hadoop-3.1.4/lib/native
export GUROBI_HOME=/usr/local/gurobi911/linux64
export PATH=$PATH:/usr/local/gurobi911/linux64/bin
export GRB_LICENSE_FILE=$HOME/gurobi.lic
export PATH=$PATH:/usr/local/anaconda3/bin
export PYSPARK_PYTHON=/usr/local/anaconda3/bin/python3.6
export PYSPARK_DRIVER_PYTHON=/usr/local/anaconda3/bin/python3.6
export SPARK_HOME=/usr/local/spark/spark-2.4.7-bin-hadoop2.7
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export DAS_VERSION=Standalone' >> ~/.bashrc
fi

. ~/.bashrc || exit 1

#`grbgetkey [key-code]` (Get key-code from Gurobi.com)
python3 -m pip install --upgrade pip --user || exit 1

cd $GUROBI_HOME 
sudo /usr/local/anaconda3/bin/python3 setup.py install || exit 1

sudo yum -y install python-pip texlive || exit 1
python3 -m pip install pytest pyspark --user || exit 1

