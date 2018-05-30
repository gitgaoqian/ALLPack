
#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <camera_info_manager/camera_info_manager.h>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cv_bridge/cv_bridge.h>
#include <sstream>
#include <boost/assign/list_of.hpp>

// Based on the ros tutorial on transforming opencv images to Image messages

int main(int argc, char** argv)
{
    ros::init(argc, argv, "image_publisher");
    ros::NodeHandle nh;//设置句柄
    ros::NodeHandle _nh("~"); // to get the private params
    image_transport::ImageTransport it(nh);
    image_transport::CameraPublisher pub_L = it.advertiseCamera("left/image_raw", 1);//使用的是CameraPublisher可以同时发布image和camera_info
    image_transport::CameraPublisher pub_R = it.advertiseCamera("right/image_raw", 1);
    // provider can be an url (e.g.: rtsp://10.0.0.1:554) or a number of device, (e.g.: 0 would be /dev/video0)
    std::string video_stream_provider;
    cv::VideoCapture cap;
    if (_nh.getParam("video_stream_provider", video_stream_provider)){
        ROS_INFO_STREAM("Resource video_stream_provider: " << video_stream_provider);
        // If we are given a string of 4 chars or less (I don't think we'll have more than 100 video devices connected)
        // treat is as a number and act accordingly so we open up the videoNUMBER device
        if (video_stream_provider.size() < 4){
            ROS_INFO_STREAM("Getting video from provider: /dev/video" << video_stream_provider);
            cap.open(atoi(video_stream_provider.c_str()));
        }
        else{
            ROS_INFO_STREAM("Getting video from provider: " << video_stream_provider);
            cap.open(video_stream_provider);
        }
    }
    else{
        ROS_ERROR("Failed to get param 'video_stream_provider'");
        return -1;
    }
    //下面进行了参数设置,这些参数在参数服务器中都存在,而关于添加参数到参数服务器是在launch文件中进行的
    std::string camera_name_L,camera_name_R;
    _nh.param("camera_name_L", camera_name_L, std::string("camera_L"));
    ROS_INFO_STREAM("Camera name: " << camera_name_L);
    _nh.param("camera_name_R", camera_name_R, std::string("camera_R"));
    ROS_INFO_STREAM("Camera name: " << camera_name_R);


    int fps;
    _nh.param("fps", fps, 240);
    ROS_INFO_STREAM("Throttling to fps: " << fps);

    std::string frame_id;//相机tf中的坐标系名称
    _nh.param("frame_id", frame_id, std::string("camera"));
    ROS_INFO_STREAM("Publishing with frame_id: " << frame_id);

    std::string camera_info_url_L,camera_info_url_R;//camera_info_manager中加载相机参数必须的参数
    _nh.param("camera_info_url_L", camera_info_url_L, std::string(""));
    ROS_INFO_STREAM("Provided camera_info_url_L: '" << camera_info_url_L << "'");
    _nh.param("camera_info_url_R", camera_info_url_R, std::string(""));
    ROS_INFO_STREAM("Provided camera_info_url_R: '" << camera_info_url_R << "'");


    bool flip_horizontal;
    _nh.param("flip_horizontal", flip_horizontal, false);
    ROS_INFO_STREAM("Flip horizontal image is: " << ((flip_horizontal)?"true":"false"));

    bool flip_vertical;
    _nh.param("flip_vertical", flip_vertical, false);
    ROS_INFO_STREAM("Flip vertical image is: " << ((flip_vertical)?"true":"false"));

    int width_target;
    int height_target;
    _nh.param("width", width_target, 0);
    _nh.param("height", height_target, 0);
    if (width_target != 0 && height_target != 0){
        ROS_INFO_STREAM("Forced image width is: " << width_target);
        ROS_INFO_STREAM("Forced image height is: " << height_target);
    }

    // From http://docs.opencv.org/modules/core/doc/operations_on_arrays.html#void flip(InputArray src, OutputArray dst, int flipCode)
    // FLIP_HORIZONTAL == 1, FLIP_VERTICAL == 0 or FLIP_BOTH == -1
    bool flip_image = true;
    int flip_value;
    if (flip_horizontal && flip_vertical)
        flip_value = 0; // flip both, horizontal and vertical
    else if (flip_horizontal)
        flip_value = 1;
    else if (flip_vertical)
        flip_value = -1;
    else
        flip_image = false;

    if(!cap.isOpened()){
        ROS_ERROR_STREAM("Could not open the stream.");
        return -1;
    }
    if (width_target != 0 && height_target != 0){
        cap.set(CV_CAP_PROP_FRAME_WIDTH, width_target);
        cap.set(CV_CAP_PROP_FRAME_HEIGHT, height_target);
    }


    ROS_INFO_STREAM("Opened the stream, starting to publish.");

    cv::Mat frame,frame_L,frame_R;
    sensor_msgs::ImagePtr msg_L;//一定是指针格式的:ImagePtr
    sensor_msgs::ImagePtr msg_R;
    sensor_msgs::CameraInfo cam_info_msg_L;
    sensor_msgs::CameraInfo cam_info_msg_R;
    std_msgs::Header header;
    header.frame_id = frame_id;
    camera_info_manager::CameraInfoManager cam_info_manager_L(nh, camera_name_L, camera_info_url_L);//使用camerainfomanaget加载相机参数(需要正确的camera_name 和 camera_info_url)
    camera_info_manager::CameraInfoManager cam_info_manager_R(nh, camera_name_R, camera_info_url_R);
    // Get the saved camera info if any
    cam_info_msg_L = cam_info_manager_L.getCameraInfo();//将获取的相机参数赋给cam_info_msg
    cam_info_msg_R = cam_info_manager_R.getCameraInfo();
    ros::Rate r(fps);
    while (nh.ok()) {
        cap >> frame;
        frame_L = frame.rowRange(0, 480).colRange(0, 640);
        frame_R = frame.rowRange(0, 480).colRange(640, 1280);
        if (pub_L.getNumSubscribers() > 0){
            // Check if grabbed frame is actually full with some content
            if(!frame.empty()) {
                // Flip the image if necessary
                if (flip_image)
                    cv::flip(frame, frame, flip_value);
                msg_L = cv_bridge::CvImage(header, "bgr8", frame_L).toImageMsg();//opencv格式转换到ros格式
                msg_R = cv_bridge::CvImage(header, "bgr8", frame_R).toImageMsg();
                // The timestamps are in sync thanks to this publisher
                pub_L.publish(*msg_L, cam_info_msg_L);
                pub_R.publish(*msg_R, cam_info_msg_R);
            }   

            ros::spinOnce();
        }
        r.sleep();
    }
}
