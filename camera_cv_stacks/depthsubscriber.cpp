#include <ros/ros.h>
#include <iostream>
#include <image_transport/image_transport.h>
#include <sensor_msgs/image_encodings.h>  
#include <camera_info_manager/camera_info_manager.h>
#include <opencv2/opencv.hpp>
#include <cv_bridge/cv_bridge.h>
using namespace std;
using namespace cv;

static const std::string INPUT = "input";
static const std::string OUTPUT = "output";

void callbackFunc(int e, int x, int y, int f, void* p);
  
//定义一个转换的类  
class RGB_GRAY  
{  
private:  
    ros::NodeHandle nh_; //定义ROS句柄  
    image_transport::ImageTransport it_; //定义一个image_transport实例  
    image_transport::Subscriber depth_image_sub_; //定义ROS深度图象接收器  
    image_transport::Subscriber rgb_image_sub_; //定义ROS深度图象接收器 
    //image_transport::Publisher image_pub_; //定义ROS图象发布器  
public:  
    RGB_GRAY()  
      :it_(nh_) //构造函数  
    {  
        depth_image_sub_ = it_.subscribe("camera/depth_registered/image_raw", 1, &RGB_GRAY::depth_convert_callback, this); //定义图象接受器，订阅话题是“camera/rgb/image_raw”  
       // image_pub_ = it_.publishe("", 1); //定义图象发布器  
       //初始化显示窗口
	cv::namedWindow(OUTPUT);
	
         
    }  
    ~RGB_GRAY() //析构函数  
    {  
         cv::destroyWindow(INPUT);  
         cv::destroyWindow(OUTPUT);  
    }  
    /* 
      这是一个ROS和OpenCV的格式转换回调函数，将图象格式从sensor_msgs/Image  --->  cv::Mat 
    */  
    void depth_convert_callback(const sensor_msgs::ImageConstPtr& msg)   
    {  
        cv_bridge::CvImagePtr cv_ptr; // 声明一个CvImage指针的实例  
  
        try  
        {  
            cv_ptr =  cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_32FC1); //将ROS消息中的图象信息提取，生成新cv类型的图象，复制给CvImage指针,此处必须采用TYPE_32FC1格式
        }  
        catch(cv_bridge::Exception& e)  //异常处理  
        {  
            ROS_ERROR("cv_bridge exception: %s", e.what());  
            return;  
        }  
  
        image_process(cv_ptr->image); //得到了cv::Mat类型的图象，在CvImage指针的image中，将结果传送给处理函数     
    }  
    /* 
       这是图象处理的主要函数，一般会把图像处理的主要程序写在这个函数中。这里的例子只是一个彩色图象到灰度图象的转化 
    */  

    
    void image_process(cv::Mat img)   
    {  
        Mat depthimg = img;
        imshow(OUTPUT,depthimg);
	    setMouseCallback(OUTPUT, callbackFunc,(void*)&depthimg);
        waitKey(1);
        
    }  
   
};  
//image_process的回调函数需要放在类的外面不然编译不通过
void callbackFunc(int e, int x, int y, int f, void* p)
    {
	Mat* frame = (Mat*)p;
        if (e == CV_EVENT_LBUTTONDOWN)
        {
	        cout << x << "," <<y << endl;
            cout << (*frame).at<float>(x,y) << endl;
        }
    }
  
//主函数  
int main(int argc, char** argv)  
{  
    ros::init(argc, argv, "RGB");  
    RGB_GRAY obj;  
    ros::spin();  
}  
