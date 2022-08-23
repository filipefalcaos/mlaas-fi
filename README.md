# mlaas-fi
Data Fault Injection for MLaaS (Machine Learning as a Service).

This framework allows injecting data faults into the input data provided to Machine Learning cloud
services and then assessing the robustness of these services when exposed to those faults based on
a set of available metrics.

## Machine Learning Cloud Services
The framework implements interfaces for using machine learning APIs from three major cloud
providers. Currently, only computer vision services are implemented:

- Amazon Rekognition (AWS): label detection, text detection, violence detection, nudity detection,
  celebrity recongnition, face detection
- Vision AI (Google Cloud): label detection, text detection, violence detection, nudity detection,
  face detection
- Vision Service (Microsoft Azure): label detection, nudity detection, face detection

## Data Faults
Data Faults are problems in the input data of a system that may arise from external data collection
(*e.g.*, sensors, cameras) or data manipulation routines [1]. The framework implements a total of
11 data faults that can be injected into images.

The available image faults in the framework and their parameters are listed below. Their
implementations rely on open-source Python packages, namely
[imagecorruptions](https://github.com/bethgelab/imagecorruptions), [numpy](https://numpy.org),
[pillow](https://python-pillow.org), and [scikit-image](https://scikit-image.org).

#### Common Image Faults
- Brightness Change
- Chromatic Aberration
- Gaussian Blur
- Motion Blur
- Zoom Blur
- Gaussian Noise
- Grayscale
- Missing Pixels
- Salt & Pepper Noise
- Contrast
- Pixelation

#### Weather-related Image Faults
- Condensation
- Fog
- Frost
- Rain/Snow

## Using Datasets
_mlaas-fi_ requires a dataset to run experiments. Valid image datasets are are tarball files that
should expand to a single directory with the dataset images.

### Study Datasets
Five datasets were used in our study to evaluate the robustness of MLaaS services to data
faults:

- Celebrity Recognition: A random sample of 500 aligned and cropped images from the CelebA dataset [2].
- Label Detection: A random sample of 500 images from the 2017 validation set of the COCO object
  detection dataset [3].
- Nudity Detection: A random sample of 500 images from the test set of the NudeNet dataset [4].
- Violence Detection: random A sample of 198 images of child soldiers and police violence from the
  Human Rights UNderstanding (HRUN) dataset [5]. All child soldier images have the presence of
  weapons.
- Text Detection: A random sample of 398 images captured in different environments from the KAIST
  Scene Text Database [6]. Only images with English text only were selected.

## References
[1] Nurminen, Jukka K., et al. "Software framework for data fault injection to test machine
learning systems." 2019 IEEE International Symposium on Software Reliability Engineering Workshops
(ISSREW). IEEE, 2019.

[2] Liu, Ziwei, et al. "Deep learning face attributes in the wild." Proceedings of the IEEE
international conference on computer vision. 2015.

[3] Lin, Tsung-Yi, et al. "Microsoft coco: Common objects in context." European conference on
computer vision. Springer, Cham, 2014.

[4] “NudeNet Classifier Dataset v1 : Https://Github.com/bedapudi6788/ : Free Download, Borrow, and
Streaming.” Internet Archive, archive.org/details/NudeNet_classifier_dataset_v1. Accessed 2 May 2021.

[5] Kalliatakis, Grigorios, et al. "Detection of human rights violations in images: Can
convolutional neural networks help?." arXiv preprint arXiv:1703.04103 (2017).

[6] SeongHun Lee, Min Su Cho, Kyomin Jung, and Jin Hyung Kim, "Scene Text Extraction with Edge
Constraint and Text Collinearity Link," 20th International Conference on Pattern Recognition
(ICPR), August 2010, Istanbul, Turkey.
