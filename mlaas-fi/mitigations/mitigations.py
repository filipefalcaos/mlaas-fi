from .image import *


def apply_mitigation(image_path, mitigation):
    if mitigation == 'bit_depth_reduction':
        bit_depth_reduction(image_path)
    elif mitigation == 'gaussian_filter':
        gaussian_filter(image_path)
    elif mitigation == 'jpeg_compression':
        JPEG_compression(image_path)
    elif mitigation == 'median_filter':
        median_filter(image_path)
    elif mitigation == 'wavelet_denoising':
        wavelet_denoising(image_path)
    else:
        return
