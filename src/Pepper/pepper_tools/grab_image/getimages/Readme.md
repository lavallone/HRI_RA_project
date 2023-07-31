# How to compile
**OpenCV** library within **NAOqi C++ SDK** is not ready to use visualization functions such as ```cv::namedWindow``` or ```cv::imshow```.  
For this reason, you have to replace the **OpenCV** libraries in **NAOqi C++ SDK** by another version of the libraries in which these functions are implemented.  
The **OpenCV** version of **NAOqi C++ SDK 2.5.5** is 2.4.9.
## Instructions
### Preparation to compile with OpenCV
* Remove **OpenCV** libraries from the NAOqi C++ SDK:
```
$ cd <path-to-your-naoqi-c++-sdk>/lib
$ sudo rm -rf libopencv_*
```
* Download **OpenCV 2.4.9** and extract it.
https://sourceforge.net/projects/opencvlibrary/files/opencv-unix/2.4.9/
* Compile **OpenCV 2.4.9** from source. The flag D_GLIBCXX_USE_CXX11_ABI=0 must be used for compatibility with **qibuild** and **NAOqi**.
```
$ cd <path-to-your-opencv-2.4.9>
$ mkdir build && cd build
$ CXXFLAGS="-D_GLIBCXX_USE_CXX11_ABI=0" cmake ..
$ make
```
* Copy the compiled libraries 
```
$ cd <path-to-your-naoqi-c++-sdk>/lib
$ sudo cp <path-to-your-opencv-2.4.9>/build/lib/libopencv_* .
```
### Compile getimages
From the getimages folder (assuming qibuild environment set up accordingly)
```
$ qibuild configure -c linux64
$ qibuild make -c linux64
```
