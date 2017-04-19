#include "opencv2/opencv.hpp"
#include <math.h>   
using namespace cv;
using namespace std;
SimpleBlobDetector detector;

float euclideanDist(float point1[], float point2[]);

int main(int, char**)
{
    VideoCapture cap(0); // open the default camera
    if(!cap.isOpened())  // check if we succeeded
        return -1;

    Mat edges;
    std::vector<KeyPoint> keypoints;
    std::vector<KeyPoint> keypoints2;
    /*float gh[3];
    gh[0]=1;
    cout << (sizeof(gh)/sizeof(*gh));*/
    namedWindow("edges",1);
    for(int i=0;i<300;i++)
    {
        Mat frame;
        Mat im;
        cap >> frame; // get a new frame from camera
        cvtColor(frame, im, CV_BGR2GRAY);
        detector.detect( im, keypoints);
        Mat im_with_keypoints;
        
        for(int i=0; i<keypoints.size(); i++)
        {    
            if(keypoints[i].size>15)
            {
                //cout << keypoints[i].size << "\n";
                cv::KeyPoint s= keypoints.at(i);
                keypoints2.push_back(s);
            }
        }
        drawKeypoints( im, keypoints, im_with_keypoints, Scalar(0,0,255), DrawMatchesFlags::DRAW_RICH_KEYPOINTS );
        imshow("keypoints", im_with_keypoints );
        waitKey(1);
        
        
    }
    float a[]={0,0};
    float b[]={1,1};
    float result=euclideanDist(a,b);
    cout << result;
    
    
        
    // the camera will be deinitialized automatically in VideoCapture destructor
    return 0;
}

float euclideanDist(float point1[], float point2[])
{
    int length=(sizeof(point1)/sizeof(*point1));
    int temp=0;
    for(int i=0; i<length; i++)
    {
        temp+=(point1[i]-point2[i])*(point1[i]-point2[i]);
    }   
 
    return sqrt(temp); 
}
/*
float * findClosest(int i, int array[])
{
    int length=(sizeof(array)/sizeof(*array));
    if i==length
    {
        cout << "Error in closest";
        res[]={0,0};
        return res;
    }
    float closest;
    int closestInd;
    
}*/
