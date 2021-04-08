# user manual

1. create a package in your workspace

    `catkin_create_pkg cup_detection sensor_msgs cv_bridge roscpp std_msgs image_transport`

2. download my file

    `git clone https://github.com/Louis208908/cup.git`

3. paste the following code into CMakeList.txt

    `find_package(OpenCV)`    
    
    `include_directories(${OpenCV_INCLUDE_DIRS})`
    
    `add_executable(cupDetect src/cupDetect.cpp)`
    
    `target_link_libraries(cupDetect ${catkin_LIBRARIES} ${OpenCV_LIBRARIES})`

    `add_executable(listener src/listener.cpp)`
    
    `target_link_libraries(listener ${catkin_LIBRARIES} ${OpenCV_LIBRARIES})`

4. move "cupDetect.cpp" and "listener.cpp" into src under the package aforementioned

5. build and compile for your workspace

    `catkin_make`