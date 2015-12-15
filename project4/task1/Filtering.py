
import numpy as np
import cv2

def filter2d(img, img_filter, method):
    height = len(img)
    width  = len(img[0])

    new_img = np.zeros((height,width),np.int32)

    for i in range(height):
        for j in range(width):
            new_img[i, j] = mean_filter(img, img_filter, i, j, method)

    return new_img

def mean_filter(img, img_filter, x, y, method):
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
        centre_gray_value1 = Convolution(img, img_filter, x, y, method, 2.5)
        centre_gray_value2 = Convolution(img, img_filter, x, y, method, 1.5)

        if centre_gray_value2 != 0:
            return int(float(centre_gray_value1) / centre_gray_value2)
        else:
            return 0

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

    return centre_gray_value


def arithmetic(img):
    arithmetic_mean_filter3 = [[1,1,1],[1,1,1],[1,1,1]]
    filtered_image1 = filter2d(img, arithmetic_mean_filter3, "arithmetic")
    cv2.imwrite("arithmetic_mean_filter3.png", filtered_image1)

    arithmetic_mean_filter9 = [[1 for j in range(9)] for i in range(9)]
    filtered_image2 = filter2d(img, arithmetic_mean_filter9, "arithmetic")
    cv2.imwrite("arithmetic_mean_filter9.png", filtered_image2)

def harmonic(img):
    harmonic_mean_filter3 = [[1,1,1],[1,1,1],[1,1,1]]
    filtered_image3 = filter2d(img, harmonic_mean_filter3, "harmonic")
    cv2.imwrite("harmonic_mean_filter3.png", filtered_image3)

    harmonic_mean_filter9 = [[1 for j in range(9)] for i in range(9)]
    filtered_image4 = filter2d(img, harmonic_mean_filter9, "harmonic")
    cv2.imwrite("harmonic_mean_filter9.png", filtered_image4)

def contraharmonic(img):
    contraharmonic_mean_filter3 = [[1,1,1],[1,1,1],[1,1,1]]
    filtered_image5 = filter2d(img, contraharmonic_mean_filter3, "contraharmonic")
    cv2.imwrite("contraharmonic_mean_filter3.png", filtered_image5)

    contraharmonic_mean_filter9 = [[1 for j in range(9)] for i in range(9)]
    filtered_image6 = filter2d(img, contraharmonic_mean_filter9, "contraharmonic")
    cv2.imwrite("contraharmonic_mean_filter9.png", filtered_image6)

def main():
        img = cv2.imread("./task_1.png", 0)
        # arithmetic(img);
        harmonic(img);
        # contraharmonic(img);


if __name__ == '__main__':
    main()
