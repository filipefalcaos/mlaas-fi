from .image import *


# Injects a specific data fault in an image with the given parameters
def inject_fault(image_path, new_image_path, params, fault):
    if fault == 'blur':
        apply_blur(image_path, new_image_path, params['sd'])
    elif fault == 'brightness':
        apply_brightness(image_path, new_image_path, params['factor'])
    elif fault == 'chromatic_aberration':
        apply_chromatic_aberration(image_path, new_image_path, params['strength'])
    elif fault == 'gaussian_noise':
        apply_gaussian_noise(image_path, new_image_path, params['mean'], params['sd'])
    elif fault == 'grayscale':
        apply_grayscale(image_path, new_image_path)
    elif fault == 'missing_pixels':
        apply_missing_pixels(image_path, new_image_path, params['proportion'], params['replace'])
    elif fault == 'sp_noise':
        apply_sp_noise(image_path, new_image_path, params['proportion'])

    elif fault == 'condensation':
        apply_weather(image_path, new_image_path, 'condensation', is_mask=True)
    elif fault == 'fog':
        apply_weather(image_path, new_image_path, 'fog', severity=params['severity'])
    elif fault == 'frost':
        apply_weather(image_path, new_image_path, 'frost', is_mask=True)
    elif fault == 'rain_snow':
        apply_weather(image_path, new_image_path, 'rain_snow', severity=params['severity'])

    else:
        return
