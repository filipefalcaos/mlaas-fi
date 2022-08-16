import time
import requests

from .utils import make_api_request


class MSFTVision:
    def __init__(self, msft_config):
        self.api_endpoint = msft_config['endpoint']
        self.api_headers = {
            'Ocp-Apim-Subscription-Key': msft_config['subscription_key'],
            'Content-Type': 'application/octet-stream'
        }

    # Labels objects detected in an image
    # Leveraged API: Analyze Image from Cognitive Services (visualFeatures=Tags)
    def __detect_labels(self, img):
        api_url = self.api_endpoint + '/vision/v3.2/analyze?visualFeatures=Tags'
        response_data = make_api_request(api_url, self.api_headers, img)
        response_data = response_data.json()
        response_labels = response_data['tags']
        label_names = [response_label['name'] for response_label in response_labels]
        return label_names

    def __detect_text(self, img):
        api_url = self.api_endpoint + '/vision/v3.2/read/analyze'
        response_data = make_api_request(api_url, self.api_headers, img)
        operation_url = response_data.headers['Operation-Location']  # URL to retrieve detected text

        analysis = {}
        poll = True
        while (poll):
            response_final = requests.get(operation_url, headers=self.api_headers)
            analysis = response_final.json()
            time.sleep(1)
            if ('analyzeResult' in analysis):
                poll = False
            if ('status' in analysis and analysis['status'] == 'failed'):
                poll = False

        if ('analyzeResult' in analysis):
            texts_content = [line['text']
                             for line in analysis['analyzeResult']['readResults'][0]['lines']]
            return texts_content

        return []

    # Detects adult and racy content in an image
    # Leveraged API: Analyze Image from Cognitive Services (visualFeatures=Adult)
    def __detect_adult_content(self, img):
        api_url = self.api_endpoint + '/vision/v3.2/analyze?visualFeatures=Adult'
        response_data = make_api_request(api_url, self.api_headers, img)
        response_data = response_data.json()
        response_labels = response_data['adult']

        # Conditionally add the adult or racy labels
        label_names = []
        if response_labels['isAdultContent']:
            label_names.append('adult')
        if response_labels['isRacyContent']:
            label_names.append('racy')
        return label_names

    def run_service(self, service, image):
        # Map a service to a prediction function
        service_map = {
            'LABEL_DETECTION': self.__detect_labels,
            'NUDITY_DETECTION': self.__detect_adult_content,
            'TEXT_DETECTION': self.__detect_text
        }

        # Apply the function to the given image
        with open(image, 'rb') as img_file:
            img_payload = img_file.read()
        output = service_map[service](img_payload)
        return output
