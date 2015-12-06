import numpy as np
import cv2

def fft2d(img, flags):
    if flags == 1:
        return Ffft2d(img)
    elif flags == -1:
        res = np.conjugate(img)
        return np.conjugate(Ffft2d(img))

def Ffft2d(img):
    height = len(img)
    width = len(img[0])

    Fourier_img0 = np.zeros((height,width),np.complex256)

    for u in xrange(height):
        Fourier_img0[u] = np.array(fft(img[u]))
        # print "FFT processing Row %d" % u

    Fourier_img = np.zeros((height,width),np.complex256)
    for v in xrange(width):
        Fourier_img[:,v] = fft(Fourier_img0[:,v])
        # print "FFT processing COL %d" % v

    # np.transpose(Fourier_img)

    return Fourier_img

def fft(x):
    N = len(x)
    if N <= 1:
        return x
    elif N % 2 != 0:
        return DFT_slow(x)
        print "slow DFT applied"
    else:
        even = fft(x[::2])
        odd = fft(x[1::2])
        return np.concatenate([[even[k] + np.exp(-2j*np.pi*k/N)*odd[k] for k in xrange(len(even))]
             ,[even[k] - np.exp(-2j*np.pi*k/N)*odd[k] for k in xrange(len(even))]])

def DFT_slow(x):
    Fourier_img = np.zeros((len(x)), np.complex256)

    for i in xrange(len(x)):
        for j in xrange(len(x)):
            Fourier_img[i] += x[j] * (np.exp(-1j*2*np.pi*(float(i*j)/len(x))))

    return Fourier_img


def Fourier_log(img):
    height = len(img)
    width = len(img[0])

    Fourier_log_img = np.zeros((height,width), np.float64)

    for u in xrange(height):
        for v in xrange(width):
            if img[u, v] > 0:
                Fourier_log_img[u, v] = np.log(img[u, v])

    return Fourier_log_img

def Fourier_scaling(img):
    height = len(img)
    width = len(img[0])
    res_img = np.zeros((height,width),np.int32)

    max_pixel = np.amax(img)
    min_pixel = np.amin(img)

    print max_pixel, min_pixel

    contantC = 255.0 / np.log10(256)

    for u in xrange(height):
        for v in xrange(width):
            res_img[u, v] = int((img[u, v] - min_pixel) / (max_pixel - min_pixel) * 255)
            #res_img[u, v] = int(contantC * np.log10(1 + np.abs(float(255*img[u, v]) / max_pixel)))
            if res_img[u, v] > 255:
                res_img[u, v] = 255

    return res_img

def centralize(img):
    height = len(img)
    width = len(img[0])

    res_img = np.zeros((height,width),np.float64)

    for x in xrange(height):
        for y in xrange(width):
            if (x + y) % 2 != 0:
                res_img[x, y] = -1 * img[x, y]
            else:
                res_img[x, y] = img[x,y]

    return res_img

def main():
    img = cv2.imread("./14.png", 0)
    # centered_img = centralize(img)
    # FFourier_img = fft2d(centered_img, 1)
    # FFourier_img = np.abs(FFourier_img)
    # FFourier_img = Fourier_log(FFourier_img)
    # FFourier_img = Fourier_scaling(FFourier_img)
    # cv2.imwrite("FFourier_test.png", FFourier_img)
    FFourier_img = fft2d(img, 1)
    origin_img = fft2d(FFourier_img, -1)
    origin_img = np.abs(origin_img)
    origin_img = Fourier_scaling(origin_img)
    origin_img = diolog_transform(origin_img)
    cv2.imwrite("IFFourier_img.png", origin_img)

if __name__ == "__main__":
    main()
