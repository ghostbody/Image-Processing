#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <vector>
#include <algorithm>
#include <stdio.h>
#include <cmath>

using namespace std;
using namespace cv;

#define PATCH_H 5
#define PATCH_W 5
#define DISTANCE 79

Mat CalculateDisparityAll(const Mat & LeftImage, const Mat & RightImage, int falg);
int CalculateMinDistASW(const Mat & LeftImage, const Mat & RightImage, int x, int y, int flag);
Mat CalculateCenterPatch(const Mat & M, int x, int y);

double Eppd(const Mat & P, const Mat & Q, int d);

double wpq(const Vec3b & p, const Vec3b & q, int d);

double deltaCpq(const Vec3b & p, const Vec3b & q);
double e0(const Vec3b & q, const Vec3b & qd);


Mat CalculateDisparityAll(const Mat & LeftImage, const Mat & RightImage, int flag = 0) {
  Mat res(LeftImage.size(), CV_32S);
  for(int i = 0; i < LeftImage.rows; i++) {
    for(int j = 0; j < LeftImage.cols; j++) {
      int tempDisparityDistance = CalculateMinDistASW(LeftImage, RightImage, i, j, flag);
      res.at<int>(i, j) = tempDisparityDistance * 3;
      printf("processing    (%d,%d):%d, %d\n", i, j, tempDisparityDistance, res.at<int>(i, j));
      printf("\033[1A");
      printf("\033[K");
    }
  }
  return res;
}

int CalculateMinDistASW(const Mat & LeftImage, const Mat & RightImage, int x, int y, int flag) {
  int min_index = y;
  double min;
  if(flag == 1) {
    Mat PatchP = CalculateCenterPatch(LeftImage, x, y);
    for(int i = y; i < RightImage.cols  && i < y + DISTANCE; i++) {
      Mat PatchQ = CalculateCenterPatch(RightImage, x, i);
      double disparity = Eppd(PatchP, PatchQ, i - y);
      if(min > disparity || i == y) {
        min = disparity;
        min_index = i;
      }
    }
  } else if(flag == 0) {
    Mat PatchP = CalculateCenterPatch(RightImage, x, y);
    for(int i = y; i >= 0 && i >= y - DISTANCE ; i--) {
      Mat PatchQ = CalculateCenterPatch(LeftImage, x, i);
      double disparity = Eppd(PatchP, PatchQ, i - y);
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
  Mat res(PATCH_H, PATCH_W, CV_32SC3);
  for(int i = 0; i < res.rows; i++) {
    for(int j = 0; j < res.cols; j++) {
      for(int k = 0; k < M.channels(); k++) {
        if(x - PATCH_H/2 + i < 0 ||  y - PATCH_W/2 + j < 0
             || x - PATCH_H/2 + i >=  M.rows || y - PATCH_W/2 + j >= M.cols) {
          res.at<Vec3b>(i,j).val[k] = 0;
        } else {
          res.at<Vec3b>(i,j).val[k] = (M.at<Vec3b>(x - PATCH_H/2 + i, y - PATCH_W/2 + j))[k];
        }
      }
    }
  }

  return res;
}

double Eppd(const Mat & P, const Mat & Q, int d) {
  Vec3b p = P.at<Vec3b>(P.rows / 2, P.cols / 2);
  Vec3b pd = Q.at<Vec3b>(Q.rows / 2, Q.cols / 2);

  double sum1 = 0;
  double sum2 = 0;

  for(int i = 0; i < P.rows; i++) {
    for(int j = 0; j < P.cols; j++) {
      sum1 += wpq(p, P.at<Vec3b>(i,j), d) * wpq(pd, Q.at<Vec3b>(i,j), d) * e0(P.at<Vec3b>(i,j), Q.at<Vec3b>(i,j));
      sum2 += wpq(p, P.at<Vec3b>(i,j), d) * wpq(pd, Q.at<Vec3b>(i,j), d);
    }
  }
  return sum2 != 0 ? sum1 / sum2 : 0;
}

double wpq(const Vec3b & p, const Vec3b & q, int d) {
  double k = 100;
  double gamac = 30;
  double gamap = 13;
  return k*exp(-(deltaCpq(p,q) / gamac + d / gamap));
}

double f(double t) {
  if(t > pow(6.0/29, 3)) {
    return pow(t, 1.0/3);
  } else {
    (1.0/3)*pow(29.0/6, 2)*t + 4.0/29;
  }
}

// Lab space color difference calculation
double deltaCpq(const Vec3b & p, const Vec3b & q) {
  double pXYZ[3] = {0};
  double qXYZ[3] = {0};
  double pLab[3] = {0};
  double qLab[3] = {0};

  pXYZ[0] = p[0] * 0.4124 + p[1] * 0.3576 + p[2] * 0.1805;
  pXYZ[1] = p[0] * 0.2126 + p[1] * 0.7152 + p[2] * 0.0722;
  pXYZ[2] = p[0] * 0.0193 + p[1] * 0.1192 + p[2] * 0.9505;

  qXYZ[0] = q[0] * 0.4124 + q[1] * 0.3576 + q[2] * 0.1805;
  qXYZ[1] = q[0] * 0.2126 + q[1] * 0.7152 + q[2] * 0.0722;
  qXYZ[2] = q[0] * 0.0193 + q[1] * 0.1192 + q[2] * 0.9505;

  const double Xn = 95.047;
  const double Yn = 100.0;
  const double Zn = 108.883;

  qLab[0] = 116 * f(qXYZ[1] / Yn) - 16;
  qLab[1] = 500 * (f(qXYZ[0]) / Xn - (f(qXYZ[1]) / Yn));
  qLab[2] = 200 * (f(qXYZ[1]) / Yn - (f(qXYZ[2]) / Zn));

  return sqrt((pLab[0] - qLab[0]) * (pLab[0] - qLab[0]) + (pLab[1] - qLab[1]) * (pLab[1] - qLab[1]) + (pLab[2] - qLab[2]) * (pLab[2] - qLab[2]));
}

//RGB space color difference calculation
// double deltaCpq(const Vec3b & p, const Vec3b & q) {
//   const int wr = 3;
//   const int wg = 4;
//   const int wb = 2;
//   return sqrt(wr*(p[0] - q[0]) * (p[0] - q[0]) + wg*(p[1] - q[1]) * (p[1] - q[1]) + wb*(p[2] - q[2]) * (p[2] - q[2]));
// }

double e0(const Vec3b & q, const Vec3b & qd) {
  return abs(q[0] - qd[0]) + abs(q[1] - qd[1]) + abs(q[2] - qd[2]);
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

  Mat resImage = CalculateDisparityAll(RightImage, LeftImage, side);
  printf("processing Done\n");
  if(side == 1) {
    imwrite("Right.png", resImage);
  } else {
    imwrite("Left.png", resImage);
  }

  return 0;
}
