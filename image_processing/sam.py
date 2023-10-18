import numpy as np
import matplotlib.image as mpimg


# removes all shades of grey from a black-and-white image and creates a new file
# that contains the updated image in array format

img = mpimg.imread('./sam.jpg')  # reads an image file and converts it to an array
img_normalized = -1 * np.array(img) / 255  # normalizes the array to [-1, 0] length scale

# replaces all values with either -1 or 1, whichever is closer, so the array looks like a system
# suitable for Ising model
img_ising = 2 * img_normalized.astype(int) + 1

np.savetxt('test.txt', img_ising, fmt='%d', delimiter=',')  # saves the updated array to a new file
