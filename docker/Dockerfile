# Docker file for Human Robot Interaction course
# ROS Melodic, Pepper tools
# Luca Iocchi, DIAG, Sapienza University of Rome, Italy
# Version 0.7

FROM ros:melodic-ros-base-bionic

ARG DEBIAN_FRONTEND=noninteractive
ARG NAOQI=notavailable

###### USER root ######

# install libraries and ros packages 

RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

RUN apt-get update && \
    apt-get install -y \
        tmux less sudo eom wget libwebsockets-dev \
        nano unzip wget iputils-ping net-tools netcat openssh-client \
        bash-completion python-pip \
        ros-melodic-desktop \
        ros-melodic-naoqi-libqi ros-melodic-naoqi-libqicore \
        ros-melodic-naoqi-driver ros-melodic-naoqi-bridge-msgs && \
    rm -rf /var/lib/apt/lists/*

# User: robot (password: robot) with sudo power

RUN useradd -ms /bin/bash robot && echo "robot:robot" | chpasswd && adduser robot sudo

# Pepper

RUN mkdir -p /opt/Aldebaran

#-- NAOqi SDK

COPY downloads/empty downloads/naoqi-sdk-2.5.5.5-linux64.tar.gz* /opt/Aldebaran/
COPY downloads/empty downloads/ctc-linux64-atom-2.5.2.74.zip* /opt/Aldebaran/
COPY downloads/empty downloads/pynaoqi-python2.7-2.5.5.5-linux64.tar.gz* /opt/Aldebaran/

RUN if [ "$NAOQI" = "OK" ]; then \
      cd /opt/Aldebaran && \
      rm empty && \
      tar xzvf naoqi-sdk-2.5.5.5-linux64.tar.gz && \
      tar xzvf pynaoqi-python2.7-2.5.5.5-linux64.tar.gz && \
      unzip ctc-linux64-atom-2.5.2.74.zip && \
      rm naoqi-sdk-2.5.5.5-linux64.tar.gz && \
      rm pynaoqi-python2.7-2.5.5.5-linux64.tar.gz && \
      rm ctc-linux64-atom-2.5.2.74.zip && \
      cd /opt/Aldebaran/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7 && \
      chmod go+rx site-packages; \
    fi

#-- Python SDK

ENV PYTHONPATH /opt/Aldebaran/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages

###### USER robot ######

USER robot

RUN touch ~/.sudo_as_admin_successful
RUN echo "set -g mouse on" > $HOME/.tmux.conf 

RUN mkdir -p $HOME/.config/pulse && \
    cd $HOME/.config/pulse && \
    ln -s /opt/config/pulse/cookie .

RUN pip install --user Pillow tornado==5.1.1 

### Init ROS workspace ###

RUN mkdir -p $HOME/ros/catkin_ws/src

RUN /bin/bash -c "source /opt/ros/melodic/setup.bash; cd $HOME/ros/catkin_ws/src; catkin_init_workspace; cd ..; catkin_make"

RUN echo "source $HOME/ros/catkin_ws/devel/setup.bash\n" >> $HOME/.bashrc

RUN rosdep update


### Additional packages ###

RUN mkdir -p $HOME/src/

# OpenCV
RUN pip install opencv-python==4.2.0.32

# qibullet
RUN pip install --user qibullet

# Pepper tools mounted from local host

VOLUME /home/robot/src/pepper_tools

ENV PEPPER_TOOLS_HOME /home/robot/src/pepper_tools

RUN echo "export PEPPER_IP=127.0.0.1\n" >> $HOME/.bashrc

# Compile ROS packages

RUN /bin/bash -c "source $HOME/ros/catkin_ws/devel/setup.bash; cd $HOME/ros/catkin_ws; catkin_make"

ADD init.bash /home/robot/init.bash

# Set working dir and container command

WORKDIR /home/robot

CMD [ "bash", "-ci", "/home/robot/init.bash" ]


