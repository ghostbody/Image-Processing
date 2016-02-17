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

def equalize_hist_average(img):
    height = len(img)
    width  = len(img[0])

    hist1, hist2, hist3 = calculate_hist(img)
    hist_average = average_hist(hist1, hist2, hist3)

    fx = [0 for i in range(256)]

    for i in range(256):
        fx[i] = 255 * sum([hist_average[j] for j in range(i+1)]) / (width * height)

    new_img = np.zeros((height, width, 3),np.uint8)

    for x in range(height):
        for y in range(width):
                new_img[x, y][0] = fx[img[x, y][0]]
                new_img[x, y][1] = fx[img[x, y][1]]
                new_img[x, y][2] = fx[img[x, y][2]]

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

def average_hist(hist1, hist2, hist3):
    hist_average = [0 for i in range(256)]
    for i in range(256):
        hist_average[i] = hist1[i] + hist2[i] + hist3[i]
        hist_average[i] /= 3
    return hist_average

def get_hist_image(hist):
    img = np.zeros((256,256),np.uint8)
    r = max(hist)/255
    for i in range (0,256):
        hist[i] = hist[i]/r
        cv2.line(img,(i,255),(i,255-hist[i]),255)
    return img

if __name__ == '__main__':
    img = cv2.imread("./14.png")

    output1 = equalize_hist(img)
    cv2.imwrite("output1.png", output1)

    hist1, hist2, hist3 = calculate_hist(img)
    hist_average = average_hist(hist1, hist2, hist3)
    origin_hist1 = get_hist_image(hist1)
    cv2.imwrite("origin_hist1.png", origin_hist1)
    origin_hist2 = get_hist_image(hist2)
    cv2.imwrite("origin_hist2.png", origin_hist2)
    origin_hist3 = get_hist_image(hist3)
    cv2.imwrite("origin_hist3.png", origin_hist3)
    average_hist_img = get_hist_image(hist_average)
    cv2.imwrite("average_hist.png", average_hist_img)

    output2 = equalize_hist_average(img)
    cv2.imwrite("output2.png", output2)
