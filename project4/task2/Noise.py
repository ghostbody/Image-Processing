# -*- coding:utf-8 -*-

import cv2
import numpy as np

# An easy to program approximate approach, that relies on the central limit
# theorem, is as follows: generate 12 uniform U(0,1) deviates, add them all up,
# and subtract 6 – the resulting random variable will have approximately
# standard normal distribution. In truth, the distribution will be Irwin–Hall,
# which is a 12-section eleventh-order polynomial approximation to the normal
# distribution. This random deviate will have a limited range of (−6, 6)
def generateGaussianNoise(mean, deviation):
    theSum = 0
    for i in xrange(12):
        theSum += np.random.random()
    return int(mean + deviation * (theSum - 6))

def generateSaltAndPepperNoise(Salt, Pepper):
    x = np.random.random()
    if 0 < x <= Salt:
        return 255
    elif x > Salt and x < (Salt+Pepper):
        return -255
    else:
        return 0

def addGaussianNoise(img):
    height, width = img.shape
    new_img = np.zeros((height,width),np.int32)
    for x in xrange(height):
        for y in xrange(width):
            new_img[x, y] = img[x, y] + generateGaussianNoise(0, 40)
            if new_img[x, y] > 255:
                new_img[x, y] = 255;
            if new_img[x, y] < 0:
                new_img[x, y] = 0
    return new_img

def addSaltNoise(img):
    height, width = img.shape
    new_img = np.zeros((height,width),np.int32)
    for x in xrange(height):
        for y in xrange(width):
            new_img[x, y] = img[x, y] + generateSaltAndPepperNoise(0.1, 0)
            if new_img[x, y] > 255:
                new_img[x, y] = 255;
            if new_img[x, y] < 0:
                new_img[x, y] = 0
    return new_img

def addSaltAndPepperNoise(img):
    height, width = img.shape
    new_img = np.zeros((height,width),np.int32)
    for x in xrange(height):
        for y in xrange(width):
            new_img[x, y] = img[x, y] + generateSaltAndPepperNoise(0.1, 0.1)
            if new_img[x, y] > 255:
                new_img[x, y] = 255;
            if new_img[x, y] < 0:
                new_img[x, y] = 0
    return new_img

def Gaussian(img):
    NoiseImage = addGaussianNoise(img)
    cv2.imwrite("1_GaussianNoise.png", NoiseImage)

def Salt(img):
    NoiseImage = addSaltNoise(img)
    cv2.imwrite("2_SaltNoise.png", NoiseImage)

def SaltAndPepper(img):
    NoiseImage = addSaltAndPepperNoise(img)
    cv2.imwrite("3_SaltAndPepperNoise.png", NoiseImage)

def main():
    img = cv2.imread("./task_2.png", 0)
    Gaussian(img)
    Salt(img)
    SaltAndPepper(img)

if __name__ == '__main__':
    main()
