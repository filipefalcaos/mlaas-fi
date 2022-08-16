import time
import requests


# Common vision services across all supported providers
COMMON_VISION_SERVICES = [
    'LABEL_DETECTION', 'NUDITY_DETECTION', 'TEXT_DETECTION'
]

# Default retry config
RETRY_TIMES = 100


# Checks if a service is a supported AWS Rekognition service
def is_rekognition_service(service):
    rekognition_only = ['CELEBRITY_RECOGNITION', 'VIOLENCE_DETECTION']
    return service in [*COMMON_VISION_SERVICES, *rekognition_only]


# Checks if a service is a supported Google Vision service
def is_google_vision_service(service):
    google_vision_only = ['VIOLENCE_DETECTION']
    return service in [*COMMON_VISION_SERVICES, *google_vision_only]


# Checks if a service is a supported Azure Vision service
def is_azure_vision_service(service):
    azure_vision_only = ['CELEBRITY_RECOGNITION']
    return service in [*COMMON_VISION_SERVICES, *azure_vision_only]


def core_api_request(api_url, headers, data):
    response = requests.post(api_url, headers=headers, data=data)
    response.raise_for_status()
    return response


# Makes an API request, using requests, to a given url with the given headers and payload data
def make_api_request(api_url, headers, data):
    try:
        return core_api_request(api_url, headers, data)
    except BaseException as e:
        print('Got %s error %s, retrying' % (type(e).__name__, e))
        time.sleep(10)
        return core_api_request(api_url, headers, data)
