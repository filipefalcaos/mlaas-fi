from google.cloud import vision


# Uses the "label_detection" API from Google Vision API to detect the labels in a list of images
def detect_labels_vision(imgs_paths):
    labels = []
    client = vision.ImageAnnotatorClient()

    for img_path in imgs_paths:
        with open(img_path, 'rb') as img_file:
            img = {'Bytes': img_file.read()}

        image = vision.Image(content=img)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        label_names = [response_label['description'] for response_label in labels]
        labels.append(label_names)

    return labels
