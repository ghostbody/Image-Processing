import cv2
import numpy as np

PATCH_H = 3
PATCH_W = 3
DISTANCE = 79

def CalculateDisparityAll(LeftImage, RightImage, flag=0):
    res_image = np.zeros(LeftImage.shape, np.int32)
    for i in xrange(LeftImage.shape[0]):
        for j in xrange(LeftImage.shape[1]):
            res_image[i, j] = CalculateMinDist(LeftImage, RightImage, i, j, flag) * 3;
            print "(%d,%d):%d" % (i, j, res_image[i,j])
    return res_image

def CalculateMinDist(LeftImage, RightImage, x, y, flag):
  min_index = y;
  min_num = 0;
  if flag == 1:
    PatchP = CalculateCenterPatch(LeftImage, x, y)
    for i in xrange(y, y + DISTANCE):
        if y > RightImage.shape[1]:
            break
        PatchQ = CalculateCenterPatch(RightImage, x, i);
        disparity = CalculateDisparitySumOne(PatchP, PatchQ)
        if min_num > disparity or i == y:
            min_num = disparity
            min_index = i
  elif flag == 0:
    PatchP = CalculateCenterPatch(RightImage, x, y)
    for i in xrange(y, y - DISTANCE, -1):
        if y < 0:
            break
        PatchQ = CalculateCenterPatch(LeftImage, x, i);
        disparity = CalculateDisparitySumOne(PatchP, PatchQ)
        if min_num > disparity or i == y:
            min_num = disparity
            min_index = i

  return np.abs(min_index - y);

def CalculateCenterPatch(M, x, y):
    res_image = np.zeros((PATCH_H, PATCH_W), np.int32)
    for i in xrange(0, PATCH_H):
        for j in xrange(0, PATCH_W):
            if x - PATCH_H/2 + i < 0 or y - PATCH_W/2 + j < 0 \
             or x - PATCH_H/2 + i >=  M.shape[0] or\
              y - PATCH_W/2 + j >= M.shape[1]:
                res_image[i, j] = 0
            else:
                res_image[i, j] = M[x - PATCH_H/2 + i, y - PATCH_W/2 + j]
    return res_image

def CalculateDisparitySumOne(P, Q):
    sum_val = 0
    for i in xrange(P.shape[0]):
        for j in xrange(P.shape[1]):
            sum_val += (P[i, j] - Q[i, j])**2
    return sum_val

def main():
    LeftImage = cv2.imread("./left.png", 0)
    RightImage = cv2.imread("./right.png", 0)
    res = CalculateDisparityAll(LeftImage, RightImage, 0)
    cv2.imwrite("py_res.png", res)

if __name__ == '__main__':
    main()
