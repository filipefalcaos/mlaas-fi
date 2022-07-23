from .image import *


# Injects a specific data fault in an image with the given parameters
def inject_fault(image_path, new_image_path, params, fault):
    # Blur
    if fault == 'blur':
        gaussian_blur(image_path, new_image_path, params['sd'])
    elif fault == 'motion_blur':
        motion_blur(image_path, new_image_path, severity=params['severity'])
    elif fault == 'zoom_blur':
        zoom_blur(image_path, new_image_path, severity=params['severity'])

    # Noise
    elif fault == 'gaussian_noise':
        gaussian_noise(image_path, new_image_path, params['sd'])
    elif fault == 'sp_noise':
        sp_noise(image_path, new_image_path, params['proportion'])

    # Weather-related image faults
    elif fault == 'condensation':
        weather_conditions(image_path, new_image_path, 'condensation')
    elif fault == 'fog':
        weather_conditions(image_path, new_image_path, 'fog', severity=params['severity'])
    elif fault == 'frost':
        weather_conditions(image_path, new_image_path, 'frost')
    elif fault == 'rain_snow':
        weather_conditions(image_path, new_image_path, 'rain_snow', severity=params['severity'])

    # Others
    elif fault == 'brightness':
        brightness_change(image_path, new_image_path, params['factor'])
    elif fault == 'chromatic_aberration':
        chromatic_aberration(image_path, new_image_path, params['factor'])
    elif fault == 'contrast':
        contrast(image_path, new_image_path, severity=params['severity'])
    elif fault == 'defective_pixels':
        defective_pixels(image_path, new_image_path, params['proportion'], params['replace'])
    elif fault == 'grayscale':
        grayscale(image_path, new_image_path)
    elif fault == 'pixelation':
        pixelation(image_path, new_image_path, severity=params['severity'])

    else:
        return
