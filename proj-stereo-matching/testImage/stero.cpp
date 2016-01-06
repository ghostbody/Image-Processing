#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <iostream>
#include <vector>
#include <algorithm>
#include <stdio.h>

using namespace std;
using namespace cv;

#define PATCH_H 7
#define PATCH_W 7
#define DISTANCE 79

Mat CalculateDisparityAll(const Mat & LeftImage, const Mat & RightImage, int falg);
int CalculateMinDistASW(const Mat & LeftImage, const Mat & RightImage, int x, int y, int flag);
Mat CalculateCenterPatch(const Mat & M, int x, int y);

Mat CalculateDisparityAll(const Mat & LeftImage, const Mat & RightImage, int flag = 0) {
  Mat res(LeftImage.size(), CV_32S);
  for(int i = 0; i < LeftImage.rows; i++) {
    for(int j = 0; j < LeftImage.cols; j++) {
      int tempDisparityDistance = CalculateMinDistASW(LeftImage, RightImage, i, j, flag);
      res.at<int>(i, j) = tempDisparityDistance * 3;
      printf("(%d,%d):%d, %d\n", i, j, tempDisparityDistance, res.at<int>(i, j));
    }
  }
  return res;
}

int CalculateMinDistASW(const Mat & LeftImage, const Mat & RightImage, int x, int y, int flag) {
  int min_index = y;
  int min;
  if(flag == 1) {
    Mat PatchP = CalculateCenterPatch(LeftImage, x, y);
    for(int i = y; i < RightImage.cols  && i < y + DISTANCE; i++) {
      Mat PatchQ = CalculateCenterPatch(RightImage, x, i);
      // int disparity = CalculateDisparityASWOne(PatchP, PatchQ);
      int disparity = 0;
      if(min > disparity || i == y) {
        min = disparity;
        min_index = i;
      }
    }
  } else if(flag == 0) {
    Mat PatchP = CalculateCenterPatch(RightImage, x, y);
    for(int i = y; i >= 0 && i >= y - DISTANCE ; i--) {
      Mat PatchQ = CalculateCenterPatch(LeftImage, x, i);
      // int disparity = CalculateDisparityASWOne(PatchP, PatchQ);
      int disparity = 0;
      if(min > disparity || i == y) {
        min = disparity;
        min_index = i;
      }
    }
    std::cout << PatchP << std::endl;
  }

  // return d
  return min_index - y > 0 ? min_index - y : y - min_index;
}

Mat CalculateCenterPatch(const Mat & M, int x, int y) {
  // Mat res(PATCH_H, PATCH_W, M.type());
  Mat res(PATCH_H, PATCH_W, CV_32SC3);
  for(int i = 0; i < res.rows; i++) {
    for(int j = 0; j < res.cols; j++) {
      for(int k = 0; k < M.channels(); k++) {
        if(x - PATCH_H/2 + i < 0 ||  y - PATCH_W/2 + j < 0
             || x - PATCH_H/2 + i >=  M.rows || y - PATCH_W/2 + j >= M.cols) {
          res.at<Vec3b>(i,j).val[k] = 0;
        } else {
          res.at<Vec3b>(i,j).val[k] = (M.at<Vec3b>(x - PATCH_H/2 + i, y - PATCH_W/2 + j))[k];
          cout << (int)(res.at<Vec3b>(i,j).val[k]) << endl;
        }
      }
    }
  }
  return res;
}


void help() {
  printf("usage: $stero_pro$ LeftImage RightImage [DisparitySide]\n");
  printf("DisparitySide: left for default, left|right for options\n");
}

int main(int argc, char ** argv) {
  Mat LeftImage, RightImage;
  LeftImage = imread(argv[1]);
  RightImage = imread(argv[2]);

  if(LeftImage.empty() || RightImage.empty()){
    help();
    return -1;
  }

  int side = 0;

  if(argc <= 3) {
    side = 0;
  }

  if(strcmp(argv[3], "right") == 0) {
    side = 1;
  }

  printf("processing...\n");
  Mat resImage = CalculateDisparityAll(RightImage, LeftImage, side);

  if(side == 1) {
    imwrite("Right.png", resImage);
  } else {
    imwrite("Left.png", resImage);
  }

  return 0;
}
