import cv2

def Reduce(image,m,n):
    H = int(image.height*m)
    W = int(image.width*n)
    size = (W,H)
    iReduce = cv2.CreateImage(size,image.depth,image.nChannels)
    for i in range(H):
        for j in range(W):
            x = int(i/m)
            y = int(j/n)
            iReduce[i,j] = image[x,y]
    return iReduce

    
image = cv2.imread('14.png',1)
iReduce1 = Reduce(image,0.7,0.6)
iReduce2 = Reduce(image,0.8,0.8)
cv2.ShowImage('image',image)
cv2.ShowImage('iReduce1',iReduce1)
cv2.ShowImage('iReduce2',iReduce2)
cv2.WaitKey(0)
