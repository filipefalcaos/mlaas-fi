from .image import *


# Injects a specific data fault in an image with the given parameters
def inject_fault(image_path, new_image_path, fault):
    # Blur
    if fault == 'blur':
        gaussian_blur(image_path, new_image_path)
    elif fault == 'motion_blur':
        motion_blur(image_path, new_image_path)
    elif fault == 'zoom_blur':
        zoom_blur(image_path, new_image_path)

    # Noise
    elif fault == 'gaussian_noise':
        gaussian_noise(image_path, new_image_path)
    elif fault == 'sp_noise':
        sp_noise(image_path, new_image_path)

    # Weather-related image faults
    elif fault == 'condensation':
        condensation(image_path, new_image_path)
    elif fault == 'fog':
        fog(image_path, new_image_path)
    elif fault == 'frost':
        frost(image_path, new_image_path)
    elif fault == 'rain_snow':
        rain_snow(image_path, new_image_path)

    # Others
    elif fault == 'brightness':
        brightness(image_path, new_image_path)
    elif fault == 'chromatic_aberration':
        chromatic_aberration(image_path, new_image_path)
    elif fault == 'contrast':
        contrast(image_path, new_image_path)
    elif fault == 'defective_pixels':
        defective_pixels(image_path, new_image_path)
    elif fault == 'grayscale':
        grayscale(image_path, new_image_path)
    elif fault == 'pixelation':
        pixelation(image_path, new_image_path)

    else:
        return
