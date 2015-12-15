import cv2
import Filtering
import numpy as np

def geometric():
    img = cv2.imread("./1_GaussianNoise.png", 0)
    img_filter = [[1 for j in xrange(5)]for i in xrange(5)]
    new_img = Filtering.filter2d(img, img_filter, "geometric")
    cv2.imwrite("1_GaussianNoise_geometric.png", new_img)

def arithmetic():
    img = cv2.imread("./1_GaussianNoise.png", 0)
    img_filter = [[1 for j in range(5)] for i in range(5)]
    new_img = Filtering.filter2d(img, img_filter, "arithmetic")
    cv2.imwrite("1_GaussianNoise_arithmetic.png", new_img)

def median():
    img = cv2.imread("./1_GaussianNoise.png", 0)
    img_filter = [[1 for j in range(5)] for i in range(5)]
    new_img = Filtering.filter2d(img, img_filter, "median")
    cv2.imwrite("1_GaussianNoise_median.png", new_img)

def main():
    geometric()
    arithmetic()
    median()

if __name__ == '__main__':
    main()
