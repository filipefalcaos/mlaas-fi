from google.cloud import vision


class GoogleVision:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()


    # Labels objects detected in an image
    # Leveraged API: label_detection from google.cloud.vision
    def __detect_labels(self, img):
        image = vision.Image(content=img)
        response = self.client.label_detection(image=image)
        response_labels = response.label_annotations
        label_names = [response_label['description'] for response_label in labels]
        return label_names
    

    # Detects text occurrences (only TEXT_DETECTION type) in an image
    # Leveraged API: text_detection from google.cloud.vision
    def __detect_text(self, img):
        image = vision.Image(content=img)
        response = self.client.text_detection(image=image)
        response_texts = response.text_annotations
        print(response_texts) # TODO: extract detected text
    

    # Detects unsafe content (violence and adult) in an image
    # Leveraged API: safe_search_detection from google.cloud.vision
    def __detect_unsafe_labels(self, img):
        image = vision.Image(content=img)
        response = self.client.safe_search_detection(image=image)
        response_labels = response.safe_search_annotation
        print(response_labels) # TODO: extract detected labels


    def run_service(self, service, images):
        # Map a service to a function
        service_fn = None
        if service == "LABEL_DETECTION":
            service_fn = self.__detect_labels
        elif service == "NUDITY_DETECTION" or service == "VIOLENCE_DETECTION":
            service_fn = self.__detect_unsafe_labels
        elif service == "TEXT_DETECTION":
            service_fn = self.__detect_text

        # Apply the function to the given images
        output_list = []
        for image in images:
            with open(image, 'rb') as img_file:
                img = img_file.read()
            try:
                output = service_fn(img)
                output_list.append(output)
            except ClientError:
                print('Unable to run {} for input image {}'.format(service, image))
        
        return output_list
