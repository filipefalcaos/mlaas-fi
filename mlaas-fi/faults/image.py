import numpy as np
from imagecorruptions import corrupt
from PIL import Image, ImageEnhance
from pkg_resources import resource_filename
from skimage.color import rgb2gray
from skimage.filters import gaussian
from skimage.io import imsave, imread
from skimage.util import img_as_ubyte, random_noise


def apply_blur(image_path, new_image_path, sd=1):
    img = imread(image_path)
    img_blurred = img_as_ubyte(gaussian(img, sigma=sd, multichannel=True))
    imsave(new_image_path, img_blurred)


def apply_brightness(image_path, new_image_path, factor=1):
    img = Image.open(image_path)
    img_noise = ImageEnhance.Brightness(img).enhance(factor)
    img_noise.save(new_image_path)


# Modification of https://github.com/yoonsikp/kromo
def apply_chromatic_aberration(image_path, new_image_path, strength=1):
    img = Image.open(image_path)
    r, g, b = img.split()
    rdata = np.asarray(r)

    # Apply the chromatic aberration
    gfinal = g.resize((round((1 + 0.018 * strength) * rdata.shape[1]),
                       round((1 + 0.018 * strength) * rdata.shape[0])), Image.ANTIALIAS)
    bfinal = b.resize((round((1 + 0.044 * strength) * rdata.shape[1]),
                       round((1 + 0.044 * strength) * rdata.shape[0])), Image.ANTIALIAS)

    rwidth, rheight = r.size
    gwidth, gheight = gfinal.size
    bwidth, bheight = bfinal.size
    rhdiff = (bheight - rheight) // 2
    rwdiff = (bwidth - rwidth) // 2
    ghdiff = (bheight - gheight) // 2
    gwdiff = (bwidth - gwidth) // 2

    # Centre the channels
    new_img = Image.merge("RGB", (
        r.crop((-rwdiff, -rhdiff, bwidth - rwdiff, bheight - rhdiff)),
        gfinal.crop((-gwdiff, -ghdiff, bwidth - gwdiff, bheight - ghdiff)),
        bfinal))
    new_img = new_img.crop((rwdiff, rhdiff, rwidth + rwdiff, rheight + rhdiff))

    new_img.save(new_image_path)


def apply_gaussian_noise(image_path, new_image_path, mean=0, sd=0.1):
    img = imread(image_path)
    img_noise = img_as_ubyte(random_noise(img, mode="gaussian", clip=True, mean=mean, var=sd ** 2))
    imsave(new_image_path, img_noise)


def apply_grayscale(image_path, new_image_path):
    img = imread(image_path)
    img_grayscale = img_as_ubyte(rgb2gray(img))
    imsave(new_image_path, img_grayscale)


def apply_missing_pixels(image_path, new_image_path, proportion=0.05, replace="b"):
    img = imread(image_path)
    noise_mode = "salt" if replace == "w" else "pepper"  # Replace with white or black pixels
    img_noise = img_as_ubyte(random_noise(img, mode=noise_mode, clip=True, amount=proportion))
    imsave(new_image_path, img_noise)


def apply_sp_noise(image_path, new_image_path, proportion=0.05):
    img = imread(image_path)
    img_noise = img_as_ubyte(random_noise(img, mode="s&p", clip=True, amount=proportion))
    imsave(new_image_path, img_noise)


# noinspection PyTypeChecker
def apply_weather_image_corruptions(image_path, new_image_path, condition, severity=1):
    img = np.asarray(Image.open(image_path))
    fog_img = corrupt(img, corruption_name=condition, severity=severity)
    fog_img = Image.fromarray(fog_img)
    fog_img.save(new_image_path)


# Masks from:
# - Condensation: https://github.com/francescosecci/Python_Image_Failures
# - Frost: https://github.com/bethgelab/imagecorruptions
def apply_weather_mask(image_path, new_image_path, condition):
    mask_path = resource_filename(__name__, '../masks/' + condition + '.jpeg')
    img = Image.open(image_path)
    img_mask = Image.open(mask_path).convert('RGB').resize(img.size)
    img_blend = Image.blend(img, img_mask, alpha=0.4)
    img_blend.save(new_image_path)


def apply_weather(image_path, new_image_path, condition, is_mask=False, severity=1):
    if is_mask:
        apply_weather_mask(image_path, new_image_path, condition)
    else:
        cond = 'snow' if condition == 'rain_snow' else condition
        apply_weather_image_corruptions(image_path, new_image_path, cond, severity)
