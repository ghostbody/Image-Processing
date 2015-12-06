import numpy as np
import cv2
from basic import *

def dft2d(img, flags):
    if flags == 1:
        return Fdft2d(img)
    elif flags == -1:
        res = np.conjugate(img)
        #return np.conjugate(Fdft2d(img))
        return np.conjugate(Fdft2d(img))

def Fdft2d(img):
    height = len(img)
    width = len(img[0])

    Fourier_img0 = np.zeros((height,width),np.complex256)

    # row Fourier transform
    for u in xrange(height):
        for v in xrange(width):
            for y in xrange(width):
                Fourier_img0[u, v] += img[u,y] * (np.exp(-1j*2*np.pi*(float(v*y)/width)))

    Fourier_img = np.zeros((height,width),np.complex256)

    # col Fourier transform
    for u in xrange(height):
        for v in xrange(width):
            for x in xrange(height):
                Fourier_img[u, v] += Fourier_img0[x, v] * (np.exp(-1j*2*np.pi*(float(u*x)/height)))

    return Fourier_img

def Fourier_Spectrum():
    img = cv2.imread("./14.png", 0)
    img = centralize(img)
    Fourier_img = dft2d(img, 1)
    Fourier_img = np.abs(Fourier_img)
    Fourier_img = Fourier_log(Fourier_img)
    Fourier_img = Fourier_scaling(Fourier_img, "linear")
    cv2.imwrite("Fourier.png", Fourier_img)

def Fourier_Inverse():
    img = cv2.imread("./14.png", 0)
    Fourier_img = dft2d(img, 1)
    origin_img = dft2d(Fourier_img, -1).real
    origin_img = Fourier_scaling(origin_img, "linear")
    origin_img = diolog_transform(origin_img)
    cv2.imwrite("InverseFourier.png", origin_img)

def main():
    Fourier_Spectrum()
    Fourier_Inverse()

if __name__ == '__main__':
    main()
