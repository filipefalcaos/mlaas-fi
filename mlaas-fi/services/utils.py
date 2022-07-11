# Common vision services across all supported providers
COMMON_VISION_SERVICES = [
    'LABEL_DETECTION', 'NUDITY_DETECTION', 'TEXT_DETECTION', 'VIOLENCE_DETECTION'
]

# Checks if a service is a supported AWS Rekognition service
def is_rekognition_service(service):
    rekognition_only = ['CELEBRITY_RECOGNITION']
    return service in [*COMMON_VISION_SERVICES, *rekognition_only]


# Checks if a service is a supported Google Vision service 
def is_google_vision_service(service):
    google_vision_only = []
    return service in [*COMMON_VISION_SERVICES, *google_vision_only]
