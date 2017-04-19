using namespace std;
using namespace cv;
 
void CallBackFunc(int event, int x, int y, int flags, void* userdata)
{
    if  ( event == EVENT_LBUTTONDOWN )
    {
        cout << "Left button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;
    }
    else if  ( event == EVENT_RBUTTONDOWN )
    {
        cout << "Right button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;
    }
    else if  ( event == EVENT_MBUTTONDOWN )
    {
        cout << "Middle button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;
    }
    else if ( event == EVENT_MOUSEMOVE )
    {
        cout << "Mouse move over the window - position (" << x << ", " << y << ")" << endl;
    }    
}
 
int main()
{
    // Read image from file 
    Mat img = imread("lena.JPG");
 
    //if fail to read the image
    if ( img.empty() ) 
    { 
        cout << "Error loading the image" << endl;
        return -1; 
    }
 
    //Create a window
    namedWindow("ImageDisplay", 1);
 
    //set the callback function for any mouse event
    setMouseCallback("ImageDisplay", CallBackFunc, NULL);
 
    //show the image
    imshow("ImageDisplay", img);
 
    // Wait until user press some key
    waitKey(0);
 
    return 0;
 
}
