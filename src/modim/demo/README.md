# MODIM demo example

This folder contains a demo example.

A demo must contain the following elements:

* `init`: file describing the default GUI configuration when the robot is not interacting with a person.
* `lang_instance`: file describing the possible languages available for the demo. Images of the flags must be included in the img folder.
* `index.html` (+ possible other HTML files): layout files
* `img`: folder containing images
* `actions`: folder containing specification of MODIM action
* `grammars`: folder containing the grammar files used in the demo. 
* `scripts`: folder containing interaction scripts

The .xml and .grxml files can be automatically generated from a .txt file using the grammar generator.
The file associates each recognized word with a keyword or label that must be sent to PNP.


# Create a new application

Create a `newdemo` folder for MODIM files with the structure described above
(or copy the example in `modim/demo/sample`)

Example:

    mkdir -p $HOME/playground
    cd $HOME/playground
    cp -a $MODIM_HOME/demo/sample .
    mv sample newdemo

Set the environment variable `MODIM_APP` to your `newdemo` folder

Example:

    export MODIM_APP=$HOME/playground/newdemo


Write your new MODIM application in the `newdemo` folder 





# Run the new application

## Docker version

Start the server with `docker-compose up` as described above.

Run the new application launching your new demo script

Example:

    docker exec -it modim bash -ci "cd \$MODIM_APP/scripts && python newdemo.py"




## Local execution (without web server)

Run the server

    cd $MODIM_HOME/src/GUI
    python ws_server.py [-robot pepper|marrtino]

Open a browser at

    $MODIM_HOME/demo/sample/index.html

Check connection (`OK` in green in the top right)

Set `MODIM_IP` environment variable to `127.0.0.1` or `localhost`

Run the interaction script

    cd $MODIM_HOME/demo/sample/scripts
    python demo1.py



## Client - Server Mode


**Server side**

Copy (or link) the demo folder into a space accessible from the web server

Run MODIM server

    cd $MODIM_HOME/src/GUI
    python ws_server.py [-robot pepper|marrtino]

Note: for using on Pepper, set environment variable PEPPER_IP to the IP of the robot.
When running the MODIM server on the robot (suggested option), use `127.0.0.1`.


**Web Client side**

Run a browser to open the URL

    http://<server_machine>/<path>/sample/index.html

Note: for using Pepper's tablet as screen, use 

    tablet_service.showWebview("http://192.18.0.1/apps/<your_app>/<your_demo>/index.html

Check connection (`OK` in green in the top)


**Script client side**

If MODIM client and server are on the the same host, just run the script

    cd $MODIM_HOME/demo/sample/scripts
    python demo1.py

If MODIM client is on a different machine of MODIM server, 
you need to set `MODIM_IP` environment variable to MODIM server and specify the absolute path of the files to be reached by the server

    cd $MODIM_HOME/demo/sample/scripts
    python demo1.py <absolute_path_of_demo_files_on_server>


