# -*- coding:utf-8 -*-

import numpy as np
import cv2

def equalize_hist(img):
    height = len(img)
    width  = len(img[0])

    hist1, hist2, hist3 = calculate_hist(img)

    fx1 = [0 for i in range(256)]
    fx2 = [0 for i in range(256)]
    fx3 = [0 for i in range(256)]

    for i in range(256):
        fx1[i] = 255 * sum([hist1[j] for j in range(i+1)]) / (width * height)
        fx2[i] = 255 * sum([hist2[j] for j in range(i+1)]) / (width * height)
        fx3[i] = 255 * sum([hist3[j] for j in range(i+1)]) / (width * height)

    new_img = np.zeros((height,width, 3),np.uint8)

    for x in range(height):
        for y in range(width):
                new_img[x, y][0] = fx1[img[x, y][0]]
                new_img[x, y][1] = fx2[img[x, y][1]]
                new_img[x, y][2] = fx3[img[x, y][2]]

    return new_img


def calculate_hist(img):
    hist1 = [0 for i in range(256)]
    hist2 = [0 for i in range(256)]
    hist3 = [0 for i in range(256)]

    height = len(img)
    width  = len(img[0])
    
    for x in range(height):
        for y in range(width):
            hist1[img[x,y][0]] += 1
            hist2[img[x,y][1]] += 1
            hist3[img[x,y][2]] += 1

    return (hist1, hist2, hist3)

def get_hist_image(hist):
    img = np.zeros((256,256),np.uint8)

    r = max(hist)/255
    for i in range (0,256):
        hist[i] = hist[i]/r
        cv2.line(img,(i,255),(i,255-hist[i]),255)

    return img

if __name__ == '__main__':
    img = cv2.imread("./picimage.jpg")

    outImage = equalize_hist(img)
    cv2.imwrite("outImage.png", outImage)

