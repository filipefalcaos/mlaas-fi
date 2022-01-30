# mlaas-fi
Data Fault Injection on MLaaS

## Data Faults
Data Faults are problems in the input data of a system that may arise from external data collection (e.g., sensors, 
cameras) or data manipulation routines. _mlaas-fi_ implements a collection of ten data faults for two kinds of data,
images and text.

#### Base Image Faults
- Brightness Change
- Chromatic Aberration
- Gaussian Blur
- Gaussian Noise
- Grayscale
- Missing Pixels
- Salt & Pepper Noise

#### Weather-related Image Faults
- Condensation
- Fog
- Frost
- Rain/Snow

#### Text
- Missing Block
- Missing Words
- OCR Error

## Datasets
- Celebrity Recognition: A sample of 500 aligned and cropped images from the CelebA dataset [1].
- Label Detection: A sample of 500 images from the 2017 validation set of the COCO object detection dataset [2].
- Nudity Detection: A sample of 500 images from the test set of the NudeNet dataset [3] (currently not available on 
  GitHub due to the nature of the images).
- Violence Detection: A sample of 198 images of child soldiers and police violence from the Human Rights UNderstanding 
  (HRUN) dataset [4]. All child soldiers images have the presence of weapons.
- Text Detection: A sample of 398 images captured in different environments from the KAIST Scene Text Database [5]. 
  Images with english text only were selected.

## References
[1] Liu, Ziwei, et al. "Deep learning face attributes in the wild." Proceedings of the IEEE international conference on 
computer vision. 2015.

[2] Lin, Tsung-Yi, et al. "Microsoft coco: Common objects in context." European conference on computer vision. Springer, 
Cham, 2014.

[3] “NudeNet Classifier Dataset v1 : Https://Github.com/bedapudi6788/ : Free Download, Borrow, and Streaming.” Internet 
Archive, archive.org/details/NudeNet_classifier_dataset_v1. Accessed 2 May 2021.

[4] Kalliatakis, Grigorios, et al. "Detection of human rights violations in images: Can convolutional neural networks 
help?." arXiv preprint arXiv:1703.04103 (2017).

[5] SeongHun Lee, Min Su Cho, Kyomin Jung, and Jin Hyung Kim, "Scene Text Extraction with Edge Constraint and Text 
Collinearity Link," 20th International Conference on Pattern Recognition (ICPR), August 2010, Istanbul, Turkey.
