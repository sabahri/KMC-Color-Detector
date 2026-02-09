Color Story

# **Table of Contents**
- Project Overview
- Script Summary
- Mathematical Operations
- TO DO

# **Project Overview**
This script detects the predominant colors in a given image. Since I intended it as an educational exercise in Computer Vision, I ignored existing OpenCV functions except for basic import and RGB <--> HSV data conversions. The script calculates colors in HSV space in order to facilitate future color detection adjustments according to Hue groups.

# **Script Summary**
The optimization method is KMC, which is probably the most basic unsupervised method. We first select an initiating set of pixel colors present in the image. We use farthest poinst sampling (FPS) in Hue space, selecting Hue values located at intervals of 2pi / (# number of colors to detect). The initiating Saturation and Value are set to 122.5. The program then compares each pixes to the initiating centroids, calculates the distance betweeen them, and assigns each pixel to the closest centroid. Finally, a new set of centroids is calculate based on the average of each group, and the process repeats again for a hard-coded number of iterations.

The program produces three figures as output:

The first shows the original image, alongside a resized version of the image to reduce the pixel load for calculation efficiency. The percentage of pixels used for the calculation is hardcoded to 1%, but can be changed in the script using variable 'perc'.

<img width="640" height="480" alt="Figure1" src="https://github.com/user-attachments/assets/03166fa1-0860-4e63-a5f6-520442966169" />

The second visualizes breakdown of these pixels in RGB and HSV space.

<img width="640" height="480" alt="Figure_2" src="https://github.com/user-attachments/assets/4ad9a34d-f670-4dcf-a6e0-61fb804d9bde" />

The third shows the distribution of common hues according to increasing Hue, along with the HEX codes of each color. Alongside this distribution we show these pixels plotted on a polar graph. The graphics are mainly for matplotlib practice.

<img width="640" height="480" alt="Figure_3" src="https://github.com/user-attachments/assets/ca822bd5-2c0b-4489-849e-290c29a3101d" />

# **Mathematical Background**

# **TO DO:**
  - Implement feature recognition to exclude photographed people from color stories (because that's just weird)
  - Create a matrix plot of colors so that common colors of similar hues are grouped together
  - Implement and interactive feature so that the HEX code appears when a pixel is clicked
