from PIL import Image
from skimage.filters import _gaussian, _median
from skimage.io import imsave, imread
from skimage.restoration import denoise_wavelet
from skimage.util import img_as_ubyte


def bit_depth_reduction(image_path):
    img = Image.open(image_path)
    new_img = img.convert('P', palette=Image.ADAPTIVE, colors=200)
    new_img = new_img.convert('RGB')
    new_img.save(image_path)


def gaussian_filter(image_path):
    img = imread(image_path)
    new_img = img_as_ubyte(_gaussian.gaussian(img, channel_axis=-1))
    imsave(image_path, new_img, check_contrast=False)


def JPEG_compression(image_path):
    img = Image.open(image_path)
    img.save(image_path, 'JPEG', quality=75)


def median_filter(image_path):
    img = imread(image_path)
    new_img = img_as_ubyte(_median.median(img))
    imsave(image_path, new_img, check_contrast=False)


def wavelet_denoising(image_path):
    img = imread(image_path)
    denoised_img = img_as_ubyte(
        denoise_wavelet(
            img, channel_axis=-1, method='BayesShrink', mode='soft', rescale_sigma=True
        )
    )
    imsave(image_path, denoised_img, check_contrast=False)
