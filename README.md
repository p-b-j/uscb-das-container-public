# Census DAS Container Execution
## Overview
The goal of this repo is to provide a means of running the Census Bureau's Disclosure Avoidance System (DAS) project in a Singularity container.

## Setup
### Gurobi License
You'll need to install a Gurobi license in order to run the DAS. See the [Gurobi website](https://www.gurobi.com/downloads/) for more information about how to obtain a free Gurobi license.

Download your license and save it to the file `~/gurobi.lic`.

If you are on the UW network, there is currently a license server up and running that you can use to dynamically retrieve a license file. This may be easier than downloading a single license as recommended above. If you wish to use this option, create a file `~/gurobi.lic` with the following contents:
```
TOKENSERVER=gurobiserver.cs.washington.edu
``` 

### Building a Singularity Image
Below are two ways to obtain a Singularity image for running the DAS.

#### Temporary Storage Setup
Singularity uses `/tmp` for temproary storage by default. Depending on how much space you have available in `/tmp`, you may run out of space when building the DAS. We recommend setting up a local temporary directory for Singularity to use by running the following commands from the top-level of the repo:

```bash
# Make sure we are at the top of the repo
$ basename $PWD
uscb-das-container-public
# Create temporary directory
$ mkdir singularity_tmp
# Point singularity tmp storage to new directory
# This will need to be run each bash session, or alternatively add it to your .bashrc
$ export SINGULARITY_TMPDIR=/path/to/uscb-das-container-public/singularity_tmp
```

#### **Option 1: Building from a prebuilt Docker Hub image**
Because the current build process requires Docker, there is a pre-built image on Docker Hub that can be used to build a Singularity container. At the time of writing this, the image worked, but we haven't rigorously tested it so please let us know if anything is amiss. Run the following command, which will take about 15 minutes:
```bash
# Make sure we are at the top of the repo
$ basename $PWD
uscb-das-container-public
# Build the Singularity container census_das.img from the Docker Hub image
$ singularity build census_das.img docker://pbjay/census-das-container:latest
```

#### **Option 2: Rebuilding from Docker and Singularity**
You can also build the Docker image locally and then build the Singularity container from the local image:
```bash
# You may or may not need --network host depending on your docker setup
$ docker build --network host -t census-das-container:latest .
# Build a Singularity image from the local docker image
$ singularity build census_das.img docker-daemon:census-das-container:latest
```

## Configuration
There are a few ways to specify changes to where input/output/temporary files are located. These are specified using the `das_container.conf` file.

### DAS files location
By default, the code is meant to run under a subdirectory of your home directory,
and many of the input/output files are based on your home directory (`~/das_files`, `~/gurobi.lic`, `~/das-log`).

If you wish to run this code elsewhere on your system, you can define a new home directory
for the singularity container to use. Note that this new home directory unfortunately cannot be a subdirectory
of your home directory due to the way that singularity mounts/binds directories.

For example, if I wanted my location for the DAS to be under `/scratch/pbj/`, I would do the following:
* Clone this repository (`uscb-das-container-public`) into a subdirectory of `/scratch/pbj/`.
* Setup your input files in the directory `/scratch/pbj/das_files`
* Setup your gurobi license file to have the path `/scratch/pbj/gurobi.lic`
* Specify your new DAS home location updating the `das_home` variable in `das_container.conf` (e.g. `das_home="/scratch/pbj"`)

Now you can run the DAS using the same commands specified in `standalone/README.md` and `cluster/README.md`. Your output files will now appear in `/scratch/pbj/das_files` and your logs should be in `/scratch/pbj/das-logs`.

### DAS Temporary Storage
The container scripts allow you to specify what directory in your system you want to bind to `/tmp` in the container. This is because we have often experienced permissions and space issues. This can be configured using the `container_tmp` variable in `das_container.conf`. By default, it is set to a local directory `singularity_tmp`, which will need to be created before your first run of the DAS.

## Execution
Scripts/instructions for running the DAS in standalone (single-machine) mode are in the `standalone` directory. 
Scripts/instructions for running the DAS in cluster mode are in the `cluster` directory.
All scripts should be run from the top-level of the repository.

The current config of the DAS assumes input/output files will be in `${das_home}/das_files` (see configuration section above for how to configure `${das_home}`) and will output logging info to `${das_home}/das-log`.
When the system finishes, your output files will be in `${das_home}/das_files/output`.

## Notes
This code currently relies on the Census Bureau's [2020 DAS production release repo](https://github.com/uscensusbureau/DAS_2020_Redistricting_Production_Code) which was last incorporated into this repo in October 2021. At that time, there were no plans to update the production code, though if there have been any changes since then please let us know! 
* Container setup done by Porter Jones (pbjones@uw.edu) with help from and to support the research of Abraham Flaxman (abie@uw.edu). Also, many thanks to researchers and engineers at the US Census Bureau for their guidance and help.
