"""
masks
* tissue: `get_tissue_mask()`
* ihc: `get_ihc_mask()`
misc
* `ihc_stain_fraction()`
* `stain_alteration()`
"""
import random
import numpy as np
import cv2 as cv
from skimage.color import rgb2hed
from sklearn.feature_extraction.image import extract_patches_2d
import matplotlib.pyplot as plt
import gc



def get_tissue_mask(I, luminosity_threshold=0.8):
    """Get a binary mask where true denotes pixels with a luminosity less than the specified threshold
    Typically we use to identify tissue in the image and exclude the bright white background.
    Parameters
    ----------
    I : np.ndarray
        RGB uint 8 image with RGB colorspace shape (x, y, 3)
    luminosity_threshold : float
        Luminosity threshold above which is considered tissue
    Returns
    -------
    tissue_mask: np.ndarray
        boolean mask shape (x, y) 
    """
    # assert is_uint8_image(I), "Image should be RGB uint8."
    I_LAB = cv.cvtColor(I, cv.COLOR_RGB2LAB)
    L = I_LAB[:, :, 0] / 255.0  # Convert to range [0,1].
    mask = L < luminosity_threshold

    return mask


def get_ihc_mask(img):
    """Generate a binary mask denoting locations on an image containing IHC stain
    
    Parameters
    ----------
    img : np.ndarray
        IHC image represented as a numpy array with rgb colorspace and shape (x, y, 3)
    min: float
        threshold for a pixel to be considered as IHC positive (default -0.35)
    
    Returns
    -------
    ihc_mask: np.ndarray
        array with third axis removed and binary values indicating location of IHC
        shape: (img.shape[0], img.shape[1])
    """
    ihc_img = rgb2hed(img)
    ihc_mask = np.where(ihc_img[:,:,2]>-0.35, 1, 0)

    return ihc_mask


def ihc_stained_fraction(img):
    """measure the percentage of tissue on an IHC image that contains peroxide
    
    Parameters
    ----------
    img : np.ndarray
        IHC image represented as a numpy array with rgb colorspace and shape (x, y, 3)
    
    Returns
    -------
    percent_tissue_ihc : float
    Notes
    -----
    this function wraps `get_tissue_mask()` and `get_ihc_mask()` to compute this stat
    """
    tissue_mask = get_tissue_mask(img)
    ihc_mask = get_ihc_mask(img)

    return ihc_mask.sum()/tissue_mask.sum()


def ihc_stain_intensity(img):
    """measure the average intensity of IHC in pixels containing IHC
    
    Parameters
    ----------
    img : np.ndarray
        IHC image represented as a numpy array with rgb colorspace and shape (x, y, 3)
    Returns
    -------
    ihc_stain_intensity : float
    """
    hed_img = rgb2hed(img)
    ihc_mask = np.where(hed_img[:,:,2]>-0.35, 1, 0)
    ihc_pixel_intensities = hed_img[:,:,2][ihc_mask == 1]
    return ihc_pixel_intensities.mean()


def stain_alteration(image, a_min=0.9, a_max=1.1, b_min=-0.039, b_max=0.039):
    # simple H&E color augmentation based on https://arxiv.org/pdf/1707.06183.pdf
    # intended to alter staining in training data for more robust models
    image = image * np.random.uniform(a_min, a_max, image.shape) + np.random.uniform(b_min, b_max, image.shape)
    return image

def patch_generator(img, patch_size, n_patches=20, ihc_stain_filter=False, filename='file.jpg', output_dir=None):
	patch_list = list(extract_patches_2d(img, patch_size, max_patches=0.0001, random_state=2019))
	patch_list_filtered = [patch for patch in patch_list if get_tissue_mask(patch).mean() > 0.5]

	if ihc_stain_filter:
		patch_list_filtered = [patch for patch in patch_list if get_ihc_mask(patch).mean() > 0.1]

	random.shuffle(patch_list_filtered)
	patch_list_filtered = patch_list_filtered[:n_patches]

	if output_dir:
		i = 1
		for patch in patch_list_filtered:
			fig = plt.imshow(patch)
			plt.axis('off')
			fig.axes.get_xaxis().set_visible(False)
			fig.axes.get_yaxis().set_visible(False)
			plt.savefig("{}/{}".format(output_dir, filename.split('.')[0] +'_'+str(i)+'.jpg'), bbox_inches='tight', pad_inches = 0)
			plt.clf()
			plt.close()
			gc.collect()
			i+=1

	return patch_list_filtered