# INVOKE (app name in progress)

# Program for color detection
# Useful Links:
# https://realpython.com/python-opencv-color-spaces/
# https://www.timpoulsen.com/2018/finding-the-dominant-colors-of-an-image.html

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

import sys
import cv2
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import warnings
import math

from matplotlib import cm
from matplotlib import colors
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D

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

# Increasing pixel percentage increases final color accuracy but also runtime
perc = 0.01
reduced_image = cv2.resize(original_image, (0,0), fx=perc, fy=perc, interpolation=cv2.INTER_AREA)
hsv_image = cv2.cvtColor(reduced_image, cv2.COLOR_RGB2HSV)

#########################################
############ Some Useful FXNS ###########
#########################################

# Converting colors from HSV to RGB for making figures
def convert_colors(average_hsv):
	average_hsv = np.asarray(average_hsv, dtype='uint8')
	# Adding dimension
	average_hsv = average_hsv[:,None,:]
	# Convert back to 8 unsigned integer format
	array_hsv = average_hsv.astype(np.uint8)
	# Convert from HSV back to RGB
	array_rgb = cv2.cvtColor(array_hsv, cv2.COLOR_HSV2RGB)

	return(array_rgb)

# HSV array with Saturation and Value set to 255
def h_255_255(hues_array):
	hues_array = np.unique(hues_array)
	num_hues = hues_array.shape[0]

	hues_opencv = np.zeros((num_hues,3))
	for i in range(num_hues):
		hues_opencv[i][0] = hues_array[i] + 1
		hues_opencv[i][1:3] = 255

	return(hues_opencv)

def sort_centroids(imfile, num_centroids, total_count):
	# Flattening the total counts array
	tot = total_count.reshape(num_centroids)

	totals_indices = tot.argsort()

	# Sorting colors in descending order
	sorted_totals = tot[totals_indices[::-1]]
	sorted_colors = imfile[totals_indices[::-1]]

	return(sorted_colors)

def sort_arrays(arr1, arr2):
	arr1_indices = arr1.argsort()
	arr1_sorted = arr1[arr1_indices]
	arr2_sorted = arr2[arr1_indices]

	return(arr1_sorted, arr2_sorted)

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

red, grn, blu = cv2.split(reduced_image)	
hue, sat, val = cv2.split(hsv_image)

# Subplots Setup

fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1, projection = "3d")

# RGB Scatter Plot

ax1.scatter(red.flatten(), grn.flatten(), blu.flatten(), facecolors=pixel_colors, marker='.')
ax1.set_xlabel("Red")
ax1.set_ylabel("Green")
ax1.set_zlabel("Blue")

# HSV Scatter Plot

ax2 = fig.add_subplot(1, 2, 2, projection = "3d")
ax2.scatter(hue.flatten(), sat.flatten(), val.flatten(), facecolors=pixel_colors, marker='.')
ax2.set_xlabel("Hue")
ax2.set_ylabel("Saturation")
ax2.set_zlabel("Value")

##############################################
############ K-means Clustering ##############
##############################################

# 1. Randomly select k cluster centroids       							### Done					
# 2. Assign each data point to the nearest centroid to form clusters	### Done
# 3. Recalculate centroid by averaging points (update step)				### Done
# 4. Repeat until convergence											### Done

# 5. Set cutoff for Euclidean distances to improve color accuracy
# 6. Farthest point sampling to increase chances of color diversity
# 7. Final color palette should exclude color of similar hues (?)
# 8. Deal with reds (hue circle freq discrimination?)

# image_array is the 1% reduced image (shape = h(pixels) x w(pixels) x 3(color channels))

def reshape_image(image_array):
	height, width, c_channels = image_array.shape

	# Total number of pixels
	num_pixels = height * width

	# Reshape 3D array into 2D, with the first dimension being having shape [num_pixels]
	image_reshaped = np.reshape(image_array, [num_pixels, c_channels])

	return(num_pixels, image_reshaped)

def hue_range(image_array):
	image_reshaped = reshape_image(image_array)[1]
	h = image_reshaped[:,0]

	count = np.zeros(180)

	for i in range(h.shape[0]):
		for j in range(180):
			if h[i] == j:
				count[j] += 1

	return(h, count)

###############################################################
# Creating a custom colormap for better histogram visualization

x_hues = hue_range(hsv_image)[0]
x_hues_unique = np.unique(x_hues)
x_hues_255_255 = h_255_255(x_hues_unique)
x_hues_rgb = np.squeeze(convert_colors(x_hues_255_255) / 255)

cmap = colors.ListedColormap(x_hues_rgb)

plt.figure()

n, bins, patches = plt.hist(x_hues,180, color='lightgreen', edgecolor = 'black')
plt.xlabel('Hue, OpenCV Format')
plt.ylabel('Pixel Count per Hue')
plt.title('Hue Distribution with Saturation and Value set to 255')

for i, p in enumerate(patches):
	color = cmap(i / len(patches))
	plt.setp(p, 'facecolor',color)

################################################################

def hue_circular_hist(array):

	# note, in OpenCV the hue range is from 0 to 180
	# so all hue values must be doubled to fit onto a cylindrical plot

	hues = hue_range(array)[0] * 2
	count = hue_range(array)[1]

	hue_rad = np.linspace(0, 179, 180) * 2 * np.pi / 180
	width = 2.5*np.pi / 360

	ax = plt.subplot(111, polar = True)	
	bars = ax.bar(hue_rad, count, width=width, color = 'lightgreen')

	plt.title('Circular Representation of Hue Histogram')

# plt.figure()
# hue_circular_hist(hsv_image)

# Farthest Point Sampling
def fps(array):

	centroid_360 = array[0,:] * 2


	return(None)

# Total random selection of centroids
# Centroids here are pixels, not hues, as a proxy for initiating HSV values
# num_centroids is the number of clusters to aim for (integer)
def init_centroids(image_array, num_centroids):

	# Reshape 3D array into 2D, with the first dimension being having shape [num_pixels]
	num_pixels, image_reshaped = reshape_image(image_array)

	# Randomly select location indices in image_array
	indices = random.sample(range(0, num_pixels), num_centroids)

	# random_centroids are the HSV values of the randomly selected pixels
	random_centroids = np.zeros((num_centroids, 3))
	
	for i,j in zip(range(num_centroids),indices):
		random_centroids[i,:] = image_reshaped[j]

	#random_centroids = np.asarray(random_centroids, dtype='int')
	return(indices, random_centroids)

def init_single_centroid(image_array):
	# Reshape 3D array into 2D, with the first dimension being having shape [num_pixels]
	num_pixels, image_reshaped = reshape_image(image_array)

	index = random.randrange(0,num_pixels,1)

	single_centroid = image_reshaped[index]

	return(single_centroid)

def distance_hsv(image_array, num_centroids, centroids):

	# Calculating the L2 norm in cylindrical coordinates

	# d.shape =  num_pixels x num_centroids (972 x 5)
	# image_reshaped.shape = num_pixels x c_channels (972 x 3)
	# num_centroids = 5
	# centroids.shape = num_centroids x c_channels (5 x 3)

	# Note: num_pixels = image_reshaped.shape[0]
	num_pixels, image_reshaped = reshape_image(image_array)

	d = np.zeros((num_pixels, num_centroids))

	for i in range(num_pixels):
		for j in range(num_centroids):
			h1, s1, v1 = image_reshaped[i]
			h2, s2, v2 = centroids[j]

			hue_diff = np.abs(2*(h1 - h2))
			theta = hue_diff * np.pi / 180

			s1, s2, v1, v2 = s1/255, s2/255, v1/255, v2/255
			d[i,j] = s1**2 + s2**2 - 2*s1*s2*math.cos(theta) + (v1 - v2)**2

			d[i,j] = math.sqrt(d[i,j])

	return(d)

def circular_mean(hues):
	hues = 2*hues * np.pi/180	# radians
	sin_sum = np.sum([np.sin(h) for h in hues])
	cos_sum = np.sum([np.cos(h) for h in hues])

	mean_hues = np.atan2(sin_sum, cos_sum)

	return(mean_hues)

def kmc(image_array, num_centroids, centroids):

	# num_pixels = 972
	# image_reshaped.shape = num_pixels x c_channels (972 x 3)
	# d.shape =  num_pixels x num_centroids (972 x 5)
	num_pixels, image_reshaped = reshape_image(image_array)
	d = distance_hsv(image_array, num_centroids, centroids)

	closest_centroid = np.argmin(d, axis=1) # 1 x num_pixels

	counts = np.bincount(closest_centroid, minlength=num_centroids)  # 1 x 5

	average_h = np.zeros((num_centroids, 1))

	for i in range(num_centroids):				# 5
		close_hues = []
		for cc in range(num_pixels):		# 900
			if closest_centroid[cc] == i:
				close_hues.append(image_reshaped[cc][0])

		average_h[i] = circular_mean(np.array(close_hues))


	average_sv = np.zeros((num_centroids, 2))

	for i in range(num_centroids):
		for j in range(image_reshaped.shape[0]):
			if closest_centroid[j] == i:
				average_sv[i,:] += image_reshaped[j,-2:]

	average_hsv = np.hstack([average_h, average_sv])

	for k in range(num_centroids):
		if counts[k] == 0:
			average_hsv[k,:] = init_single_centroid(image_array)
			counts[k] = 1
	
	average_sv = average_sv / counts[:,None]

	return(average_hsv, counts, num_centroids)

################################################
######### Running K-means Clustering ###########
#########  And Plotting the Results  ###########
################################################

# Initiating with random centroid selection

n_centroids = 20
# Randomly select first 10 centroids
indices_0, centroids_0 = init_centroids(hsv_image, n_centroids)

centroid_update, totals_array, n_centroids = kmc(hsv_image, n_centroids, centroids_0)

#for n in range(num_iter):
for n in range(num_iter):
	centroid_update, totals_array, n_centroids = kmc(hsv_image, n_centroids, centroid_update)
	centroid_rgb =  convert_colors(centroid_update)
	frequent_colors = sort_centroids(centroid_rgb, n_centroids, totals_array)

Titles = ["Original", "Color Story"]
images2 = [original_image, frequent_colors]
count = len(images2)

plt.figure()

for i in range(count):
	plt.subplot(1, len(images2), i+1)
	plt.title(Titles[i])
	plt.imshow(images2[i])

plt.tight_layout

try:
	plt.show()
except KeyboardInterrupt:
	sys.exit(0)
