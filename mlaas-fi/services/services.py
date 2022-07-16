from .aws_rekognition import AWSRekognition
from .google_vision import GoogleVision
from .utils import is_google_vision_service, is_rekognition_service


# Retrieves the predictions from a service for a given set of images
def get_predictions(exp_config, client, images):
    service = exp_config['service']
    predictions = client.run_service(service, images)
    return predictions


# Retrieves the client to invoke a machine learning cloud service
def get_client(exp_config, services_config):
    provider = exp_config['provider']
    service = exp_config['service']

    if (provider == 'AWS' and is_rekognition_service(service) and
            services_config['providers']['AWS']):
        return AWSRekognition(services_config['providers']['AWS'])
    elif provider == 'GOOGLE_CLOUD' and is_google_vision_service(service):
        return GoogleVision()
    else:
        print('Invalid combination of provider ({}) and service ({})'.format(provider, service))
        return None
