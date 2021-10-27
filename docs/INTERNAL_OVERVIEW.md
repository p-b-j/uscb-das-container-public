# Internal Documentation
The purpose of this documentation is to provide enough internal information to facilitate maintaining and adding to the project. It mainly documents what was originally done when setting up the project, and better practices/alternatives may exist.

## Sections
1. [Container Setup](#container-setup)
2. [DAS Code Setup and Modification](#das-code-setup-and-modification)
3. [Project and DAS Configuration](#project-and-das-configuration)
4. [Synthetic Population Scripts](#synthetic-population-scripts)

# Container Setup
The public release of the DAS was originally intended to be run in an AWS environment, which was impractical for running multiple experiments due to the high cost for each run. Our project made use of containers in order to allow us to run experiments on servers we already had access to.

There are two parts of the container setup, a `Dockerfile` that contains a recipe for building the container, and a set of `singularity` commands for running the container. `Singularity` is used for running the container at the request of the IHME server admins due to security considerations. There was an attempt to use `singularity` for the recipe specification, but due to some limitations with the build interface/image caching it became cumbersome to iterate with. If one really doesn't want to use `docker` to build containers, it should be possible to port the recipe over to `singularity`, though it may require some tweaking.

## Docker Recipe
The purpose of the `docker` recipe is to setup the environment w/packages and tools necessary for running the DAS. It relies on both manual installation of packages as well as a few scripts from the 2018 public release of the DAS.

The `docker` recipe is fairly simple. It is based on `CENTOS 7`, which is no longer going to be supported by Red Hat. Right now AWS still supports `CENTOS 7` but the container recipe may need to be updated in the future if AWS and the Census Bureau move away from it.

The script installs a few package dependencies using `yum`. It then installs the `gurobi` software and downloads a `gurobi` license to the container to use for setup. Right now anyone attempting to rebuild the container will need to procure a temporary license and update the `Dockerfile` with its hash when installing the script (should be able to get an academic one easily from the `gurobi` website). There may be a way to get it working with a floating license, but the original builder was working on a computer w/out access to the license server and was not able to test it out.

After the `gurobi` setup, the script runs the `2018_das_release/etc/standalone_prep.sh` script from the 2018 public release, and updates a few `Python` packages.

## Singularity Scripts/Commands
`singularity` provides a nice interface for building an image from a `docker` image (see the project's `README` for more details).

The DAS can be run in the container in both a `standalone` and `cluster` mode, with directories that contain scripts and instructions for each. These both rely on Apache Spark.

The scripts responsible for starting a run of the DAS in the container have two main parts. The first is a script responsible for running the desired task inside the container, including any setup that needs to be done. These scripts are inside the `singularity_scripts` directory within the `standalone` and `cluster` directories. The second part is a wrapper script that starts the inner script inside the `singularity` container. The wrapper scripts are the scripts directly inside the `standalone` and `cluster` directories.

The purpose of the wrapper structure was to make the commands that the user runs to start the DAS as simple as possible, leaving all of the `singularity` script parameters and internals inside of the wrapper script. See the configuration instructions below for more in-depth info about configuring these scripts. 

## DAS Setup File Modifications
A few changes needed to be made to the files in `2018_das_release/etc/`. Here are the changes made to each file from the version that was part of the 2018 public release:

* `aws_prep.sh`
    * Changed `spark` distribution from `2.3.1` to `2.4.8`
    * Added a separate check to see if the distribution folder already exists before extracting the tar file
    * Changed the `tar xfvz $SPARK_FILE` command to `tar xfvz $SPARK_TAR`
* `gurobi_install.sh`
    * Changed `gurobi` version from `7.5.2` to `9.1.1`
    * Added the following code at the bottom of the script to use `anaconda` to install `gurobi` for `Python`
    ```
    ANACONDA_ROOT=/usr/local/anaconda3
    if [ ! -d $ANACONDA_ROOT ]; then
    echo Please install Anaconda and rerun this script
    exit 1
    else
    echo Installing Gurobi python3.6 support
    cd $GUROBI_HOME
    $ANACONDA_ROOT/bin/python3.6 setup.py install
    fi
    ```
* `standalone_prep.sh`
    * Remove the wget/extraction commands for the spark/hadoop packages (these were installed in earlier scripts)
    * Change `hadoop` version in `LD_LIBRARY_PATH` from `3.1.2` to `3.1.4`
    * Change `gurobi` version from `7.5.2` to `9.1.1`
    * Remove lines that add spark to the path (`export PATH=$PATH:$HOME/spark-2.4.0-bin-hadoop2.7/bin` and `export PATH=$SPARK_HOME:$PATH`). These are done in a later step now
    * Change `spark` version from `2.4.0` to `2.4.7`

## Gurobi License Server
Since the DAS was intended to be run on servers within the IHME cluster, a `gurobi` license server was setup to allow the same license file to be used regardless of which server was running the DAS. The license server was setup on a server under the CSE department, but should likely be migrated over to IHME servers with the help of some admins.

* Here is a form to request an academic site license, which is needed to run the token server: https://assets.gurobi.com/pdf/requests/ACADEMIC-SITE-REQUEST.pdf

* Here is how to retrieve the license once it is granted: https://www.gurobi.com/documentation/9.1/quickstart_mac/retrieving_a_floating_lice.html

* Here is some documentation on starting a token server once you've retrieved the license: https://www.gurobi.com/documentation/9.1/quickstart_mac/sta_a_token_server.html

* And then finally you should setup the client license for the DAS according to these directions (there are also directions specific to this project in the project README): https://www.gurobi.com/documentation/9.1/quickstart_mac/creating_a_token_server_cl.html#subsection:clientlicensetoken

We also found `gurobi` support to be helpful and responsive, so likely they can be contacted if any guidance is needed: https://www.gurobi.com/support/

# DAS Code Setup and Modification
This is documentation for the bulk of the DAS code base, including where different modules were obtained from and what modifications were necessary to get the code up and running.

## Code Setup
The DAS code is in the `das_decennial` directory of the project. It was last copied from the Census Bureau's [2020 DAS production release repo](https://github.com/uscensusbureau/DAS_2020_Redistricting_Production_Code), which should be in its final state barring any unforeseen changes.

## Steps for Updating Code
If you need to incorporate any updates of the DAS code into this repo, you may unfortunately have to go through a pretty manual process to update the code base.

* Copy in the code from the updated source.
* Remove any `git` files that are not `.gitignore` from the directories, since they will mess with the `git` configuration for our project.
* Make the modifications listed below. If new modifications need to be made, please add to the list.

### Modifications Made
The DAS code needs a bit of modification to run outside of the Census Bureau's AWS environment. There are a number of AWS-specific packages used and some logging infrastructure that cannot be replicated. Here are a list of changes that were needed in order to run the DAS, with the disclaimer that some of the changes may need to be redesigned if they remove a part of the system deemed critical.

* `das_decennial` directory
    * `das_decennial/das2020_driver.py`
        * Comment out the `boto3` import
        * In `DASDelegate.log_testpoint` add a void `return` at the top of the function such that the function doesn't run. This removes the testpoint logging but a fix would require a larger restructuring of logging (maybe manageable if testpoint logging is needed in the future)
        * In `__main__` comment out the two calls to `dashboard.SQS_Client().flush()`. We aren't using the dashboard logging right now since it was pretty reliant on `AWS` and didn't seem necessary, so no need to flush the queue
    * `das_decennial/das_utils.py`
        * In `clearPath` change the `subprocess.run(['hadoop', 'fs', '-rm', '-r', path], stdout=subprocess.PI    PE, stderr=subprocess.PIPE)` command to `subprocess.run(['rm', '-r', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)` since we aren't using a `hadoop` filesystem.
    * `das_decennial/programs/dashboard.py`
        * Comment out the `boto3` and `botocore.config` imports
        * In `send_obj` add a void `return` at the top of the function such that the function doesn't run. This removes the dashboard url logging but a fix would require a larger restructuring of the system (probably manageable if dashboard url logging is needed in the future)
    * `das_decennial/programs/emr_control.py`
        * Comment out the `boto3` and `botocore` imports
    * `das_decennial/programs/engine/engine_utils.py`
        * In `DASEngineHierarchical.loadNoisyAnswers` change the `else` branch of the `if path.startswith(CC.HDFS_PREFIX):` check to only have the line `level_rdd = spark.sparkContext.pickleFile(das_utils.expandPathRemoveHdfs(path))`. This is due to the code assuming we are on an AWS machine and not allowing local paths
    * `das_decennial/programs/nodes/manipulate_nodes.py`
        * In `geoimp_wrapper` change the `clogging.setup` call to just be `clogging.setup(level=logging.INFO)`
        * In `geoimp_wrapper_root` change the `clogging.setup` call to just be `clogging.setup(level=logging.INFO)`
    * `das_decennial/programs/optimization/optimizer.py`
        * Comment out the `boto3` import
        * In `AbstractOptimizer.getGurobiEnvironment` change the `clogging.setup` call to just be `clogging.setup(level=logging.INFO)`
        * In `AbstractOptimizer.getGurobiEnvironment` change `self.getconfig(CC.GUROBI_LIC)` to `os.path.expandvars(self.getconfig(CC.GUROBI_LIC))`
        * In `Optimizer.setObjAndSolve` change the `if save_model:` check to be `if save_model and False:`, essentially not saving the model ever. If we want to support saving the model, we'll have to either modify the `saveModelToS3` function or write our own simple function to do so.
    * `das_decennial/programs/reader/cef_2020/cef_validator_classes.py`
        * In `CEF20_UNIT.parse_line` after `inst` is initiated, include the following check:
        ```Python
        if '|' in line:
            return inst.parse_piped_line(line)
        ```
        * In `CEF20_PER.parse_line` after `inst` is initiated, include the following check:
        ```Python
        if '|' in line:
            return inst.parse_piped_line(line)
        ```
    * `das_decennial/programs/s3cat.py`
        * Replace this file with the version in `census2020-das-e2e/s3cat.py` which allows for concatenation of files on the local disk
    * `das_decennial/programs/writer/mdf2020writer.py`
        * In `MDF2020Writer.saveHeader` change `with s3open(path, "w", fsync=True) as f:` to `with open(path, "w") as f:`
        * In `MDF2020Writer.saveRDD` change `df.write.csv(path, sep="|")` to `df.write.csv(path, sep="|", mode="overwrite")`
    * `das_decennial/programs/writer/writer.py`
        * In `DASDecennialWriter.saveMetadata` change `with s3open(path, "w", fsync=True) as f:` to `with open(path, "w") as f:`
        * In `DASDecennialWriter.saveRunData` change the `s3cat` function call to be the following line instead:
        ```
        s3cat.s3_cat(output_datafile_name)
        ```
* `das_framework` directory
    * `das_framework/certificate/__init__.py`
        * In `CertificatePrinter.typeset` change `shutil.rmtree(outdir)` to `os.system("rm -rf {}".format(outdir))` due to a bug in `shutil.rmtree` on some linux systems
    * `das_framework/driver.py`
        * In `_DAS.annotate` change the method body to only contain the following (should only have the code inside the `if verbose:` check left):
        ```Python
        when  = time.asctime()[11:16]
        whent = round(self.running_time(),2)
        print(f"ANNOTATE: {when} t={whent} {message}")
        ```
        * In `main_setup`, change the `clogging.setup` call to be the following (basically deactivate the syslog parameters):
        ```Python
        clogging.setup(args.loglevel,
                       syslog=False,
                       filename=args.logfilename)
        ```
* `ctools` directory
    * `ctools/aws.py`
        * Comment out the `boto3` import
    * `ctools/ec2.py`
        * Comment out the `boto3` import
    * `ctools/s3.py`
        * Comment out the `boto3`, `botocore`, and `botocore.exceptions` imports

# Project and DAS Configuration
There is some configuration both for how the project runs and for how the DAS runs.  

## Project Configuration
The file `das_container.conf` contains some variables that can be configured to tweak how the container runs. Currently there options are:

* `das_home` - For configuring the home directory the container uses, see the project README for more information about how to use this variable.
* `container_tmp` - The temporary directory the container uses, the project README has a bit more information about this variable as well.
* `coord_hostname` - The hostname for the coordinator when running in cluster mode, see the README in the `cluster` project directory for instructions for setting up the DAS in cluster mode.
* `config_file` - The configuration file used by the DAS, see below for more information on this.

This file's purpose is solely for configuring parameters used to get the DAS running in the container. Once the DAS is running, you should use the DAS config file to modify parameters related to its computations.

## DAS Configuration
The DAS has many parameters that can be configured for how it runs its privacy algorithms. There isn't a ton of documentation as to what each of these parameters do and what combinations of parameters are valid. `das_decennial/configs/` is a directory with some example config files for the production release of the DAS.

`configs/basic_cef.ini` (note that this is a different directory than `das_decennial/configs/`) has a configuration that was working for a container run of the DAS. It mostly borrows from the given production config examples w/a few modifications needed for running outside of the AWS environment.

# Synthetic Population Scripts
`util/convert_synth_pop.py` was added to convert synthetic population files into a format that can be used with the DAS.

## Converting
Abie has a way to generate synthetic population files for different areas of the country. The purpose of `util/convert_synth_pop.py` is to convert these into a person and unit file that is in valid format for the DAS.

The main part of the process is fairly straightforward, though the details still could use some work. Essentially the script uses the information in the original file to populate the appropriate attributes in the DAS file. It uses a household id attribute to determine households, and then builds a unit file from the household information.

It has been a little bit difficult getting information on what each of the DAS attributes are, and some of the information contradicts what the code allows. Here are some resources that were used to help determine what attributes mean and what format they should be in, though we have not yet figured things out for every attribute:

* [Document w/MDF code specifications](https://github.com/uscensusbureau/census2020-das-2010ddp/blob/master/doc/2010-Demonstration-Data-Products-Disclosure-Avoidance-System-Design-Specification%20FINAL.pdf) - Document with information specific to the MDF/CEF specifications for the DAS. Not all of the specifications tell us what values mean what for a given attribute.
* [Document w/various other code specifications](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2019.pdf) - Used this to determine relationship codes, very well may have some other information we are missing but a bit hard to search because the attribute names don't match the ones used in the DAS.
* `das_decennial/programs/reader/cef_2020/cef_validator_classes.py` - contains code for validating the person and unit files. There is a little bit of information about what each attribute is (though not what each value represents) and what formats are valid for each attribute. Some of this information contradicts what is given in other writeups (e.g. some attributes have 0 as a documented value but the validator doesn't allow 0 for that same attribute).

## Lingering Issues
There are still some unknown attributes and inconsistencies with the validator classes. A few `TODO`s in the script mark specific places where we either have unknown attributes or the script could be improved in some way.

The most important lingering issues for experiments are likely:
* Householder/group quarter logic - There is still some safety logic for determining householders and for group quarters that should probably be removed at some point. Specifically, see the `TODO`s in the functions `get_head_of_household`, `get_hht2`, `get_hhspan`, and `get_hhrace`.
