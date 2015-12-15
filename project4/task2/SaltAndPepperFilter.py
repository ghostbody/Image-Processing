import cv2
import Filtering
import numpy as np

def arithmetic():
    img = cv2.imread("./3_SaltAndPepperNoise.png", 0)
    img_filter = [[1 for j in range(5)] for i in range(5)]
    new_img = Filtering.filter2d(img, img_filter, "arithmetic")
    cv2.imwrite("3_SaltAndPepperNoise_arithmetic.png", new_img)

def geometric():
    img = cv2.imread("./3_SaltAndPepperNoise.png", 0)
    img_filter = [[1 for j in xrange(3)]for i in xrange(3)]
    new_img = Filtering.filter2d(img, img_filter, "geometric")
    cv2.imwrite("3_SaltAndPepperNoise_geometric.png", new_img)

def Max():
    img = cv2.imread("./3_SaltAndPepperNoise.png", 0)
    img_filter = [[1 for j in xrange(3)]for i in xrange(3)]
    new_img = Filtering.filter2d(img, img_filter, "max")
    cv2.imwrite("3_SaltAndPepperNoise_max.png", new_img)

def Min():
    img = cv2.imread("./3_SaltAndPepperNoise.png", 0)
    img_filter = [[1 for j in xrange(3)]for i in xrange(3)]
    new_img = Filtering.filter2d(img, img_filter, "min")
    cv2.imwrite("3_SaltAndPepperNoise_min.png", new_img)

def median():
    img = cv2.imread("./3_SaltAndPepperNoise.png", 0)
    img_filter = [[1 for j in range(5)] for i in range(5)]
    new_img = Filtering.filter2d(img, img_filter, "median")
    cv2.imwrite("3_SaltAndPepperNoise_median.png", new_img)

def main():
    #arithmetic()
    geometric()
    Max()
    Min()
    #median()

if __name__ == '__main__':
    main()
