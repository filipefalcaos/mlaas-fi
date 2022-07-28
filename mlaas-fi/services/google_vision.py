from google.cloud import vision


# Default labels for nudity and violence
NUDITY_LABELS = ['adult', 'racy']
VIOLENCE_LABELS = ['violence']


class GoogleVision:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    # Labels objects detected in an image
    # Leveraged API: label_detection from google.cloud.vision
    def __detect_labels(self, img):
        image = vision.Image(content=img)
        response = self.client.label_detection(image=image)
        response_labels = response.label_annotations
        label_names = [response_label.description for response_label in response_labels]
        return label_names

    def __detect_nudity(self, img):
        return self.__detect_unsafe_labels(img, unsafe_labels=NUDITY_LABELS)

    # Detects text occurrences (only of the TEXT_DETECTION type) in an image
    # Leveraged API: text_detection from google.cloud.vision
    def __detect_text(self, img):
        image = vision.Image(content=img)
        response = self.client.text_detection(image=image)
        response_texts = response.text_annotations
        texts_content = [resp_text.description for resp_text in response_texts]
        return texts_content

    # Detects unsafe content, defined by the unsafe_label parameter, in an image
    # Supported unsafe labels: adult, medical, spoofed, violence, racy
    # Leveraged API: safe_search_detection from google.cloud.vision
    def __detect_unsafe_labels(self, img, unsafe_labels=None):
        # Unsafe labels and likelihood names
        UNSAFE_LABELS = ['adult', 'medical', 'spoofed', 'violence', 'racy']
        LIKELIHOOD_NAMES = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY',
                            'VERY_LIKELY')

        image = vision.Image(content=img)
        response = self.client.safe_search_detection(image=image)
        response_labels = response.safe_search_annotation

        # Convert output to the "label-likelihood" format
        label_names = [
            # safe_search_annotation isn't subscriptable
            unsafe_label + '-' + LIKELIHOOD_NAMES[getattr(response_labels, unsafe_label)]
            for unsafe_label in UNSAFE_LABELS
            if unsafe_labels is not None and unsafe_label in unsafe_labels
        ]

        return label_names

    def __detect_violence(self, img):
        return self.__detect_unsafe_labels(img, unsafe_labels=VIOLENCE_LABELS)

    # Run an Google Cloud Vision AI service for a given image
    def run_service(self, service, image):
        # Map a service to a prediction function
        service_map = {
            'LABEL_DETECTION': self.__detect_labels,
            'NUDITY_DETECTION': self.__detect_nudity,
            'VIOLENCE_DETECTION': self.__detect_violence,
            'TEXT_DETECTION': self.__detect_text
        }

        # Apply the function to the given image
        with open(image, 'rb') as img_file:
            img_payload = img_file.read()
        output = service_map[service](img_payload)
        return output
