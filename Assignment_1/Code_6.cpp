#include <opencv2/opencv.hpp>
#include <opencv2/features2d.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main()
{
    // Load the two images from the assets directory
    Mat img1 = imread("assets/SSEFigure1.bmp");
    Mat img2 = imread("assets/SSEFigure2.bmp");

    // Check if the images were loaded successfully
    if (img1.empty() || img2.empty()) {
        return -1;
    }

    // Create an ORB (Oriented FAST and Rotated BRIEF) feature detector
    Ptr<Feature2D> orb = ORB::create();

    // Vectors to hold keypoints and descriptors for each image
    vector<KeyPoint> keypoints1, keypoints2;
    Mat descriptors1, descriptors2;

    // Detect keypoints and compute descriptors for the first image
    orb->detectAndCompute(img1, Mat(), keypoints1, descriptors1);

    // Detect keypoints and compute descriptors for the second image
    orb->detectAndCompute(img2, Mat(), keypoints2, descriptors2);

    // Create a Brute Force matcher using the Hamming distance metric
    BFMatcher matcher(NORM_HAMMING);
    vector<DMatch> matches;

    // Match descriptors between the two images
    matcher.match(descriptors1, descriptors2, matches);

    // Extract the matched keypoints from both images
    vector<Point2f> points1(matches.size()), points2(matches.size());
    for (size_t i = 0; i < matches.size(); ++i) {
        points1[i] = keypoints1[matches[i].queryIdx].pt;
        points2[i] = keypoints2[matches[i].trainIdx].pt;
    }

    // Use RANSAC to find the homography and filter out outlier matches
    vector<uchar> inliers_mask;
    Mat homography = findHomography(points1, points2, RANSAC, 3.0, inliers_mask);

    // Create a vector to store inliers (good matches)
    vector<DMatch> inliers;
    inliers.reserve(matches.size());
    for (size_t i = 0; i < inliers_mask.size(); ++i) {
        if (inliers_mask[i]) {
            inliers.push_back(matches[i]);
        }
    }

    // Draw the matches between the two images (only inliers)
    Mat result;
    drawMatches(img1, keypoints1, img2, keypoints2, inliers, result);

    // Display the result
    imshow("Result", result);
    waitKey(0);

    return 0;
}