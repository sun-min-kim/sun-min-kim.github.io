# CS180: Project 1 Image Alignment

import os
import glob
import numpy as np
import skimage as sk
import skimage.io as skio

data = "CS180_fa2026_proj1_data"

#---Single Scale Alignment---
output = "single_scale_alignment"
os.makedirs(output, exist_ok=True)

# Crop the images
def crop(im, ratio=0.85):
    print(f"Cropping...")
    height, width = im.shape
    cropped_height = int((1 - ratio) * height / 2)
    cropped_width = int((1 - ratio) * width / 2)
    print("Cropped")
    return im[cropped_height:height - cropped_height, cropped_width:width - cropped_width]


window = 15
# align the images
# functions that might be useful for aligning the images include:
# np.roll, np.sum, sk.transform.rescale (for multiscale)
def align(im1, im2):
    print(f"Aligning...")
    best = np.inf
    best_change_x, best_change_y = 0, 0

    for x in range(-window, window + 1):
        for y in range(-window, window + 1):
            shifted = np.roll(im1, (x, y), axis = (0, 1))
            score = np.sqrt(np.sum(np.sum((shifted - im2) ** 2)))
            if score < best:
                best = score
                best_change_x = x
                best_change_y = y

    aligned_im = np.roll(im1, (best_change_x, best_change_y), axis = (0, 1))
    return aligned_im, best_change_x, best_change_y


def single_scale_alignment(imname):
    image_name = os.path.basename(imname)
    print(f"---Aligning {image_name}...---")
    # read in the image
    im = skio.imread(imname)

    # convert to double (might want to do this later on to save memory)    
    im = sk.img_as_float(im)

        
    # compute the height of each part (just 1/3 of total)
    height = np.floor(im.shape[0] / 3.0).astype(int)

    # separate color channels
    b = im[:height]
    g = im[height: 2*height]
    r = im[2*height: 3*height]

    b, g, r = crop(b), crop(g), crop(r)

    ag, ag_x, ag_y = align(g, b)
    ar, ar_x, ar_y = align(r, b)

    log_path = f"{output}/alignment_log.txt"
    with open(log_path, "a") as f:
        f.write(f"{image_name}: Green = ({ag_x}, {ag_y}), Red = ({ar_x}, {ar_y})\n")

    # create a color image
    im_out = np.dstack([ar, ag, b])
    im_out = np.clip(im_out, 0, 1)
    im_out = sk.img_as_ubyte(im_out)

    # save the image
    fname = f"{output}/{image_name}"
    skio.imsave(fname, im_out)
    print(f"---Aligned {image_name}---")


# Single scale alignment on .jpg images
open(f"{output}/alignment_log.txt", "w").close()
print("------SINGLE SCALE ALIGNMENT------")
for imname in glob.glob(os.path.join(data, "*.jpg")):
    single_scale_alignment(imname)


#---Pyramid Alignment---
output = "pyramid_alignment"
os.makedirs(output, exist_ok=True)
min_dimension = 350

# Scale image down and align
def pyramid(im1, im2):
    print("Pyramiding...")
    height, width = im1.shape

    if height < min_dimension or width < min_dimension:
        _, best_change_x, best_change_y = align(im1, im2)
        return best_change_x, best_change_y
    im1_rescaled = sk.transform.rescale(im1, 0.5)
    im2_rescaled = sk.transform.rescale(im2, 0.5)

    best_change_x, best_change_y = pyramid(im1_rescaled, im2_rescaled)
    cur_change_x, cur_change_y = best_change_x * 2, best_change_y * 2

    im1_rolled = np.roll(im1, (cur_change_x, cur_change_y), axis = (0, 1))
    # Compare caorser image with current image
    _, change_x, change_y = align(im1_rolled, im2)
    change_x = change_x + cur_change_x
    change_y = change_y + cur_change_y
    print(f"Aligned: {change_x}, {change_y}")
    print("Pyramided")
    return change_x, change_y


# Pyramid alignment
def pyramid_alignment(imname):
    image_name = os.path.splitext(os.path.basename(imname))[0]
    print(f"---Aligning {image_name}...---")
    # read in the image
    im = skio.imread(imname)

    # convert to double (might want to do this later on to save memory)    
    im = sk.img_as_float(im)
        
    # compute the height of each part (just 1/3 of total)
    height = np.floor(im.shape[0] / 3.0).astype(int)

    # separate color channels
    b = im[:height]
    g = im[height: 2*height]
    r = im[2*height: 3*height]

    b, g, r = crop(b), crop(g), crop(r)

    change_x, change_y = pyramid(g, b)

    # Shift green and red images
    ag = np.roll(g, (change_x, change_y), axis=(0, 1))
    ag_x = change_x
    ag_y = change_y
    print(f"Green shift: {change_x}, {change_y}")

    change_x, change_y = pyramid(r, b)
    ar = np.roll(r, (change_x, change_y), axis=(0, 1))
    ar_x = change_x
    ar_y = change_y
    print(f"Red shift: {change_x}, {change_y}")

    log_path = f"{output}/alignment_log.txt"
    with open(log_path, "a") as f:
        f.write(f"{image_name}: Green = ({ag_x}, {ag_y}), Red = ({ar_x}, {ar_y})\n")

    # create a color image
    im_out = np.dstack([ar, ag, b])
    im_out = np.clip(im_out, 0, 1)
    im_out = sk.img_as_ubyte(im_out)

    # save the image
    fname = f"{output}/{image_name}.jpg"
    skio.imsave(fname, im_out)
    print(f"---Aligned {image_name}---")

# Pyramid alignment on all images
open(f"{output}/alignment_log.txt", "w").close()
print("------PYRAMID ALIGNMENT------")
for imname in glob.glob(os.path.join(data, "*.tif")) + glob.glob(os.path.join(data, "*.jpg")):
    pyramid_alignment(imname)