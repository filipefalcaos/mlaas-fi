import glob
import json
import os
import random
import shutil
import time

from faults.image import *
from metrics import *
from services.aws_rekognition import *
from utils import extract_tarfile


random.seed(10)  # Default seed


def save_results(expconfig, experiment_name, results_dir, preds, alt_preds, mrates):
    """
    Saves the results of an experiment to the disk

    :param expconfig: The experiment configuration
    :param experiment_name: The experiment name
    :param results_dir: The base directory for all results
    :param preds: The list of base predictions
    :param alt_preds: The list of alternative predictions
    :param mrates: The set of misclassification rates calculated for each fault
    """

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    output_obj = {'experiment': experiment_name, 'config': expconfig, 'preds': preds, 'alt_preds': alt_preds,
                  'mrate': mrates}
    output_path = results_dir + experiment_name + '-' + str(int(time.time())) + '.json'
    with open(output_path, 'w') as outfile:
        json.dump(output_obj, outfile, indent=2)


def get_predictions(client_interface, images):
    """
    Retrieves the predictions from a service for a given set of images

    :param client_interface: The client interface of the requested machine learning service
    :param images: The paths to the input images
    :return: The predictions from the service
    """

    provider = client_interface['provider']
    service_type = client_interface['service_type']
    client = client_interface['client']

    if provider == "AWS":
        if service_type == "CELEBRITY_RECOGNITION":
            return recognize_celebrities_rekognition(client, images)
        elif service_type == "LABEL_DETECTION":
            return detect_labels_rekognition(client, images)
        elif service_type == "NUDITY_DETECTION" or service_type == "VIOLENCE_DETECTION":
            return detect_unsafe_labels_rekognition(client, images)
        elif service_type == "TEXT_DETECTION":
            return detect_text_rekognition(client, images)


def get_client(provider, service_type):
    """
    Retrieves the client to invoke a machine learning service

    :param provider: The name of the service provider
    :param service_type: The name of the service
    :return: The client of the requested machine learning service
    """

    if provider == "AWS":
        rekognition_services = ["CELEBRITY_RECOGNITION", "LABEL_DETECTION", "NUDITY_DETECTION", "TEXT_DETECTION",
                                "VIOLENCE_DETECTION"]
        if service_type in rekognition_services:
            return create_rekognition_client()


def inject_fault(image_path, new_image_path, params, fault):
    """
    Injects a specific data fault in an image with the given parameters

    :param image_path: The path of the image to inject the fault on
    :param new_image_path: The path of the new image
    :param params: The parameters (dict) of the data fault
    :param fault: The name of the data fault
    """

    # Base image faults
    if fault == 'blur':
        apply_blur(image_path, new_image_path, params['sd'])
    elif fault == 'brightness':
        apply_brightness(image_path, new_image_path, params['factor'])
    elif fault == 'chromatic_aberration':
        apply_chromatic_aberration(image_path, new_image_path, params['strength'])
    elif fault == 'gaussian_noise':
        apply_gaussian_noise(image_path, new_image_path, params['mean'], params['sd'])
    elif fault == 'grayscale':
        apply_grayscale(image_path, new_image_path)
    elif fault == 'missing_pixels':
        apply_missing_pixels(image_path, new_image_path, params['proportion'], params['replace'])
    elif fault == 'sp_noise':
        apply_sp_noise(image_path, new_image_path, params['proportion'])

    # Weather faults
    elif fault == 'condensation':
        apply_weather(image_path, new_image_path, 'condensation', is_mask=True)
    elif fault == 'fog':
        apply_weather(image_path, new_image_path, 'fog', severity=params['severity'])
    elif fault == 'frost':
        apply_weather(image_path, new_image_path, 'frost', is_mask=True)
    elif fault == 'rain_snow':
        apply_weather(image_path, new_image_path, 'rain_snow', severity=params['severity'])

    # Unknown fault name - ignore
    else:
        return


def get_experiment_data(dataset_base_dir, expconfig):
    """
    Retrieves the data for an experiment and returns a sample of it according to the
    experiment's configuration

    :param dataset_base_dir: The base directory for all datasets
    :param expconfig: The current experiment configuration
    :return: The sample of the experiment's data
    """

    # Extract the dataset content
    dataset = dataset_base_dir + expconfig['dataset']
    dataset_file = dataset + '.tar.gz'
    extract_tarfile(dataset_file, dataset_base_dir)

    # Set the random dataset sample - works recursively
    dataset_images = glob.glob(dataset + '/**/*.jpg', recursive=True)
    dataset_images = random.sample(dataset_images, expconfig['n_samples'])
    return dataset_images


def launch_experiments(expconfig):
    """
    Launches the configured Fault Injection experiments. Experiments are launched
    in the order they are defined in the experiments configuration file

    :param expconfig: The object with the configuration of the experiments
    """

    for experiment_name in expconfig:
        curr_experiment = expconfig[experiment_name]
        print('\nRunning experiment "{}"...'.format(experiment_name))

        # Get the configured dataset
        exp_images = {'base': {}}
        dataset_base_dir = 'datasets/'
        exp_images['base']['images'] = get_experiment_data(dataset_base_dir, curr_experiment)

        # Set the temporary images dir
        temp_images_dir = 'temp/'
        if os.path.exists(temp_images_dir):
            shutil.rmtree(temp_images_dir)
        os.makedirs(temp_images_dir)

        # Inject data faults into the dataset
        print('Injecting data faults on {} images...'.format(curr_experiment['n_samples']))
        for fault in curr_experiment['data_faults']:
            exp_images[fault] = {'images': []}
            for image_path in exp_images['base']['images']:
                fault_params = curr_experiment['data_faults'][fault]

                # Get the temporary noisy image path
                basename = os.path.basename(image_path)
                image_name, extension = os.path.splitext(basename)
                new_path = temp_images_dir + image_name + "-" + fault + extension

                # Inject the fault
                inject_fault(image_path, new_path, fault_params, fault)
                exp_images[fault]['images'].append(new_path)

        # Setup the configured service and perform the predictions
        provider = curr_experiment['provider']
        service_type = curr_experiment['service_type']
        client = get_client(provider, service_type)
        client_int = {'provider': provider, 'service_type': service_type, 'client': client}

        for key in exp_images:
            print("Performing predictions ({})...".format(key))
            preds = get_predictions(client_int, exp_images[key]['images'])
            exp_images[key]['preds'] = preds

        # Compute the misclassification rate for each fault
        mrates, final_preds = {}, {}
        base_preds = exp_images['base']['preds']

        print('\nResults')
        for key in exp_images:
            if key != "base":
                curr_preds = exp_images[key]['preds']
                mrate = misclassification_rate(base_preds, curr_preds, curr_experiment['metrics']['misclassification'])
                final_preds[key] = curr_preds
                mrates[key] = mrate
                print('({}, {}) => MRate: {}%'.format(key, curr_experiment['data_faults'][key], mrate * 100))

        # Save the experiment results
        results_dir = 'results/'
        save_results(curr_experiment, experiment_name, results_dir, base_preds, final_preds, mrates)

    print('\nAll experiments finished')
    print('Results saved in the \'results\' directory')
