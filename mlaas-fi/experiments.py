import glob
import os
import random
import time

from constants import BASE_TEMP_DIR
from faults import inject_fault
from metrics import misclassification_rate, confidence_change
from services import get_client, get_predictions
from utils import create_dir, dump_json, extract_tarfile, recreate_dir


random.seed(10)  # Default seed


# Saves the results of an experiment to a given results directory
def save_results(expconfig, experiment_name, mrates):
    output_dir = expconfig['output_dir'] + '/'
    create_dir(output_dir)

    output_obj = {'experiment': experiment_name, 'config': expconfig, 'mrate': mrates}
    output_path = output_dir + experiment_name + '-' + str(int(time.time())) + '.json'
    dump_json(output_path, output_obj)


# Retrieves the data for an experiment and returns a sample of it according to the experiment's
# configuration
def get_experiment_data(dataset_base_dir, expconfig):
    dataset = dataset_base_dir + expconfig['dataset']
    dataset_file = dataset + '.tar.gz'

    # Extract the dataset content
    extract_tarfile(dataset_file, dataset_base_dir)

    # Set the random dataset sample - works recursively
    dataset_images = glob.glob(dataset + '/**/*.jpg', recursive=True)
    dataset_images = random.sample(dataset_images, expconfig['n_samples'])
    return dataset_images


# Launches the configured fault injection experiments. Experiments are launched in the order they
# are defined in the experiments configuration file
def launch_experiments(exp_config, services_config):
    experiments = exp_config['experiments']
    for experiment_name in experiments:
        curr_experiment = experiments[experiment_name]
        print('\nStarting experiment "{}"'.format(experiment_name))

        # Get the configured dataset and set the temporary images dir
        exp_images = {'base': {}}
        dataset_base_dir = 'datasets/'
        exp_images['base']['images'] = get_experiment_data(dataset_base_dir, curr_experiment)
        recreate_dir(BASE_TEMP_DIR)

        # Inject data faults into the dataset
        print('Injecting data faults on {} images...'.format(curr_experiment['n_samples']))
        for fault in curr_experiment['data_faults']:
            exp_images[fault] = {'images': []}
            for image_path in exp_images['base']['images']:
                fault_params = curr_experiment['data_faults'][fault]

                # Get the temporary noisy image path
                basename = os.path.basename(image_path)
                image_name, extension = os.path.splitext(basename)
                new_path = BASE_TEMP_DIR + image_name + "-" + fault + extension

                # Inject the fault
                inject_fault(image_path, new_path, fault_params, fault)
                exp_images[fault]['images'].append(new_path)

        # Setup the configured service and perform the predictions
        client = get_client(curr_experiment, services_config)
        for key in exp_images:
            print("Performing predictions ({})...".format(key))
            preds = get_predictions(curr_experiment, client, exp_images[key]['images'])
            exp_images[key]['preds'] = preds

        # Compute the metrics for each fault
        mrates = {}
        base_preds = exp_images['base']['preds']

        for key in exp_images:
            if key != "base":
                curr_preds = exp_images[key]['preds']
                mrate = misclassification_rate(base_preds, curr_preds, curr_experiment['metrics']['k_mrate'])
                mrates[key] = mrate

        # Save the experiment results
        save_results(curr_experiment, experiment_name, mrates)

    print('\nAll experiments finished')
    print('Results saved in the "results" directory')
