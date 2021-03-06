int main( int argc, char** argv ){
  Mat image;
  image = imread(argv[1]);

  if( argc != 2 || !image.data ){
    printf("没有图片\n");
    return -1;
  }

  for (int i = 0; i < image.cols; i++) {
    for (int j = 0; j < image.rows; j++) {
      Vec3b intensity = image.at<Vec3b>(j, i);
      cout << "R:" << (uint)intensity.val[0] << " ";
      cout << "G:" << (uint)intensity.val[1] << " ";
      cout << "B:" << (uint)intensity.val[2] << " ";
      cout << endl;
    }
  }

  namedWindow( "显示图片", CV_WINDOW_AUTOSIZE );
  imshow( "显示图片", image );
  waitKey(0);

  return 0;
}
