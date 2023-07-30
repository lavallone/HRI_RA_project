# MODIM: Multi-modal Interaction Manager #

The repository is organized in different folders:

* `src`. source files
* `demo`. a ready-to-use demonstration
* `doc`. the user-guide
* `docker`. docker files and scripts


# Install

Install `docker` and `docker-compose`.

Download this repository in any directory (default `$HOME/src`)

Set environment variables

    export MODIM_HOME=<modim_directory>
    export MODIM_APP=<modim_directory>/demo/sample

Note: add these lines in `.bashrc` and open a new terminal.

Build the docker image in `docker` folder

    cd $MODIM_HOME/modim/docker
    ./build.bash

or pull the image from `dockerhub`

    docker pull iocchi/modim


# Run the sample application

Run the docker containers

    cd $MODIM_HOME/docker
    docker-compose up

Open a browser at URL

    http://<localhost or IP_address>/

Example:

    http://localhost/


You should read `OK` in green in the top right of the browser window
The web client is now connected to the MODIM server.


Run the demo

    docker exec -it modim bash -ci "cd \$MODIM_APP/scripts && python demo1.py"

The `Start` button appears in the browser window and you can start interaction.


To shutdown the containers, use `CTRL-c` in the terminal where `docker-compose` command was issued or use:

    cd $MODIM_HOME/docker
    docker-compose down


# Create a new MODIM app

To create a new MODIM application, see the `README` file in the `demo` folder.

