#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <iostream>
#include <vector>
#include <algorithm>
#include <stdio.h>
#include <cmath>

using namespace std;
using namespace cv;

double CalculateDisparityErrorOne(int, int);

#define BORDER 10

double CalculateDisparityErrorPercent(const Mat & DisparityMap, const Mat & GroudTruth) {
  int sum = 0;
  for(int i = BORDER; i < GroudTruth.rows - BORDER; i++) {
    for(int j = BORDER; j < GroudTruth.cols - BORDER; j++) {
      int GroudTruthVal = GroudTruth.at<int>(i, j);
      int DisparityMapVal = DisparityMap.at<int>(i, j);
      if(GroudTruthVal == 0) {
        continue;
      }
      double error = CalculateDisparityErrorOne(DisparityMapVal, GroudTruthVal);
      if(error > 3) {
        sum++;
      }
    }
  }
  return ((double)sum) / (GroudTruth.rows * GroudTruth.cols) * 100;
}

double CalculateDisparityErrorOne(int DisparityMapVal,
                                    int GroudTruthVal) {
  double res = DisparityMapVal - GroudTruthVal;
  return res > 0 ? res : -res;
}

int main(int argc, char const *argv[]) {
  Mat GroudTruth, DisparityMap;
  GroudTruth = imread(argv[1], 0);
  DisparityMap = imread(argv[2], 0);
  const char * name = argv[3];

  if(GroudTruth.empty() || DisparityMap.empty()){
    printf("usage: $eval_pro$ GroudTruthImage DisparityMap %s\n", name);
    return -1;
  }

  printf("[%s] \t %lf\n", name, CalculateDisparityErrorPercent(DisparityMap, GroudTruth));
  return 0;
}
