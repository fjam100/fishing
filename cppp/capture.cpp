#include "opencv2/opencv.hpp"

using namespace cv;

int main(int, char**)
{
    VideoCapture cap(0); // open the default camera
    if(!cap.isOpened())  // check if we succeeded
        return -1;

    Mat edges;
    namedWindow("edges",1);
    for(;;)
    {
        Mat frame;
        Mat hsv_image;
        Mat cdst;
        cap >> frame; // get a new frame from camera
        cvtColor(frame, edges, CV_BGR2HSV);
        cvtColor(frame, hsv_image, CV_BGR2HSV);
        Mat lower_red_hue_range;
	    Mat upper_red_hue_range;
	    inRange(hsv_image, cv::Scalar(0, 140, 140), cv::Scalar(15, 255, 255), lower_red_hue_range);
	    inRange(hsv_image, cv::Scalar(160, 100, 100), cv::Scalar(179, 255, 255), upper_red_hue_range);
	    Mat red_hue_image;
	    addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0, red_hue_image);
	    namedWindow("Threshold lower image", cv::WINDOW_AUTOSIZE);
	    imshow("Threshold lower image", lower_red_hue_range);
	    namedWindow("Threshold upper image", cv::WINDOW_AUTOSIZE);
	    imshow("Threshold upper image", upper_red_hue_range);
        GaussianBlur(lower_red_hue_range, edges, Size(7,7), 1.5, 1.5);
        Canny(edges, edges, 0, 30, 3);
        cvtColor(edges, cdst, CV_GRAY2BGR);
        imshow("edges", edges);
        vector<Vec4i> lines;
        HoughLinesP(edges, lines, 1, CV_PI/180, 100, 50, 10 );
        for( size_t i = 0; i < lines.size(); i++ )
        {
            Vec4i l = lines[i];
            line( cdst, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0,0,255), 3, CV_AA);
        }
        imshow("detected lines", cdst);
        waitKey(1);
        //if(waitKey(1) >= 0) break;
    }
    // the camera will be deinitialized automatically in VideoCapture destructor
    return 0;
}
