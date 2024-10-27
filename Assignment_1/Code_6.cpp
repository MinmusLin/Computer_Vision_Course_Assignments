#include <opencv2/opencv.hpp>
#include <opencv2/features2d.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main()
{
    Mat img1 = imread("SSEFigure1.bmp");
    Mat img2 = imread("SSEFigure2.bmp");
    if (img1.empty() || img2.empty()) {
        return -1;
    }
    Ptr<Feature2D> orb = ORB::create();
    vector<KeyPoint> keypoints1, keypoints2;
    Mat descriptors1, descriptors2;
    orb->detectAndCompute(img1, Mat(), keypoints1, descriptors1);
    orb->detectAndCompute(img2, Mat(), keypoints2, descriptors2);
    BFMatcher matcher(NORM_HAMMING);
    vector<DMatch> matches;
    matcher.match(descriptors1, descriptors2, matches);
    vector<Point2f> points1(matches.size()), points2(matches.size());
    for (size_t i = 0; i < matches.size(); ++i) {
        points1[i] = keypoints1[matches[i].queryIdx].pt;
        points2[i] = keypoints2[matches[i].trainIdx].pt;
    }
    vector<uchar> inliers_mask;
    Mat homography = findHomography(points1, points2, RANSAC, 3.0, inliers_mask);
    vector<DMatch> inliers;
    inliers.reserve(matches.size());
    for (size_t i = 0; i < inliers_mask.size(); ++i) {
        if (inliers_mask[i]) {
            inliers.push_back(matches[i]);
        }
    }
    Mat result;
    drawMatches(img1, keypoints1, img2, keypoints2, inliers, result);
    imshow("Result", result);
    waitKey(0);
    return 0;
}