# Introduction
This script detects the predominant colors in a given image. Since I intended it as an educational exercise in Computer Vision, I ignored existing OpenCV functions except for basic import and RGB <--> HSV data conversions.

The script primarily uses K-Means Clustering in HSV space. KMC is a very approachable and basic unsupervised Machine Learning method, while HSV space (as opposed to RGB) provides greatest flexibility by encoding the color in a single value (Hue). HSV space also provides a greater mathematical challenge because of its cylindrical as opposed to Cartesian coordinate system.

The user provides the image and the desired number of colors, and the script outputs the color distribution with corresponding color HEX codes.

KMC is a hard clustering mathod that, in this context, assigns pixels to a most likely HSV color value. It begins with a random initialization of centroids (the HSV values of randomly chosen pixels from the image), and computes the color distance of each pixel in the image from those randomly selected.
Following this, each pixel is clustered with others that are closest to the same centroid, and their HSV values are averaged to a more optimized centroid location. This process repeats for a given number of iterations (here, I set it to 20), producing the final optimized averages of clustered pixels.

# Script Summary

Since using the fully sized original image slows down computation excessively, the image is first reduce to 1% of its original pixels. This of course also reduces the color accuracy, but not to an appreciable extent.

<img width="640" height="480" alt="Figure1" src="https://github.com/user-attachments/assets/03166fa1-0860-4e63-a5f6-520442966169" />

<img width="640" height="480" alt="Figure_2" src="https://github.com/user-attachments/assets/4ad9a34d-f670-4dcf-a6e0-61fb804d9bde" />

<img width="640" height="480" alt="Figure_3" src="https://github.com/user-attachments/assets/ca822bd5-2c0b-4489-849e-290c29a3101d" />


# The Math

