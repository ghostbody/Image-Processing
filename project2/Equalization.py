# -*- coding:utf-8 -*-

import numpy as np
import cv2

def equalize_hist(img, mode="RGB"):
    height = len(img)
    width  = len(img[0])

    if mode == "RGB":
        hist = calculate_hist(img, "RGB")
    elif mode == "Gray":
        hist = calculate_hist(img, "Gray")

    fx = [0 for i in range(256)]

    for i in range(256):
        fx[i] = 255 * sum([hist[j] for j in range(i+1)]) / (width * height)

    new_img = np.zeros((height,width),np.uint8)

    for x in range(height):
        for y in range(width):
            if mode == "Gray":
                new_img[x, y] = fx[img[x, y]]
            elif mode == "RGB":
                new_img[x, y] = fx[img[x, y][0]]

    return new_img


def calculate_hist(img, mode):
    hist = [0 for i in range(256)]
    height = len(img)
    width  = len(img[0])
    
    for x in range(height):
        for y in range(width):
            if mode == "RGB":
                hist[img[x,y][0]] += 1
            elif mode == "Gray":
                hist[img[x,y]] += 1
    return hist

def get_hist_image(hist):
    img = np.zeros((256,256),np.uint8)

    r = max(hist)/255
    for i in range (0,256):
        hist[i] = hist[i]/r
        cv2.line(img,(i,255),(i,255-hist[i]),255)

    return img

if __name__ == '__main__':
    img = cv2.imread("./14.png")

    originHist = get_hist_image(calculate_hist(img, "RGB"))
    cv2.imwrite("originHist.png", originHist)

    outImage = equalize_hist(img)
    cv2.imwrite("outImage.png", outImage)

    newHist = get_hist_image(calculate_hist(outImage, "Gray"))
    cv2.imwrite("newHist.png", newHist)
