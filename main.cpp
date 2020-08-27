#include <opencv2/opencv.hpp>
#include <iostream>
#include <cmath>

using namespace cv;
using namespace std;

void PreProcess(Mat &img, Mat &mask)//preprocessing to filter max. noise
{	

	Mat gray_image,image1,dst;
	cvtColor( img, gray_image, COLOR_BGR2GRAY );
    GaussianBlur(gray_image, image1, Size( 3, 3), 0, 0 );
	Laplacian( image1, dst, CV_8U );
	threshold(dst, mask, 7, 255, THRESH_BINARY);
}


void DetectCircle(Mat &img,Mat &mask)
{
	int u_s[100];
    int x_y[100][100];
    int res=0;
    int thickness=3;
    std::vector<std::vector<cv::Point> > contours;
	Mat contourImage(img.size(), CV_8UC3, Scalar(0,0,0));
    Scalar color( rand()&0, rand()&255, rand()&0 );
	findContours( mask, contours, RETR_TREE, CHAIN_APPROX_NONE );
	for (size_t idx = 0; idx < contours.size(); idx++) //looping through every contour in the image
	{	
		//calculating center
		Moments m = moments(contours[idx]);
		Point centerofmass(m.m10/m.m00, m.m01/m.m00);
 	    for (size_t j = 0; j< contours[idx].size(); j++ ) //looping through the co-ordinates of each contour
 	    {	
			//x and y coordinates of the point on the contour
			Point coord = contours[idx][j];
			//calculating distance from center(cx,cy) to the x and y coordinate aka radius if it's a circle
			int t = (centerofmass.x-coord.x)*(centerofmass.x-coord.x)+(centerofmass.y-coord.y)+(centerofmass.y-coord.y);
			int r = sqrt(t);
			u_s[idx] = r;
		}
		//finding the distinct values in the array
		int n = sizeof(u_s)/sizeof(u_s[0]);
		for (int i = 0; i < n; i++)
		{
			while (i < n - 1 && u_s[i] == u_s[i + 1])
			{
				i++;
			}
			res++;
			/*the value of r remains almost same for a circle whereas with other shapes it varies significantly
			the contour with minimum no. of distinct values(here hardcoded as <=4) of r (radius) is a circle!*/
			if (res <= 4)
			//drawing the contour
			drawContours(img, contours, idx, color,thickness);
		}; 
    }
 
}


int main()
{
    Mat img(cv::imread("input2.jpg"));
	Mat mask;
	PreProcess(img,mask);
	DetectCircle(img,mask);
    imwrite("output.jpg", img);
}

