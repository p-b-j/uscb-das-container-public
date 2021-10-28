FROM centos:7

# install yum dependencies
RUN yum update -y && yum -y clean all
RUN yum install -y epel-release passwd initscripts cronie wget bzip2 zip unzip && yum -y clean all
RUN yum makecache && yum -y clean all
RUN yum update -y && yum -y clean all

# download gurobi and get gurobi license key
WORKDIR /usr/local
RUN wget https://packages.gurobi.com/9.1/gurobi9.1.1_linux64.tar.gz
RUN tar xfz gurobi9.1.1_linux64.tar.gz
# Hash specific to a particular user's license
# If you are running the script for the first time, you will have to update
# with a hash for your own license. Free academic licenses should be available at gurobi.com
ARG GUROBIHASH
RUN /usr/local/gurobi911/linux64/bin/grbgetkey --path ~ $GUROBIHASH

# copy in directories
COPY 2018_das_release/etc ~/das_centennial/etc

# start the setup scripts
WORKDIR ~/das_centennial/etc
RUN mkdir -p /etc/rsyslog.d/
# Remove sudo from the scripts since we are already sudo
RUN for f in *.sh; do mv ${f} sudo${f} && sed 's/sudo //g' sudo${f} > ${f} && rm sudo${f}; done
RUN chmod +x *.sh
RUN bash -c "source ./standalone_prep.sh"
RUN bash -c "/usr/local/anaconda3/bin/python3.6 -m pip install msgpack"
RUN bash -c "/usr/local/anaconda3/bin/python3.6 -m pip install --upgrade pip"
RUN bash -c "/usr/local/anaconda3/bin/python3.6 -m pip install numpy --upgrade"
RUN bash -c "/usr/local/anaconda3/bin/python3.6 -m pip install randomgen"

ENTRYPOINT ./start_das.sh
