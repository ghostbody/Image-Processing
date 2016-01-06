#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <iostream>
#include <vector>
#include <algorithm>
#include <stdio.h>

using namespace std;
using namespace cv;

#define PATCH_H 3
#define PATCH_W 3
#define DISTANCE 79

Mat CalculateDisparityAll(const Mat & LeftImage, const Mat & RightImage, int falg);
int CalculateMinDist(const Mat & LeftImage, const Mat & RightImage, int x, int y, int flag);
Mat CalculateCenterPatch(const Mat & M, int x, int y);
int CalculateDisparitySumOne(const Mat & P, const Mat &Q);
int CalculateDisparityNCC(const Mat & P, const Mat & Q);

Mat CalculateDisparityAll(const Mat & LeftImage, const Mat & RightImage, int flag = 0) {
  Mat res(LeftImage.size(), CV_32S);
  for(int i = 0; i < LeftImage.rows; i++) {
    for(int j = 0; j < LeftImage.cols; j++) {
      int tempDisparityDistance = CalculateMinDist(LeftImage, RightImage, i, j, flag);
      res.at<int>(i, j) = tempDisparityDistance * 3;
      printf("(%d,%d):%d, %d\n", i, j, tempDisparityDistance, res.at<int>(i, j));
    }
  }
  return res;
}

int CalculateMinDist(const Mat & LeftImage, const Mat & RightImage, int x, int y, int flag) {
  int min_index = y;
  int min;
  if(flag == 1) {
    Mat PatchP = CalculateCenterPatch(LeftImage, x, y);
    for(int i = y; i < RightImage.cols  ; i++) {
      Mat PatchQ = CalculateCenterPatch(RightImage, x, i);
      // int disparity = CalculateDisparitySumOne(PatchP, PatchQ);
      int disparity = CalculateDisparityNCC(PatchP, PatchQ);
      if(min > disparity || i == y) {
        min = disparity;
        min_index = i;
      }
    }
  } else if(flag == 0) {
    Mat PatchP = CalculateCenterPatch(RightImage, x, y);
    for(int i = y; i >= 0  ; i--) {
      Mat PatchQ = CalculateCenterPatch(LeftImage, x, i);
      // int disparity = CalculateDisparitySumOne(PatchP, PatchQ);
      int disparity = CalculateDisparityNCC(PatchP, PatchQ);
      if(min > disparity || i == y) {
        min = disparity;
        min_index = i;
      }
    }
  }
  // return d
  return min_index - y > 0 ? min_index - y : y - min_index;
}

Mat CalculateCenterPatch(const Mat & M, int x, int y) {
  // Mat res(PATCH_H, PATCH_W, M.type());
  Mat res(PATCH_H, PATCH_W, CV_32S);
  for(int i = 0; i < res.rows; i++) {
    for(int j = 0; j < res.cols; j++) {
      if(x - PATCH_H/2 + i < 0 ||  y - PATCH_W/2 + j < 0
           || x - PATCH_H/2 + i >=  M.rows || y - PATCH_W/2 + j >= M.cols) {
        res.at<int>(i,j) = 0;
      } else {
        res.at<int>(i,j) = M.at<uchar>(x - PATCH_H/2 + i, y - PATCH_W/2 + j);
      }
    }
  }
  return res;
}

int CalculateDisparitySumOne(const Mat & P, const Mat & Q) {
  int sum = 0;
  // if(P.cols != Q.cols || P.rows != Q.rows) {
  //   return sum;
  // }
  for(int i = 0; i < P.rows; i++) {
    for(int j = 0; j < P.cols; j++) {
      int difference = P.at<int>(i,j) - Q.at<int>(i,j);
      // difference > 0 ? sum += difference : sum += -difference;
      sum += difference * difference;
    }
  }

  return sum;
}

int CalculateDisparityNCC(const Mat & P, const Mat & Q) {
  double f_hat = 0;
  double t_hat = 0;
  double f_cigma = 0;
  double t_cigma = 0;

  for(int i = 0; i < P.rows; i++) {
    for(int j = 0; j < P.cols; j++) {
      f_hat += P.at<int>(i,j);
      t_hat += Q.at<int>(i,j);
    }
  }

  f_hat /= P.rows * P.cols;
  t_hat /= P.rows * P.cols;

  for(int i = 0; i < P.rows; i++) {
    for(int j = 0; j < P.cols; j++) {
      f_cigma += (P.at<int>(i,j) - f_hat) * (P.at<int>(i,j) - f_hat);
      t_cigma += (Q.at<int>(i,j) - f_hat) * (Q.at<int>(i,j) - f_hat);
    }
  }

  f_cigma = sqrt(f_cigma / (P.rows * P.cols));
  t_cigma = sqrt(t_cigma / (P.rows * P.cols));

  double sum = 0;

  for(int i = 0; i < P.rows; i++) {
    for(int j = 0; j < P.cols; j++) {
      sum += (P.at<int>(i,j) - f_hat) * (Q.at<int>(i,j) - t_hat) / (f_cigma * t_cigma);
    }
  }

  int res = (int)(sum * P.rows * P.cols);
  cout << f_hat << " " << t_hat << endl;
  return res > 0 ? res : - res;
}

Mat & scalling(Mat & M) {
  if(M.channels() > 1) {
    std::cout << "[Function] Scalling: unable to scalling RGB" << std::endl;
    return M;
  }
  int max, min;

  max = min = ((Vec3b)M.at<int>(0,0))[0];

  for(int i = 0 ; i < M.rows; i++) {
    for(int j = 0; j < M.cols; j++) {
      int temp = M.at<Vec2b>(i, j)[0];
      printf("temp: %d\n", temp);
      if(temp > max) {
        max = temp;
      }
      if(temp < min) {
        min = temp;
      }
    }
  }

  for(int i = 0; i < M.rows; i++) {
    for(int j = 0; j < M.cols; j++) {
      M.at<Vec2b>(i, j)[0] = int(double(M.at<Vec2b>(i, j)[0] - min) / (max - min) * 255);
    }
  }
  return M;
}

void help() {
  printf("usage: $stero_pro$ LeftImage RightImage [DisparitySide]\n");
  printf("DisparitySide: left for default, left|right for options\n");
}

int main(int argc, char ** argv) {
  Mat LeftImage, RightImage;
  LeftImage = imread(argv[1], IMREAD_GRAYSCALE);
  RightImage = imread(argv[2], IMREAD_GRAYSCALE);

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
