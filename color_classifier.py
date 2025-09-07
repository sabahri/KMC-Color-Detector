# INVOKE (app name in progress)

# Program for color detection
# Useful Links:
# https://realpython.com/python-opencv-color-spaces/
# https://www.timpoulsen.com/2018/finding-the-dominant-colors-of-an-image.html
# https://stackoverflow.com/questions/29156091/opencv-edge-border-detection-based-on-color

#########################################
############ Things to do ###############
#########################################

# Face/skin detection to remove skin tone from color story analysis
# Kmeans clustering to find most dominant colors
# Add Hues range to colors for more choices in color depth
# Output HEX color codes for these colors
# Web scraping (might be a separate script)
# App construction

import cv2
import numpy as np
import random
import matplotlib.pyplot as plt

# To make colored 3D scatter plot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

# Saving all color space conversions into 'flags' variable
flags = [i for i in dir(cv2) if i.startswith('COLOR_')]

# Import image from path file and convert from BGR to RGB format
path = "/Users/salima/Desktop/Git/Color-Story-Generator/images/utah_sunset.jpg"
original_image = cv2.imread(path)
original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

# Reducing to 5% of image resolution to speed up color splitting
reduced_image = cv2.resize(original_image, (0,0), fx=0.01, fy=0.01, interpolation=cv2.INTER_AREA)

#gray_flowers = cv2.cvtColor(flowers, cv2.COLOR_RGB2GRAY)
#edges = cv2.Canny(gray_flowers, 60,100)

'''
#########################################
############ Comparing Photos ###########
#########################################

Titles = ["Original", "Resized to 1%"] #, "Canny Edge Detection"]
images = [original_image, reduced_image] #, edges]
count = 2

for i in range(count):
	plt.subplot(1, 2, i+1)
	plt.title(Titles[i])
	plt.imshow(images[i])

plt.tight_layout

##################################
######### Scatter Plots ##########
##################################
'''

# Facecolors

pixel_colors = reduced_image.reshape((np.shape(reduced_image)[0] * np.shape(reduced_image)[1], 3))
norm = colors.Normalize(vmin = 1., vmax = 1.)
norm.autoscale(pixel_colors)
pixel_colors = norm(pixel_colors).tolist()

# Split image into component channels (RGB, HSV respectively)

r, g, b = cv2.split(reduced_image)						
hsv_image = cv2.cvtColor(reduced_image, cv2.COLOR_RGB2HSV)
h, s, v = cv2.split(hsv_image)


'''
# Subplots Setup

fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1, projection = "3d")

# RGB Scatter Plot

ax1.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker='.')
ax1.set_xlabel("Red")
ax1.set_ylabel("Green")
ax1.set_zlabel("Blue")

# HSV Scatter Plot

ax2 = fig.add_subplot(1, 2, 2, projection = "3d")
ax2.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker='.')
ax2.set_xlabel("Hue")
ax2.set_ylabel("Saturation")
ax2.set_zlabel("Value")
'''

##############################################
############ K-means Clustering ##############
##############################################

# 1. Randomly select k cluster centroids       							
# 2. Assign each data point to the nearest centroid to form clusters
# 3. Recalculate centroid by averaging points (update step)
# 4. Repeat until convergence


### Note: maybe add a function to maximize the distance between centroids in hue space ###
### Are there any existing algorithms that do this efficiently? ###
### This may end up being problematic for values close to 0 / 360 in the "red" space ###


# image_array is the 1% reduced image (shape = h(pixels) x w(pixels) x 3(color channels))
# num_centroids is the number of clusters to aim for (integer)

def reshape_image(image_array):
	height, width, c_channels = image_array.shape

	# Total number of pixels
	num_pixels = height * width

	# Reshape 3D array into 2D, with the first dimension being having shape [num_pixels]
	image_reshaped = np.reshape(image_array, [num_pixels, c_channels])

	return(num_pixels, image_reshaped)

# Plotting the range of Hues in the image
# Do this in a cylindrical representation?

def hue_range(array):
	image_reshaped = reshape_image(array)[1]
	hue = image_reshaped[:,0]

	count = np.zeros(180)

	for i in range(hue.shape[0]):
		for j in range(180):
			if hue[i] == j:
				count[j] += 1
	'''
	hues_opencv = np.linspace(0, 179, 180)
	#plt.scatter(hues_opencv, count, color = 'lightgreen', edgecolor = 'black')
	plt.hist(hue,180, color='lightgreen', edgecolor = 'black')
	plt.xlabel('Hue')
	plt.ylabel('Count')
	plt.title('Hue Distribution in Image')
	plt.show()
	'''
	return(hue, count)

def hue_circular_plot(array):

	# note, in OpenCV the hue range is from 0 to 180
	# so all hue values must be doubled to fit onto a cylindrical plot

	hue = hue_range(array)[0] * 2
	count = hue_range(array)[1]

	hue_rad = np.linspace(0, 179, 180) * 2 * np.pi / 180
	width = 2*np.pi / 360

	ax = plt.subplot(111, polar = True)
	bars = ax.bar(hue_rad, count, width=width)

	plt.show()


# Farthest Point Sampling
def fps(array):
	return(None)

# Total random selection of centroids
def select_centroids(image_array, num_centroids):

	# Reshape 3D array into 2D, with the first dimension being having shape [num_pixels]
	num_pixels = reshape_image(image_array)[0]
	image_reshaped = reshape_image(image_array)[1]

	# Randomly select location indices in image_array
	indices = random.sample(range(0, num_pixels), num_centroids)

	random_centroids = image_reshaped[indices]

	return(random_centroids)

#def kmc(image_array, random_centroids):

#init_centroid = select_centroids(hsv_image, 5)
hue_circular_plot(hsv_image)


