from config import config, session
import os
import matplotlib.pyplot as plt
import gc
import tempfile
import skimage.io

# ID Utils ----
# AWS id grammer:
# url = AWS_HOSTNAME + path
def is_url(x):
    """predicate test for url
    """
    AWS_HOSTNAME="https://krzysztof-images.s3.amazonaws.com/"

    lgl = x.startswith(AWS_HOSTNAME)
    return lgl


def is_path(x):
    lgl = x.startswith("hpa_images/")
    return lgl


def url_2_path(x):
    """Truncate AWS URL to the Path
    Parameters
    ----------
    x: str
    Returns
    -------
    str with path component only
    Examples
    --------
    url_2_path("https://krzysztof-images.s3.amazonaws.com/hpa_images/RPE/HPA036498/healthy_tissue/kidney/hpa_patient_2089/74260_A_7_5.jpg")
    'hpa_images/RPE/HPA036498/healthy_tissue/kidney/hpa_patient_2089/74260_A_7_5.jpg'
    """
    AWS_HOSTNAME="https://krzysztof-images.s3.amazonaws.com/"
    path = x.replace(AWS_HOSTNAME, "")
    return(path)


def path_2_wsi_id(x):
    """Extract the wsi id from an aws path
    Parameters
    ----------
    x: str
    Returns
    -------
    x: str
    """
    assert is_path(x[0])
    fns =[os.path.basename(url) for url in x]
    wsi_ids = [fn.replace(".jpg", "") for fn in fns]
    return wsi_ids

def img_load(fp):
    """Load image from local fs
    Parameters
    ----------
    fp: str
        path to image file
    Returns
    -------
    numpy.ndarray (w, h, channels) or None
    Notes
    -----
    engine: `skimage.io.imread()`
    """
    try:
        img = skimage.io.imread(fp)
    except:
        print("Unable to read {}".format(fp))
        return None

    return img

# def patch_generator(img, patch_size, ihc_stain_filter=False):
# 	"""
# 	input a skimage object and get a list of patches in return
# 	"""
# 	patch_list = list(extract_patches_2d(img, patch_size, max_patches=0.00001, random_state=2019))
# 	patch_list_filtered = [patch for patch in patch_list if get_tissue_mask(patch).mean()>0.5]
#
# 	if ihc_stain_filter:
# 		patch_list_filtered = [patch for patch in patch_list if np.where(rgb2hed(patch)[:,:,2]>-0.8, 1, 0).mean()>0.1]
#
# 	random.shuffle(patch_list_filtered)
# 	patch_list_filtered = patch_list_filtered[:50]
#
# 	return patch_list_filtered


def save_patch(patch, patch_name, output_dir):
	fig = plt.imshow(patch)
	plt.axis('off')
	fig.axes.get_xaxis().set_visible(False)
	fig.axes.get_yaxis().set_visible(False)
	plt.savefig("{}/{}".format(output_dir, patch_name+'.jpg'), bbox_inches='tight', pad_inches = 0)
	plt.clf()
	plt.close()
	gc.collect()

def img_load_aws(path, session = session, host = config['aws_host'], bucket = config['aws_bucket_name']):
    """Load image from aws
    Parameters
    ----------
    path: str
        aws path (w/ or w/o prepended hostname)
    Returns
    -------
    numpy.ndarray (w, h, channels) or None
    Notes
    -----
    implemented via tempfile intermediate and `img_load()`
    Raises
    ------
    with file not found on AWS server or temp file unloadable, 
    print url and return None
    Examples
    --------
    img_load_aws('hpa_images/RPE/HPA036498/healthy_tissue/kidney/hpa_patient_2089/74260_A_7_5.jpg').shape
    (3000, 3000, 3)
    """
    # precondition
    if is_url(path):
        path = url_2_path(path)
        print("Coercing AWS URL {}".format(path))

    # aws
    s3 = session.resource('s3', region_name=host)
    bucket = s3.Bucket(bucket)

    # MAIN
    # temp file intermediate
    object = bucket.Object(path)
    tmp_img = tempfile.NamedTemporaryFile()

    try:
        with open(tmp_img.name, 'wb') as f:
            object.download_fileobj(f)
    except:
        print("Unable to download url {}".format(path))
        return None

    img = img_load(tmp_img.name)
    return img