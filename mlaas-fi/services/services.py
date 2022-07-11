from utils import is_rekognition_service
from .aws_rekognition import AWSRekognition


# Retrieves the predictions from a service for a given set of images
def get_predictions(expconfig, client, images):
    service = expconfig['service']
    client.run_service(service, images)


# Retrieves the client to invoke a machine learning cloud service
def get_client(expconfig, services_config):
    provider = expconfig['provider']
    service = expconfig['service']

    if provider == "AWS" and is_rekognition_service(service) and services_config['providers']['AWS']:
        return AWSRekognition(services_config['providers']['AWS'])
    else:
        print('Invalid combination of provider ({}) and service ({})'.format(provider, service))
        return None
