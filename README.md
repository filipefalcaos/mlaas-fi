# mlaas-fi
Data Fault Injection for MLaaS (Machine Learning as a Service).

## Data Faults
Data Faults are problems in the input data of a system that may arise from external data collection
(*e.g.*, sensors, cameras) or data manipulation routines [1]. _mlaas-fi_ implements a total of 14
data faults for two categories of data, images and text.

### Image Faults
The available image faults in _mlaas-fi_ and their parameters are listed bellow. Their
implementations rely on open-source Python packages, namely imagecorruptions, numpy, pillow, and
skimage.

For more details on the available image faults, please refer to [PAPER CITATION].

#### Common Image Faults
- Brightness Change (factor $f$)
- Chromatic Aberration (strength $s$)
- Gaussian Blur (standard deviation $sd$)
- Gaussian Noise (mean $m$; standard deviation $sd$)
- Grayscale
- Missing Pixels (proportion $p$)
- Salt & Pepper Noise (proportion $p$)

#### Weather-related Image Faults
- Condensation
- Fog (severity $s$)
- Frost
- Rain/Snow (severity $s$)

### Text Faults
- Missing Block (TODO)
- Missing Words (TODO)
- OCR Error (TODO)

## Using Datasets
_mlaas-fi_ requires a dataset to run experiments. Valid image datasets are simply tar files which
should expand to a single directory with the dataset images.

### Study Datasets
Five datasets were used in [PAPER CITATION] to evaluate the robustness of MLaaS services to data
faults:

- Celebrity Recognition: A random sample of 500 aligned and cropped images from the CelebA dataset [2].
- Label Detection: A random sample of 500 images from the 2017 validation set of the COCO object
  detection dataset [3].
- Nudity Detection: A random sample of 500 images from the test set of the NudeNet dataset [4].
- Violence Detection: random A sample of 198 images of child soldiers and police violence from the
  Human Rights UNderstanding (HRUN) dataset [5]. All child soldiers images have the presence of
  weapons.
- Text Detection: A random sample of 398 images captured in different environments from the KAIST
  Scene Text Database [6]. Only images with english text only were selected.

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
