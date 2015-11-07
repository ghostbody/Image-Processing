
import numpy as np
import cv2
import Equalization

def filter2d(img, img_filter, filter_type, mode):
    height = len(img)
    width  = len(img[0])

    new_img = np.zeros((height,width),np.int32)

    for i in range(height):
        for j in range(width):
            if filter_type == "Mean":
                new_img[i, j] = mean_filter(img, img_filter, i, j, mode)
            elif filter_type == "Laplacian":
                if mode == "RGB":
                    gray_value =  5*img[i,j][0] - int(laplacian_filter(img, img_filter, i, j, mode))
                elif mode == "Gray":
                    gray_value =  5*img[i, j] - laplacian_filter(img, img_filter, i, j, mode)
                new_img[i, j] = gray_value

    
    if filter_type == "Laplacian":
        new_img = scaling(new_img)
    return new_img

def high_boost_filtering(img):
    img_filter = [[1 for i in range(11)] for i in range(11)]
    fuzzy_img = filter2d(img, img_filter, "Mean", "RGB")
    height = len(img)
    width  = len(img[0])

    sub_img = np.zeros((height,width),np.int32)

    for i in range(height):
        for j in range(width):
            sub_img[i ,j] = img[i, j][0] - fuzzy_img[i][j]

    k = 0.8
    enhanced_img = np.zeros((height,width),np.int32)
    for i in range(height):
        for j in range(width):
            enhanced_img[i, j] = img[i, j][0] + k * sub_img[i][j]

    enhanced_img = scaling(enhanced_img)

    return enhanced_img

def gama_correction(img, scale):
    table = [0 for i in range(256)]
    for i in range(256):
        val = pow(float(i)/255.0 ,scale) * 255.0
        if val>255:    
                val = 255    
        elif val<0:  
                val = 0  
        table[i]= val

    height = len(img)
    width  = len(img[0])

    new_img = np.zeros((height,width), np.uint8)

    for i in range(height):
        for j in range(width):
            new_img[i, j] = int(table[img[i,j]])

    return new_img

def scaling(img):
    gmax = np.amax(img)
    gmin = np.amin(img)
    height = len(img)
    width  = len(img[0])

    new_img = np.zeros((height,width),np.uint8)

    for i in range(height):
        for j in range(width):
            new_img[i, j] = int((img[i, j] - gmin) * 255 / (gmax - gmin))

    return new_img

def mean_filter(img, img_filter, x, y, mode):
    filter_size = len(img_filter[0])
    centre_gray_value = Convolution(img, img_filter, x, y, mode)
    return int(centre_gray_value / (filter_size**2))

def laplacian_filter(img, img_filter, x, y, mode):
    return Convolution(img, img_filter, x, y, mode)

def  Convolution(img, img_filter, x, y, mode):
    height = len(img)
    width  = len(img[0])

    filter_size = len(img_filter[0])
    factor = int(filter_size / 2)

    centre_gray_value = 0

    for i in range(filter_size):
        for j in range(filter_size):
            img_x = x - factor + i
            img_y = y - factor + j

            if (img_x < 0) or (img_x >= height) or (img_y < 0) or (img_y >= width):
                centre_gray_value += 0
            else:
                if mode == "RGB":
                    centre_gray_value += (img[img_x, img_y][0] * img_filter[i][j])
                elif mode == "Gray":
                    centre_gray_value += (img[img_x, img_y] * img_filter[i][j])

    return centre_gray_value


if __name__ == '__main__':
    img = cv2.imread("./14.png")

    img_filter1 = [[1,1,1],[1,1,1],[1,1,1]]
    filtered_image1 = filter2d(img, img_filter1, "Mean", "RGB")  
    cv2.imwrite("Image1.png", filtered_image1)

    img_filter2 = [[1 for i in range(7)] for i in range(7)]
    filtered_image2 = filter2d(img, img_filter2, "Mean", "RGB")
    cv2.imwrite("Image2.png", filtered_image2)

    img_filter3 = [[1 for i in range(11)] for i in range(11)]
    filtered_image3 = filter2d(img, img_filter3, "Mean", "RGB")
    cv2.imwrite("Image3.png", filtered_image3)

    img_filter4 = [[1,1,1], [1,-8,1], [1,1,1]]
    filtered_image4 = filter2d(img, img_filter4, "Laplacian", "RGB")
    filtered_image4 = Equalization.equalize_hist(filtered_image4, "Gray")
    cv2.imwrite("Image4.png", filtered_image4)

    filtered_image5 = high_boost_filtering(img)
    filtered_image5 = Equalization.equalize_hist(filtered_image5, "Gray")
    cv2.imwrite("Image5.png", filtered_image5)

