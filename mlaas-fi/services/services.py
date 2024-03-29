from .aws_rekognition import AWSRekognition
from .google_vision import GoogleVision
from .msft_vision import MSFTVision
from .utils import is_azure_vision_service, is_google_vision_service, is_rekognition_service


# Retrieves the predictions from a service for a given image
def get_predictions(exp_config, client, image):
    service = exp_config['service']
    predictions = client.run_service(service, image)
    return predictions


# Retrieves the client to invoke a machine learning cloud service
def get_client(exp_config, providers_config):
    provider = exp_config['provider']
    service = exp_config['service']

    if provider == 'AWS' and is_rekognition_service(service):
        return AWSRekognition(providers_config['providers']['AWS'])
    elif provider == 'GOOGLE_CLOUD' and is_google_vision_service(service):
        return GoogleVision()
    elif provider == 'MSFT_AZURE' and is_azure_vision_service(service):
        return MSFTVision(providers_config['providers']['MSFT_AZURE'])
    else:
        print('Unsupported combination of provider ({}) and service ({})'.format(provider, service))
        return None
