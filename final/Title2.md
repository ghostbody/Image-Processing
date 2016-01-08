
## DIP Final Project : Stero Matching

<br>

### Basic Task
**1.Implement a test program to evaluate the quality of your disparity maps. Your program should output the percentage of bad pixels in each of your disparity maps, where bad pixels are those whose errors are greater than one when comparing to ground truths (without multiplication).**

(You can see the implementation in the code evaluate.cpp)
Calculation Formula:
$$
E(x,y) = {|D(x,y) - G(x,y)|} \ \  (G(x,y) != 0)
$$


(D(x,y) indicates a pixel in disparity map, G(x,y) indicates the corresponding pixel in GroundTruth, when G(x,y) = 0, the result is not defined)

This program is used to evaluate the quality of the disparity map later with inputs(disparitymap, groundtruth) and output(bad_pixel_percentage)
This is an example of its output:
```c
[Rocks2]the percentage of bad pixels: 9.355803
[Rocks2]the percentage of bad pixels: 8.801272
[Wood2]the percentage of bad pixels: 18.744331
[Wood2]the percentage of bad pixels: 17.688102
```
The higher bad_pixel_percentage the disparity map has, the worse the disparity map is. So the best way for stero matching should be the way that result in a small bad percentage.

**2. Implement a local stereo matching algorithm using “Sum of Squared Difference (SSD)” as matching cost. Compute both the left and the right disparity maps for all test cases, and visualize them by scaling their intensities by a factor of three. Save each disparity map to a file named testcasename disp1 SSD.png or testcasename disp5 SSD.png. Also write down the matching cost function and the quality of your disparity maps.**
Matching cost function:
$$
D(p,q) = \sum_{i,j\in P_p,Qq}(P_p(i,j) - Q_q(i,j))^2
$$
(P,Q indicates the patch in Left and Right)

Experiment in patch size(5*5)
(You can see the result image in the SSD folder)

Evaluating result:
```c
[Baby2] 		 86.623912
[Baby2] 		 86.485832
[Plastic] 		 95.403489
[Plastic] 		 95.960003
[Lampshade1] 	 90.939392
[Lampshade1] 	 90.484364
[Wood1] 		 84.996747
[Wood1] 		 85.702289
[Cloth2] 		 85.989014
[Cloth2] 		 86.743649
[Bowling2] 		 88.971997
[Bowling2] 		 89.059850
[Midd1] 		 90.292357
[Midd1] 		 91.058413
[Cloth1] 		 77.970056
[Cloth1] 		 77.347851
[Aloe] 			 82.254573
[Aloe] 	 		 82.334958
[Monopoly] 		 91.509975
[Monopoly] 		 91.359893
[Cloth3] 		 80.191847
[Cloth3] 		 79.908614
[Baby1] 		 79.717950
[Baby1] 		 79.548459
[Rocks1] 		 80.377742
[Rocks1] 		 80.512560
[Lampshade2] 	 91.407528
[Lampshade2] 	 91.998627
[Flowerpots] 	 93.149236
[Flowerpots] 	 93.285917
[Midd2] 	   	 92.732997
[Midd2] 	 	 92.919513
[Baby3] 		 84.986084
[Baby3] 		 84.874142
[Cloth4] 		 81.736471
[Cloth4] 		 82.141564
[Bowling1] 		 92.239938
[Bowling1] 		 92.373453
[Rocks2] 		 82.866137
[Rocks2] 		 82.267727
[Wood2] 		 85.840323
[Wood2] 		 85.942839
```

**3. Implement a local stereo matching algorithm using “Normalized Cross Correlation (NCC)” as matching cost. Visualize and save your estimated disparity maps to testcasename disp1 NCC.png or testcasename disp5 NCC.png. You are required to figure out the meaning of NCC by yourselves and write down the formula of the NCC matching cost. Also write down the quality of your disparity maps.**

NCC explantion:
>In signal processing, cross-correlation is a measure of similarity of two series as a function of the lag of one relative to the other. This is also known as a sliding dot product or sliding inner-product. It is commonly used for searching a long signal for a shorter, known feature. It has applications in pattern recognition, single particle analysis, electron tomography, averaging, cryptanalysis, and neurophysiology.

*From wikipedia*

As an example, consider two real valued functions f and g differing only by an unknown shift along the x-axis. One can use the cross-correlation to find how much g must be shifted along the x-axis to make it identical to f. The formula essentially slides the g function along the x-axis, calculating the integral of their product at each position. When the functions match, the value of (f\star g) is maximized. This is because when peaks (positive areas) are aligned, they make a large contribution to the integral. Similarly, when troughs (negative areas) align, they also make a positive contribution to the integral because the product of two negative numbers is positive.

The Formula of NCC:
$$
D(p,q) = \frac{1}{n}\cdot \sum_{i,j \in N_{pq}} \frac{(f_p(i,j)-\hat f_p)\cdot(g_q(i,j)-\hat g_q)}{\sigma f_p \sigma g_p}
$$
(f hat and g hat indicates the mean value of the window, and sigma means the variance of the window)
Notice that we are supposed to use max value according to the definition of NCC, i.e.
$$
D(x,y) = arg_{d\in \{0...dmax\}}max(F,G)
$$

Evaluating result:
```c
[Baby2] 		 86.623912
[Baby2] 		 86.485832
[Plastic] 		 95.403489
[Plastic] 		 95.960003
[Lampshade1] 	 90.939392
[Lampshade1] 	 90.484364
[Wood1] 		 84.996747
[Wood1] 		 85.702289
[Cloth2] 		 85.989014
[Cloth2] 		 86.743649
[Bowling2] 		 88.971997
[Bowling2] 		 89.059850
[Midd1] 		 90.292357
[Midd1] 		 91.058413
[Cloth1] 		 77.970056
[Cloth1] 		 77.347851
[Aloe] 			 82.254573
[Aloe] 			 82.334958
[Monopoly] 		 91.509975
[Monopoly] 		 91.359893
[Cloth3] 		 80.191847
[Cloth3] 		 79.908614
[Baby1] 		 79.717950
[Baby1] 		 79.548459
[Rocks1] 		 80.377742
[Rocks1] 		 80.512560
[Lampshade2] 	 91.407528
[Lampshade2] 	 91.998627
[Flowerpots] 	 93.149236
[Flowerpots] 	 93.285917
[Midd2] 		 92.732997
[Midd2] 		 92.919513
[Baby3] 		 84.986084
[Baby3] 		 84.874142
[Cloth4] 		 81.736471
[Cloth4] 		 82.141564
[Bowling1] 	   	 92.239938
[Bowling1] 		 92.373453
[Rocks2] 		 82.866137
[Rocks2] 		 82.267727
[Wood2] 		 85.840323
[Wood2] 		 85.942839

```

**Add a small constant amount of intensity (e.g. 10) to all right eye images, and re-run the above two methods. Analyze how the intensity change affects the results (i.e. the quality) of the two methods. Explain in which ways that NCC is a better matching cost than SSD.**

In my experiment, if add a small constant of intensity to the image, both NCC and SSD's disparity map will result in worse result. Specially, the SSD's disparity map will result even worse than NCC. SSD's disparity map loss its basic profile but NCC reserved.(see the result in CNCC and CSSD)

SSD add constant 10 result
```c
[Baby2] 		 89.896604
[Baby2] 		 85.593220
[Plastic] 		 88.304262
[Plastic] 		 86.158073
[Lampshade1] 	 84.219462
[Lampshade1] 	 73.606516
[Wood1] 		 88.854456
[Wood1] 		 91.019575
[Cloth2] 		 94.607702
[Cloth2] 		 91.513014
[Bowling2]	 	 84.290159
[Bowling2] 		 79.769386
[Midd1] 		 83.192677
[Midd1] 		 72.415577
[Cloth1] 		 97.745803
[Cloth1] 		 95.213559
[Aloe] 			 93.188176
[Aloe] 			 94.152794
[Monopoly] 		 96.091758
[Monopoly] 		 90.593618
[Cloth3] 		 94.215438
[Cloth3] 		 89.472422
[Baby1] 		 94.743799
[Baby1] 		 91.389961
[Rocks1] 		 94.054690
[Rocks1] 		 90.436248
[Lampshade2] 	 83.931090
[Lampshade2] 	 72.315711
[Flowerpots] 	 73.113365
[Flowerpots] 	 70.875750
[Midd2] 		 81.773686
[Midd2] 		 71.585982
[Baby3] 		 88.570103
[Baby3] 		 86.137052
[Cloth4] 		 95.223769
[Cloth4] 		 92.755758
[Bowling1] 		 83.129820
[Bowling1] 		 76.843606
[Rocks2] 		 95.115421
[Rocks2] 		 92.391097
[Wood2] 		 92.915191
[Wood2] 		 92.140416

```

NCC  add constant 10
```
[Baby2] 		 87.540082
[Baby2] 		 20.133499
[Plastic] 		 71.748131
[Plastic] 		 25.738930
[Lampshade1] 	 71.480557
[Lampshade1] 	 16.047063
[Wood1] 		 90.974037
[Wood1] 		 22.077000
[Cloth2] 		 94.617065
[Cloth2] 		 20.848262
[Bowling2] 		 79.796230
[Bowling2] 		 31.101214
[Midd1] 		 67.438535
[Midd1] 		 29.808777
[Cloth1] 		 85.013935
[Cloth1] 		 11.200985
[Aloe] 	 		 90.169631
[Aloe] 	 		 18.427116
[Monopoly] 		 92.618510
[Monopoly] 		 37.651150
[Cloth3] 		 93.256854
[Cloth3] 		 41.552272
[Baby1] 		 86.632419
[Baby1] 		 15.481971
[Rocks1] 		 93.103975
[Rocks1] 		 44.372019
[Lampshade2] 	 65.176955
[Lampshade2] 	 12.695837
[Flowerpots] 	 90.497866
[Flowerpots] 	 47.730843
[Midd2] 		 66.247104
[Midd2] 		 30.431838
[Baby3] 		 88.249119
[Baby3] 		 33.716989
[Cloth4] 		 91.010549
[Cloth4] 		 15.795518
[Bowling1] 		 61.824486
[Bowling1] 		 17.068507
[Rocks2] 		 93.700477
[Rocks2] 		 37.656598
[Wood2] 		 67.785648
[Wood2] 		 11.588071
```

>SSD method has a higher computational complexity compared to SAD algorithm as it involves numerous multiplication operations. Normally, two areas which consist of exactly the same pixel values would yield a score of zero. However, these measures will no longer yield the correct results in the case of radiometric distortion, i.e., **where the pixel values in one image differ from those in the other image by a constant offset and/or gain factor. **
>...
>NCC algorithm is robust to the linear variation in the brightness due to different illumination conditions to the cameras. But it can be seen that due to more complex calculations of division, multiplication and square root its computational time is more than SAD, SSD. Hence it could only be used for real time application only if we are able to develop more efficient algorithm to speed up matching process. 

*From Papper :Comparison of Various Stereo Vision Cost Aggregation Methods*

In a word, NCC perform better than SSD when one image differ from those in the other image by a constant offset but cost more time.

**5.Cost aggregation using Adaptive Support Weight (ASW) is a powerful local stereo approach. You are required to implement this approach described in the CVPR’05 paper “Locally Adaptive Support-Weight Approach for Visual Correspondence Search” (to save time you are recommended to read mainly sec. 2.6 and sec. 3 of the paper). Visualize and save your estimated disparity maps to testcasename disp1 ASW.png or testcasename disp5 ASW.png. Also write down the quality of your disparity maps. Note that this algorithm is in general a bit slow.**



**6.6. Explain the idea of the ASW paper in question 5. Also explain in which ways ASW is better than NCC. Why?**
The core idea of ASW(Adaptive Support-Weight Approach) is to give a weight value to each pixel in the matching window, which is based on the color difference and the distance between them and the center point of the window. In essence, an approximate image segmentation is completed.

According to the like between location and color difference of window in the original pixel cost Fu to different weighting, and to perform polymerization. Many studies show that the algorithm is all local stereo matching effect is the best, and the result of matching algorithm and the optimization results compared. But the algorithm of adaptive weighted algorithm is relatively slow, and the complexity of the algorithm is relatively high, and the weight of the storage space is very large.

ASW is better than NCC, but NCC is very slow. In the case that the images are colorful(3 channels), ASW is good. But for gray images, ASW are not necessary because color images do not have the definition of color difference(cq).


### implementation details

### discussions of the disadvantages of the paper

### improvements