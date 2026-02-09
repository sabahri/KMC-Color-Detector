Color Story

# Table of Contents
1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Script Summary](#3-script-summary)
4. [Future Work](#4-future-work)

# 1. Project Overview
This script detects the predominant colors in a given image. Since I intended it as an educational exercise in Computer Vision, I ignored existing OpenCV functions except for basic import and RGB <--> HSV data conversions. The script calculates colors in HSV space in order to facilitate future color detection adjustments according to Hue groups. To use, run:

```
python color_detector_KMC.py <num_colors> <image_path>
```
e.g.
```
python color_detector_KMC.py 5 utah_sunset.jpg
```

# 2. Architecture
```
[Input Image] 
    ↓
┌─────────────────────────┐
│   Preprocessing         │
│  ┌──────────────────┐   │
│  │ Downsample       │   │
│  └────────┬─────────┘   │
│           ↓             │
│  ┌──────────────────┐   │
│  │ RGB → HSV        │   │
│  │ Conversion       │   │
│  └────────┬─────────┘   │
│           ↓             │
│  ┌──────────────────┐   │
│  │ Reshape to       │   │
│  │ Pixel Array      │   │
│  └────────┬─────────┘   │
└───────────┼─────────────┘
            ↓
┌─────────────────────────┐
│   K-Means Clustering    │
│  ┌──────────────────┐   │
│  │ Initialize       │   │
│  │ Centroids (FPS)  │   │
│  └────────┬─────────┘   │
│           ↓             │
│  ┌──────────────────┐   │
│  │ Calculate        │   │
│  │ Distances (HSV)  │   │
│  └────────┬─────────┘   │ 
│           ↓             │
│  ┌──────────────────┐   │
│  │ Assign to        │   │
│  │ Clusters         │   │
│  └────────┬─────────┘   │
│           ↓             │
│  ┌──────────────────┐   │
│  │ Update Centroids │   │
│  │ (circular mean)  │   │
│  └────────┬─────────┘   │
│           ↓             │
│  └──→ Iterate 10x       │
└─────────────────────────┘
    ↓
[Sort by Hue]
    ↓
┌─────────────────────────┐
│  Generate Visualizations│
│  ├→ Color Swatches+Hex  │
│  └→ Polar Plot (H vs S) │
└─────────────────────────┘
```

# 3. Script Summary
The optimization method is KMC, which is probably the most basic unsupervised method. We first select an initiating set of pixel colors present in the image. We use farthest poinst sampling (FPS) in Hue space, selecting Hue values located at intervals of pi / (# number of colors to detect). The initiating Saturation and Value are set to 122.5. The program then compares each pixel to the initiating centroids, calculates the distance betweeen them, and assigns each pixel to the closest centroid. Finally, a new set of centroids is calculate based on the average of each group, and the process repeats again for a hard-coded number of iterations.

NOTE: OpenCV formats Hue values to range between 0 and 180. On the other hand, circular or cylindrical coordinate systems requre a range between 0 and 360. Therefore, Hue values are multiplied by 2 before the mean calculation, and then divided by 2 afterwards in keeping with OpenCV format.

The program produces three figures as output:

The first shows the original image, alongside a resized version of the image to reduce the pixel load for calculation efficiency. The percentage of pixels used for the calculation is hardcoded to 1%, but can be changed in the script using variable 'perc'.

<img width="640" height="480" alt="Figure1" src="https://github.com/user-attachments/assets/03166fa1-0860-4e63-a5f6-520442966169" />

The second visualizes breakdown of these pixels in RGB and HSV space.

<img width="640" height="480" alt="Figure_2" src="https://github.com/user-attachments/assets/4ad9a34d-f670-4dcf-a6e0-61fb804d9bde" />

The third shows the distribution of common hues according to increasing Hue, along with the HEX codes of each color. Alongside this distribution we show these pixels plotted on a polar graph.

<img width="640" height="480" alt="Figure_3" src="https://github.com/user-attachments/assets/ca822bd5-2c0b-4489-849e-290c29a3101d" />

# 4. Future Work:
  - Implement feature recognition to exclude photographed people from color stories (because that's just weird)
  - Create a matrix plot of colors so that common colors of similar hues are grouped together
