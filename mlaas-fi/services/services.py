from utils import is_rekognition_service
from .aws_rekognition import AWSRekognition


# Retrieves the predictions from a service for a given set of images
def get_predictions(expconfig, client, images):
    service_type = expconfig['service_type']
    return client.run_service(service_type, images)


# Retrieves the client to invoke a machine learning cloud service
def get_client(expconfig, services_config):
    provider = expconfig['provider']
    service_type = expconfig['service_type']

    if provider == "AWS" and is_rekognition_service(service_type) and services_config['providers']['AWS']:
        return AWSRekognition(services_config['providers']['AWS'])
