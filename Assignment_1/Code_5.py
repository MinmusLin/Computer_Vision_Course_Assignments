import cv2
import numpy as np
import sys

# Extract keypoints and descriptors using SIFT
def extract_features(image):
    detector = cv2.SIFT_create()
    (keypoints, descriptors) = detector.detectAndCompute(image, None)
    keypoints = np.float32([kp.pt for kp in keypoints])
    return keypoints, descriptors, detector

# Match features between two sets of keypoints and descriptors
def match_features(keys1, desc1, keys2, desc2):
    matcher = cv2.BFMatcher()
    knn_matches = matcher.knnMatch(desc1, desc2, 2)
    filtered_matches = []
    for pair in knn_matches:
        if len(pair) == 2 and pair[0].distance < pair[1].distance * 0.75:
            filtered_matches.append((pair[0].trainIdx, pair[0].queryIdx))
    if len(filtered_matches) > 4:
        points1 = np.float32([keys1[i] for (_, i) in filtered_matches])
        points2 = np.float32([keys2[i] for (i, _) in filtered_matches])
        homography, _ = cv2.findHomography(points1, points2, cv2.RANSAC, 4.0)
        return homography, filtered_matches
    return None, None

# Remove black borders from the final stitched image
def crop_black_borders(img):
    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_map = cv2.threshold(gray_scale, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_map, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, width, height = cv2.boundingRect(contours[0])
    cropped_img = img[y:y + height, x:x + width]
    return cropped_img

# Perform image stitching using feature matching and homography
def image_stitching(right_image, left_image):
    img1 = right_image.copy()
    img2 = left_image.copy()
    resized_img1 = cv2.resize(img1, (0, 0), fx=0.2, fy=0.2)
    resized_img2 = cv2.resize(img2, (0, 0), fx=0.2, fy=0.2)
    key_pts1, desc1, detector1 = extract_features(resized_img1)
    key_pts2, desc2, detector2 = extract_features(resized_img2)
    homography_matrix, matches = match_features(key_pts1, desc1, key_pts2, desc2)
    if homography_matrix is None:
        sys.exit()
    
    # Visualize detected keypoints
    keypoints_full1 = detector1.detect(resized_img1, None)
    keypoints_full2 = detector2.detect(resized_img2, None)
    img1_with_keypoints = cv2.drawKeypoints(resized_img1, keypoints_full1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    img2_with_keypoints = cv2.drawKeypoints(resized_img2, keypoints_full2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('Detected Keypoints - Image 1', img1_with_keypoints)
    cv2.imshow('Detected Keypoints - Image 2', img2_with_keypoints)
    
    # Visualize matches between images
    matches_drawing = [cv2.DMatch(m[1], m[0], 0) for m in matches]
    match_visual = cv2.drawMatches(resized_img1, keypoints_full1, resized_img2, keypoints_full2, matches_drawing, None)
    cv2.imshow('Matched Features', match_visual)
    
    # Apply homography to warp the images and combine them
    result_image = cv2.warpPerspective(resized_img1, homography_matrix, (resized_img1.shape[1] + resized_img2.shape[1], resized_img1.shape[0]))
    result_image[0:resized_img2.shape[0], 0:resized_img2.shape[1]] = resized_img2
    result_image = crop_black_borders(result_image)
    return result_image

if __name__ == '__main__':
    # Load images to be stitched
    right_side_img = cv2.imread('SSELeft.png')
    left_side_img = cv2.imread('SSERight.png')
    
    # Perform stitching and display the result
    final_result = image_stitching(right_side_img, left_side_img)
    cv2.imshow('Stitched Result', final_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()