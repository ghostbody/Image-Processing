
import numpy as np
import cv2

def filter2d(img, img_filter, method, q = 1):
    height = len(img)
    width  = len(img[0])

    new_img = np.zeros((height,width),np.int32)

    for i in range(height):
        for j in range(width):
            if method in ["median", "max", "min"]:
                new_img[i, j] = median_filter(img, img_filter, i, j, method)
            else:
                new_img[i, j] = mean_filter(img, img_filter, i, j, method, q)

    return new_img

def median_filter(img, img_filter, x, y, method):
    filter_size = len(img_filter[0])
    height = len(img)
    width  = len(img[0])

    array = np.zeros(filter_size**2, np.int32)
    factor = int(filter_size / 2)

    for i in range(filter_size):
        for j in range(filter_size):
            img_x = x - factor + i
            img_y = y - factor + j
            if (img_x < 0) or (img_x >= height) or (img_y < 0) \
                            or (img_y >= width):
                array[i*filter_size + j] = 0
            else:
                array[i*filter_size + j] = img[img_x, img_y]

    if method == "median":
        array.sort()
        if filter_size ** 2 % 2 == 0:
            return array[filter_size*filter_size / 2]
        else:
            return int(float(array[filter_size*filter_size / 2] \
            + array[filter_size * filter_size / 2 -1])/2)
    elif method == "max":
        return np.amax(array)
    elif method == "min":
        return np.amin(array)


def mean_filter(img, img_filter, x, y, method, q=1):
    filter_size = len(img_filter[0])
    if method == "arithmetic":
        centre_gray_value = Convolution(img, img_filter, x, y, method)
        return int(centre_gray_value / (filter_size**2))
    elif method == "harmonic":
        centre_gray_value = Convolution(img, img_filter, x, y, method)
        if centre_gray_value == 0:
            return 0
        return int(float(filter_size**2) / centre_gray_value)
    elif method == "contraharmonic":
        centre_gray_value1 = Convolution(img, img_filter, x, y, method, q+1)
        centre_gray_value2 = Convolution(img, img_filter, x, y, method, q)
        if centre_gray_value2 != 0:
            return int(float(centre_gray_value1) / centre_gray_value2)
        else:
            return 0
    elif method == "geometric":
        centre_gray_value = Convolution(img, img_filter, x, y, method)
        return centre_gray_value

def  Convolution(img, img_filter, x, y, method, q=1):
    height = len(img)
    width  = len(img[0])

    filter_size = len(img_filter[0])
    factor = int(filter_size / 2)

    centre_gray_value = 0

    for i in range(filter_size):
        for j in range(filter_size):
            img_x = x - factor + i
            img_y = y - factor + j
            # Zero Padding
            if (img_x < 0) or (img_x >= height) or (img_y < 0) \
                            or (img_y >= width):
                centre_gray_value += 0
            elif method == "arithmetic":
                centre_gray_value += (img[img_x, img_y] * img_filter[i][j])
            elif method == "harmonic":
                if img[img_x, img_y] == 0:
                    centre_gray_value += 1
                else:
                    centre_gray_value += 1.0 / (img[img_x, img_y] * img_filter[i][j])
            elif method == "contraharmonic":
                if img[img_x, img_y] == 0:
                    centre_gray_value += 1
                else:
                    centre_gray_value += (img[img_x, img_y] * img_filter[i][j]) ** q
            elif method == "geometric":
                if centre_gray_value == 0:
                    centre_gray_value = np.power(img[img_x, img_y], 1.0 / filter_size**2)
                else:
                    centre_gray_value *= np.power(img[img_x, img_y], 1.0 / filter_size**2)

    return centre_gray_value
