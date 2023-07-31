/**
 *
 * This example demonstrates how to get images from the robot remotely and how
 * to display them on your screen using opencv.
 *
 * Copyright Aldebaran Robotics
 */

// Opencv includes.
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

// Aldebaran includes.
#include <alproxies/alvideodeviceproxy.h>
#include <alvision/alimage.h>
#include <alvision/alvisiondefinitions.h>
#include <alerror/alerror.h>

// Boost includes.
#include <boost/program_options.hpp>

#include <iostream>
#include <string>
#include <chrono>
using namespace AL;

/**
* \brief Shows images retrieved from the robot.
*
* \param robotIp the IP adress of the robot
*/
void showImages(const std::string& robotIp, int port, std::string camera_type, bool use_gui, bool save_images)
{

  /** Create a proxy to ALVideoDevice on the robot.*/
  ALVideoDeviceProxy camProxy(robotIp, port);

  /** Subscribe a client image requiring 320*240 and BGR colorspace.*/
  std::string clientName = camera_type + std::to_string(std::chrono::steady_clock::now().time_since_epoch().count());
  //We need variable clientNames since the same name can be used just up to 6 times
  std::cerr << "Client name: " << clientName << std::endl;

  /** Create an cv::Mat header to wrap into an opencv image.*/
  cv::Mat imgHeader;
  if (camera_type != "kDepthCamera"){
    int camera_id = (camera_type == "kTopCamera")? 0 : 1;
    clientName = camProxy.subscribeCamera(clientName, camera_id, kQVGA, kBGRColorSpace, 30);
    imgHeader = cv::Mat(cv::Size(320, 240), CV_8UC3);
  }else {
    //camera_type == kDepthCamera
    int camera_id = 2;
    clientName = camProxy.subscribeCamera(clientName, 2, kQVGA, kDepthColorSpace, 30);
    imgHeader = cv::Mat(cv::Size(320, 240), CV_16UC1);
  }



  /** Create a OpenCV window to display the images. */
  if (use_gui)
    cv::namedWindow("images");

  /** Main loop. Exit when pressing ESC.*/
  while (true)
  {
    /** Retrieve an image from the camera.
    * The image is returned in the form of a container object, with the
    * following fields:
    * 0 = width
    * 1 = height
    * 2 = number of layers
    * 3 = colors space index (see alvisiondefinitions.h)
    * 4 = time stamp (seconds)
    * 5 = time stamp (micro seconds)
    * 6 = image buffer (size of width * height * number of layers)
    */
    ALValue img = camProxy.getImageRemote(clientName);

    /** Access the image buffer (6th field) and assign it to the opencv image
    * container. */
    imgHeader.data = (uchar*) img[6].GetBinary();

    /** Tells to ALVideoDevice that it can give back the image buffer to the
    * driver. Optional after a getImageRemote but MANDATORY after a getImageLocal.*/
    camProxy.releaseImage(clientName);

    if (save_images){
      char buf[1024];
      auto now = std::chrono::steady_clock::now().time_since_epoch();
      float timestamp = std::chrono::duration_cast<std::chrono::duration<float>>(now).count();
      sprintf(buf, "%s_%.5lf.png", camera_type.c_str(), timestamp);
      cv::imwrite(buf, imgHeader);

    }
    /** Display the iplImage on screen.*/
    if (use_gui){
      cv::imshow("images", imgHeader);
      cv::waitKey(30);
    }else {
      usleep(100000);
    }
    
  }

  /** Cleanup.*/
  camProxy.unsubscribe(clientName);
}



int main(int argc, char** argv)
{
  namespace po = boost::program_options;

  po::options_description description("Options");
  description.add_options()
    ("help", "Displays this help message")
    ("pip", po::value<std::string>()->default_value(std::getenv("PEPPER_IP")), "Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    ("pport", po::value<int>()->default_value(9559), "Naoqi port number.")
    ("use_gui", po::value<bool>()->default_value(false), "Visualize images. Not possible when running in Pepper.")
    ("save_images", po::value<bool>()->default_value(false), "Save images.")
    ("camera", po::value<std::string>()->default_value("kTopCamera"), "Camera to visualize. Choose from: kTopCamera, kBottomCamera, kDepthCamera")
    ;

  po::variables_map vm;
  po::store(po::parse_command_line(argc, argv, description), vm);
  po::notify(vm);
  
  // --help option
  if (vm.count("help")){ 
    std::cout << description << std::endl; 
    return 0; 
  } 

  const std::string pip = vm["pip"].as<std::string>();
  int pport = vm["pport"].as<int>();
  bool use_gui = vm["use_gui"].as<bool>();
  bool save_images = vm["save_images"].as<bool>();
  std::string camera = vm["camera"].as<std::string>();
  if (camera != "kTopCamera" and camera != "kBottomCamera" and camera != "kDepthCamera"){
    std::cerr << "Not a valid camera. Choose from: kTopCamera, kBottomCamera or kDepthCamera" << std::endl;
    exit(0);
  }
  
  showImages(pip, pport, camera, use_gui, save_images);
  
}

