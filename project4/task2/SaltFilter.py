import cv2
import Filtering
import numpy as np

def harmonic():
    img = cv2.imread("./2_SaltNoise.png", 0)
    img_filter = [[1 for j in xrange(3)]for i in xrange(3)]
    new_img = Filtering.filter2d(img, img_filter, "harmonic")
    cv2.imwrite("1_SaltNoise_harmonic.png", new_img)

def contraharmonic_Positive():
    img = cv2.imread("./2_SaltNoise.png", 0)
    img_filter = [[1 for j in xrange(3)]for i in xrange(3)]
    new_img = Filtering.filter2d(img, img_filter, "contraharmonic", 1.5)
    cv2.imwrite("1_SaltNoise_contraharmonic_positive.png", new_img)

def contraharmonic_Negative():
    img = cv2.imread("./2_SaltNoise.png", 0)
    img_filter = [[1 for j in xrange(3)]for i in xrange(3)]
    new_img = Filtering.filter2d(img, img_filter, "contraharmonic", -1.5)
    cv2.imwrite("1_SaltNoise_contraharmonic_negative.png", new_img)

def main():
    harmonic()
    contraharmonic_Positive()
    contraharmonic_Negative()

if __name__ == '__main__':
    main()
