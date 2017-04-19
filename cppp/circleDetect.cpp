#include "opencv2/opencv.hpp"
#include <iostream>
#include <fstream>
#include <termios.h>

using namespace cv;
using namespace std;

int main(int, char**)
{
    ofstream outFile  ("example.csv");
    const char *device = "/dev/ttyACM0";
    fd = open(device, O_RDWR | O_NOCTTY | O_NDELAY);
    if(fd == -1) {
      printf( "failed to open port\n" );
    }
           
    VideoCapture cap(0); // open the default camera
    if(!cap.isOpened())  // check if we succeeded
        return -1;

    Mat edges;
    namedWindow("edges",1);
    for(int i=1;i<300;i++)
    {
        Mat src, src_gray;
        cap >> src; // get a new frame from camera
        cvtColor( src, src_gray, CV_BGR2GRAY );

        /// Reduce the noise so we avoid false circle detection
        GaussianBlur( src_gray, src_gray, Size(9, 9), 2, 2 );

        vector<Vec3f> circles;

        /// Apply the Hough Transform to find the circles
        HoughCircles( src_gray, circles, CV_HOUGH_GRADIENT, 1.2, src_gray.rows/8, 200, 100, 0, 0 );

        /// Draw the circles detected
        for( size_t i = 0; i < circles.size(); i++ )
        {
          Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
          int radius = cvRound(circles[i][2]);
          // circle center
          circle( src, center, 3, Scalar(0,255,0), -1, 8, 0 );
          outFile << center.x;
          outFile << ",";
          outFile << center.y;
          outFile << "\n";
          // circle outline
          circle( src, center, radius, Scalar(0,0,255), 3, 8, 0 );
        }

        /// Show your results
        namedWindow( "Hough Circle Transform Demo", CV_WINDOW_AUTOSIZE );
        imshow( "Hough Circle Transform Demo", src );
        waitKey(1);
  
    }
    
    outFile.close();
    // the camera will be deinitialized automatically in VideoCapture destructor
    return 0;
}
