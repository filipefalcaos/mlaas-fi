import time
import requests

from .utils import make_api_request


# Default Content-Type header
CONTENT_TYPE_HEADER = 'application/octet-stream'


class MSFTVision:
    def __init__(self, msft_config):
        self.api_endpoint_vision = msft_config['endpoint_vision']
        self.api_endpoint_face = msft_config['endpoint_face']
        self.api_headers_vision = {
            'Ocp-Apim-Subscription-Key': msft_config['subscription_key_vision'],
            'Content-Type': CONTENT_TYPE_HEADER
        }
        self.api_headers_face = {
            'Ocp-Apim-Subscription-Key': msft_config['subscription_key_face'],
            'Content-Type': CONTENT_TYPE_HEADER
        }

    def __detect_faces(self, img):
        api_url = self.api_endpoint_face + '/face/v1.0/detect'
        response_data = make_api_request(api_url, self.api_headers_face, img)
        response_data = response_data.json()
        response_faces_n = len(response_data)
        return ['detected'] if response_faces_n else ['not-detected']

    # Labels objects detected in an image
    # Leveraged API: Analyze Image from Cognitive Services (visualFeatures=Tags)
    def __detect_labels(self, img):
        api_url = self.api_endpoint_vision + '/vision/v3.2/analyze?visualFeatures=Tags'
        response_data = make_api_request(api_url, self.api_headers_vision, img)
        response_data = response_data.json()
        response_labels = response_data['tags']
        label_names = [response_label['name'] for response_label in response_labels]
        return label_names

    def __detect_text(self, img):
        api_url = self.api_endpoint_vision + '/vision/v3.2/read/analyze'
        response_data = make_api_request(api_url, self.api_headers_vision, img)
        operation_url = response_data.headers['Operation-Location']  # URL to retrieve detected text

        analysis = {}
        poll = True
        while (poll):
            response_final = requests.get(operation_url, headers=self.api_headers_vision)
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
        api_url = self.api_endpoint_vision + '/vision/v3.2/analyze?visualFeatures=Adult'
        response_data = make_api_request(api_url, self.api_headers_vision, img)
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
            'FACE_DETECTION': self.__detect_faces,
            'LABEL_DETECTION': self.__detect_labels,
            'NUDITY_DETECTION': self.__detect_adult_content,
            'TEXT_DETECTION': self.__detect_text
        }

        # Apply the function to the given image
        with open(image, 'rb') as img_file:
            img_payload = img_file.read()
        output = service_map[service](img_payload)
        return output
