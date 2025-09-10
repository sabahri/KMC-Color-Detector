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


##### The commented numbers are expected results for utah_sunset.jpg

import cv2
import numpy as np
import random
import matplotlib.pyplot as plt
import sys

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
import matplotlib.gridspec as gridspec

# Saving all color space conversions into 'flags' variable
flags = [i for i in dir(cv2) if i.startswith('COLOR_')]

# Specify number of iterations to use for K-means cluster algorithm
# Import image from path file and convert from BGR to RGB format

num_iter = int(sys.argv[1])
input_image = sys.argv[2]

original_image = cv2.imread(input_image)

# 2736 x 3648 x 3 array
original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)		

# Reducing to 5% of image resolution to speed up color splitting
# 27 x 36 x 3 array
reduced_image = cv2.resize(original_image, (0,0), fx=0.01, fy=0.01, interpolation=cv2.INTER_AREA)
hsv_image = cv2.cvtColor(reduced_image, cv2.COLOR_RGB2HSV)

#########################################
############ Comparing Photos ###########
#########################################

Titles = ["Original", "Resized to 1%"] #, "Canny Edge Detection"]
images = [original_image, reduced_image] #, edges]
count = len(images)

plt.figure()

for i in range(count):
	plt.subplot(1, len(images), i+1)
	plt.title(Titles[i])
	plt.imshow(images[i])

plt.tight_layout

##################################
######### Scatter Plots ##########
##################################

# Facecolors
hgt, wth, chn = reduced_image.shape

pixel_colors = reduced_image.reshape(hgt * wth, chn)
norm = colors.Normalize(vmin = 1., vmax = 1.)
norm.autoscale(pixel_colors)					# 972 x 3 array
pixel_colors = norm(pixel_colors).tolist()		# 972 x 3 list

# Split image into component channels (RGB, HSV respectively)

r, g, b = cv2.split(reduced_image)	
h, s, v = cv2.split(hsv_image)

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

##############################################
############ K-means Clustering ##############
##############################################

# 1. Randomly select k cluster centroids       							### Done					
# 2. Assign each data point to the nearest centroid to form clusters	### Done
# 3. Recalculate centroid by averaging points (update step)				### Done
# 4. Repeat until convergence

### Note: maybe add a function to maximize the distance between centroids in hue space ###
### Are there any existing algorithms that do this efficiently? ###
### This may end up being problematic for values close to 0 / 180 in the "red" space ###

# image_array is the 1% reduced image (shape = h(pixels) x w(pixels) x 3(color channels))

def reshape_image(image_array):
	height, width, c_channels = image_array.shape

	# Total number of pixels
	num_pixels = height * width

	# Reshape 3D array into 2D, with the first dimension being having shape [num_pixels]
	image_reshaped = np.reshape(image_array, [num_pixels, c_channels])

	return(num_pixels, image_reshaped)

# Plotting histogram of Hues in the image, normal and circular representations

def hue_range(array):
	image_reshaped = reshape_image(array)[1]
	hue = image_reshaped[:,0]

	count = np.zeros(180)

	for i in range(hue.shape[0]):
		for j in range(180):
			if hue[i] == j:
				count[j] += 1
	
	#hues_opencv = np.linspace(0, 179, 180)
	#plt.scatter(hues_opencv, count, color = 'lightgreen', edgecolor = 'black')
	#plt.hist(hue,180, color='lightgreen', edgecolor = 'black')
	#plt.xlabel('Hue')
	#plt.ylabel('Count')
	#plt.title('Hue Distribution in Image')
	#plt.show()
	
	return(hue, count)

def hue_circular_hist(array):

	# note, in OpenCV the hue range is from 0 to 180
	# so all hue values must be doubled to fit onto a cylindrical plot

	hue = hue_range(array)[0] * 2
	count = hue_range(array)[1]

	hue_rad = np.linspace(0, 179, 180) * 2 * np.pi / 180
	width = 2*np.pi / 360

	ax = plt.subplot(111, polar = True)
	bars = ax.bar(hue_rad, count, width=width, color = 'lightgreen', edgecolor = 'black')

	plt.title('Circular Representation of Hue Histogram')

# Farthest Point Sampling
def fps(array):
	return(None)

# Total random selection of centroids
# Centroids here are pixels, not hues
# num_centroids is the number of clusters to aim for (integer)
def init_centroids(image_array, num_centroids):

	# Reshape 3D array into 2D, with the first dimension being having shape [num_pixels]
	num_pixels = reshape_image(image_array)[0]
	image_reshaped = reshape_image(image_array)[1]

	# Randomly select location indices in image_array
	indices = random.sample(range(0, num_pixels), num_centroids)

	# random_centroids are the HSV values of the randomly selected pixels
	random_centroids = np.zeros((num_centroids, 3))
	
	for i,j in zip(range(num_centroids),indices):
		random_centroids[i,:] = image_reshaped[j]

	return(indices, random_centroids)

def euclidean_pixels(image_array, num_centroids, centroids):

	# Calculating the L2 norm

	# euclidean.shape =  num_pixels x num_centroids (972 x 5)
	# image_reshaped.shape = num_pixels x c_channels (972 x 3)
	# num_centroids = 5
	# centroids.shape = num_centroids x c_channels (5 x 3)

	# Note: num_pixels = image_reshaped.shape[0]
	num_pixels, image_reshaped = reshape_image(image_array)

	euclidean = np.zeros((num_pixels, num_centroids))

	for i in range(num_pixels):
		for j in range(num_centroids):
			euclidean[i,j] = np.linalg.norm(image_reshaped[i] - centroids[j])

	return(euclidean)

def kmc(image_array, num_centroids, centroids):

	# num_pixels = 972
	# image_reshaped.shape = num_pixels x c_channels (972 x 3)
	num_pixels, image_reshaped = reshape_image(image_array)

	# euclidean.shape =  num_pixels x num_centroids (972 x 5)
	euclidean = euclidean_pixels(image_array, num_centroids, centroids)
	min_array = np.zeros((num_pixels, num_centroids))

	# Creating a min_array "mask": ones and zeros matrix to locate
	# closest centroid

	for i in range(num_pixels):
		for j in range(num_centroids):
			if euclidean[i,j] == min(euclidean[i,:]):
				min_array[i,j] = 1
			else:
				min_array[i,j] = 0

	# Updating the centroid location
	# Reminder: centroid is a specific pixel with HSV values
	# Euclidean distance minimization is looking for pixels with similar HSV values
	# When we select a new centroid, we want to updated the average HSV values, 
	# not pixel location

	min_array = min_array.transpose()
	total_count = min_array.sum(axis = 1)[:,None]
	total_count = np.asarray(total_count, dtype='int')

	average_hsv = (min_array @ image_reshaped) / total_count

	average_hsv = np.asarray(average_hsv, dtype='int')

	return(average_hsv, total_count)


################################################
######### Running K-means Clustering ###########
################################################

def sort_centroids(imfile, num_centroids, total_count):
	# Flattening the total counts array
	tot = total_count.reshape(num_centroids)

	# Sorting colors in descending order
	totals_indices = tot.argsort()
	sorted_totals = tot[totals_indices[::-1]]
	sorted_colors = imfile[totals_indices[::-1]]

	return(sorted_colors)

n_centroids = 10
indices_0, centroids_0 = init_centroids(hsv_image, n_centroids)

#plt.ion()
plt.figure()

# Initiating with random centroid selection

n = 0
centroid_update, totals_array = kmc(hsv_image, n_centroids, centroids_0)

#figure, ax = plt.subplots(figsize=(10,8))
#line1, = ax.plot()

for n in range(1, num_iter):
	centroid_update, totals_array = kmc(hsv_image, n_centroids, centroid_update)
		
	centroid_hsv = cv2.merge(centroid_update)	# 3 x 1 x 10 array
	centroid_hsv = np.transpose(centroid_hsv)	# 10 x 1 x 3 array
	centroid_hsv = centroid_hsv.astype(np.uint8)

	frequent_colors = sort_centroids(centroid_hsv, n_centroids, totals_array)

	#figure.canvas.draw()
	#figure.canvas.flush_events()

plt.imshow(frequent_colors)
plt.show()



