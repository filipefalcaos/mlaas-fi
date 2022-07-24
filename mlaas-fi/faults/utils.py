import numpy as np

from imagecorruptions import corrupt
from PIL import Image
from pkg_resources import resource_filename


def apply_img_corruption(image_path, new_image_path, corruption, severity):
    img = np.asarray(Image.open(image_path))
    img_corrupt = corrupt(img, corruption_name=corruption, severity=severity)
    img_corrupt = Image.fromarray(img_corrupt)
    img_corrupt.save(new_image_path)


def apply_corruptions(image_path, new_image_path, corruption, severity=None):
    default_parameters = [1, 2, 3, 4, 5]  # Default severity parameters

    if severity is not None:
        apply_img_corruption(image_path, new_image_path, corruption, severity)
    else:
        for param in default_parameters:
            apply_img_corruption(image_path, new_image_path, corruption, param)


# Masks from:
# - Condensation: https://github.com/francescosecci/Python_Image_Failures
# - Frost: https://github.com/bethgelab/imagecorruptions
def apply_weather_mask(image_path, new_image_path, condition):
    mask_path = resource_filename(__name__, './masks/' + condition + '.jpeg')
    img = Image.open(image_path)
    img_mask = Image.open(mask_path).convert('RGB').resize(img.size)
    img_blend = Image.blend(img, img_mask, alpha=0.4)
    img_blend.save(new_image_path)
