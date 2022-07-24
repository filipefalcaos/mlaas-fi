import warnings
import numpy as np

from PIL import Image
from skimage.color import rgb2gray
from skimage.io import imsave, imread
from skimage.util import img_as_ubyte, random_noise

from .utils import apply_img_corruption, apply_weather_mask


def gaussian_blur(image_path, new_image_path, severity=1):
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        apply_img_corruption(image_path, new_image_path, 'gaussian_blur', severity)


def motion_blur(image_path, new_image_path, severity=1):
    apply_img_corruption(image_path, new_image_path, 'motion_blur', severity)


def zoom_blur(image_path, new_image_path, severity=1):
    apply_img_corruption(image_path, new_image_path, 'zoom_blur', severity)


def gaussian_noise(image_path, new_image_path, severity=1):
    apply_img_corruption(image_path, new_image_path, 'gaussian_noise', severity)


def sp_noise(image_path, new_image_path, severity=1):
    apply_img_corruption(image_path, new_image_path, 'impulse_noise', severity)


def condensation(image_path, new_image_path):
    apply_weather_mask(image_path, new_image_path, 'condensation')


def fog(image_path, new_image_path, severity=1):
    apply_img_corruption(image_path, new_image_path, 'fog', severity)


def frost(image_path, new_image_path):
    apply_weather_mask(image_path, new_image_path, 'frost')


def rain_snow(image_path, new_image_path, severity=1):
    apply_img_corruption(image_path, new_image_path, 'snow', severity)


def brightness(image_path, new_image_path, severity=1):
    apply_img_corruption(image_path, new_image_path, 'brightness', severity)


# Implements simple chromatic aberration by altering the g and b channels of the image
# Modification of https://github.com/yoonsikp/kromo
def chromatic_aberration(image_path, new_image_path, factor=1):
    img = Image.open(image_path)

    r, g, b = img.split()
    rdata = np.asarray(r)

    # Apply the chromatic aberration
    gfinal = g.resize((round((1 + 0.018 * factor) * rdata.shape[1]),
                       round((1 + 0.018 * factor) * rdata.shape[0])), Image.ANTIALIAS)
    bfinal = b.resize((round((1 + 0.044 * factor) * rdata.shape[1]),
                       round((1 + 0.044 * factor) * rdata.shape[0])), Image.ANTIALIAS)

    rwidth, rheight = r.size
    gwidth, gheight = gfinal.size
    bwidth, bheight = bfinal.size
    rhdiff = (bheight - rheight) // 2
    rwdiff = (bwidth - rwidth) // 2
    ghdiff = (bheight - gheight) // 2
    gwdiff = (bwidth - gwidth) // 2

    # Centre the channels
    new_img = Image.merge('RGB', (
        r.crop((-rwdiff, -rhdiff, bwidth - rwdiff, bheight - rhdiff)),
        gfinal.crop((-gwdiff, -ghdiff, bwidth - gwdiff, bheight - ghdiff)),
        bfinal))
    new_img = new_img.crop((rwdiff, rhdiff, rwidth + rwdiff, rheight + rhdiff))

    new_img.save(new_image_path)


def contrast(image_path, new_image_path, severity=1):
    apply_img_corruption(image_path, new_image_path, 'contrast', severity)


def defective_pixels(image_path, new_image_path, count=1):
    img = imread(image_path)
    total_pixels = img.shape[0] * img.shape[1]
    proportion = count / total_pixels
    img_noise = img_as_ubyte(random_noise(img, mode='pepper', clip=True, amount=proportion))
    imsave(new_image_path, img_noise)


def grayscale(image_path, new_image_path):
    img = imread(image_path)
    img_grayscale = img_as_ubyte(rgb2gray(img))
    imsave(new_image_path, img_grayscale)


def pixelation(image_path, new_image_path, severity=1):
    apply_img_corruption(image_path, new_image_path, 'pixelate', severity)
