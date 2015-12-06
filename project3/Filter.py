import cv2
import numpy as np

import FFT

def calculate_pow2(x):
    res = 2
    while res < x:
        res = res << 1
    return res

def filter2d_freq(img, the_filter):
    # FFT_image = FFT.centralize(img)
    # FFT_image = FFT.fft2d(img, 1)
    height = len(img)
    width = len(img[0])
    adjust_height = calculate_pow2(height)
    adjust_width  = calculate_pow2(width)

    FFT_filter = np.zeros((adjust_height,adjust_width), np.int32)
    adjust_img = np.zeros((adjust_height,adjust_width), np.int32)

    for x in xrange(height):
        for y in xrange(width):
            adjust_img[x, y] = img[x, y]

    for x in xrange(len(the_filter)):
        for y in xrange(len(the_filter[0])):
            FFT_filter[x, y] = the_filter[x, y]

    FFT_filter = FFT.centralize(FFT_filter)
    adjust_img = FFT.centralize(adjust_img)

    FFT_filter = FFT.fft2d(FFT_filter, 1)
    FFT_image = FFT.fft2d(adjust_img, 1)

    # FFT_filter = np.fft.fft2(FFT_filter)
    # FFT_image = np.fft.fft2(adjust_img)

    print "done Fourier transform"

    Result = FFT_image * FFT_filter

    print "done frequecy processing"

    Result = FFT.fft2d(Result, -1)
    # Result = np.fft.ifft2(Result)

    print "done Inverse Fourier transform"

    Result_img = np.zeros((height, width), np.float64)
    Result = np.abs(Result)

    Result = FFT.diolog_transform(Result)

    for x in xrange(height):
        for y in xrange(width):
            Result_img[x, y] = Result[x, y]

    Result_img = FFT.centralize(Result_img)
    Result_img = FFT.Fourier_scaling(Result_img)

    return Result_img

def main():
    # img = cv2.imread("./14.png", 0)
    # the_filter = np.array([[1 for i in xrange(7)] for i in xrange(7)])
    # Result = filter2d_freq(img, the_filter)
    # Result = gama_correction(Result, 7)

    # cv2.imwrite("Mean_Filtered_image.png", Result)
    img = cv2.imread("./14.png", 0)
    the_filter = np.array([[1,1,1],[1,-8,1],[1,1,1]])
    Result = filter2d_freq(img, the_filter)

    Result += img


    print Result

    Result = FFT.Fourier_scaling(Result)
    cv2.imwrite("Laplacian_Filtered_image.png", Result)

if __name__ == '__main__':
    main()
