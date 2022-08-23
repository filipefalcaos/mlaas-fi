import glob
import os
import random
import sys
import time
import warnings

from constants import DEFAULT_DATASET_DIR, DEFAULT_TEMP_DIR
from faults import inject_fault
from mitigations import apply_mitigation
from services import get_client, get_predictions
from utils import create_dir, dump_json, extract_tarfile, has_key, recreate_dir


# Experiment steps
INJECT_FAULTS = '  Injecting {} on {} images'
APPLY_MITIGATIONS = '  Applying mitigations to faulty images{}'
GET_PREDICTIONS = '  Performing predictions{}'
SAVE_RESULTS = '  Saving experiment output'


# Prints a step (i.e., a message followed by a check mark)
def print_step(message, parameters=[], complete=False, multistep=False, extra_end=''):
    if multistep or complete:
        sys.stdout.write('\033[F')

    # Prints '...' if incomplete or a mark otherwise
    mark = u'\u2714'
    mark_color = '\033[92m'
    end = ' ...' if not complete else ' ' + mark_color + mark + '\033[0m'
    end = end + (' ' * 20) + '\n' + extra_end

    print((message).format(*parameters), end=end)


def gen_faulty_image_path(image_path, fault, fault_param=None, fault_param_value=None):
    basename = os.path.basename(image_path)
    image_name, extension = os.path.splitext(basename)
    base_path = DEFAULT_TEMP_DIR + image_name + '-' + fault

    if fault_param is None or fault_param_value is None:
        return base_path + extension
    else:
        return base_path + '-' + fault_param + '_' + str(fault_param_value) + extension


# Retrieves the data for an experiment and returns a sample of it according to the experiment's
# configuration
def get_experiment_data(dataset_base_dir, exp_config):
    dataset = dataset_base_dir + exp_config['dataset']

    # Extract the dataset content - works recursively
    extract_tarfile(dataset + '.tar.gz', dataset_base_dir)
    dataset_images = glob.glob(dataset + '/**/*.jpg', recursive=True)
    dataset_images += glob.glob(dataset + '/**/*.JPG', recursive=True)

    return dataset_images


# Saves the results of an experiment to a given results directory
def save_results(exp_config, experiment_name, predictions):
    output_dir = exp_config['output_dir'] + '/'
    create_dir(output_dir)

    output_obj = {'experiment': experiment_name, 'config': exp_config, 'predictions': predictions}
    output_path = output_dir + experiment_name + '-' + str(int(time.time())) + '.json'
    dump_json(output_path, output_obj)


# Injects the experiment faults into the experiment data, saving the faulty to the
# DEFAULT_TEMP_DIR directory
def inject_faults(exp_data, exp_data_faults):
    dataset_len = len(exp_data)
    faults_len = len(exp_data_faults)

    for idx, fault in enumerate(exp_data_faults):
        fault_name = fault['name']
        step_str = fault_name + ' (' + str(idx + 1) + '/' + str(faults_len) + ')'
        print_step(INJECT_FAULTS, [step_str, dataset_len], multistep=True)

        try:
            for image_path in exp_data:
                if not has_key(fault, 'parameter'):
                    new_path = gen_faulty_image_path(image_path, fault_name)
                    inject_fault(image_path, new_path, fault_name)  # Inject the fault
                else:
                    fault_param = fault['parameter']
                    for param_value in fault_param['values']:
                        # Inject the fault w/ parameter
                        new_path = gen_faulty_image_path(
                            image_path, fault_name, fault_param['name'], param_value
                        )
                        inject_fault(image_path, new_path, fault_name, param_value)
        except BaseException:
            print('Failed to inject fault {} on {}'.format(fault_name, image_path))
            raise

    print_step(INJECT_FAULTS, ['data faults', dataset_len], complete=True, extra_end='\n')


# Applies a random mitigation for each faulty image
def apply_mitigations(mitigations):
    if (not len(mitigations)):
        return

    faulty_images = glob.glob(DEFAULT_TEMP_DIR + '*', recursive=True)
    faulty_images_len = len(faulty_images)
    secure_random = random.SystemRandom()

    # Apply random mitigations to faulty images
    for idx, faulty_image in enumerate(faulty_images):
        step_str = ' (' + str(idx) + '/' + str(faulty_images_len) + ')'
        print_step(APPLY_MITIGATIONS, [step_str], multistep=True)
        random_mitigation = secure_random.choice(mitigations)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=RuntimeWarning)
            apply_mitigation(faulty_image, random_mitigation)

    print_step(APPLY_MITIGATIONS, [''], complete=True)


# Performs the predictions (base + faulty) for all the data points in the experiment data
def perform_predictions(curr_experiment, exp_data, service_client):
    predictions = []
    dataset_len = len(exp_data)

    print_step(GET_PREDICTIONS, [' '])
    for idx, image_path in enumerate(exp_data):
        image_pred_object = {
            'key': os.path.basename(image_path),
            'base': [],
            'faults': {}
        }

        step_str = ' (' + str((idx + 1)) + '/' + str(dataset_len) + ')'
        print_step(GET_PREDICTIONS, [step_str], multistep=True)

        try:
            # Get the base predictions
            preds = get_predictions(curr_experiment, service_client, image_path)
            image_pred_object['base'] = preds

            # Get the faulty predictions
            for idx, fault in enumerate(curr_experiment['data_faults']):
                fault_name = fault['name']

                if not has_key(fault, 'parameter'):
                    faulty_image_path = gen_faulty_image_path(image_path, fault_name)
                    preds = get_predictions(curr_experiment, service_client, faulty_image_path)
                    image_pred_object['faults'][fault_name] = preds
                else:
                    fault_param = fault['parameter']
                    for param_value in fault_param['values']:
                        faulty_image_path = gen_faulty_image_path(
                            image_path, fault_name, fault_param['name'], param_value
                        )
                        preds = get_predictions(curr_experiment, service_client, faulty_image_path)
                        fault_key = fault_name + '-' + fault_param['name'] + '_' + str(param_value)
                        image_pred_object['faults'][fault_key] = preds
        except BaseException:
            print('Failed to get predictions for image {}'.format(image_path))
            raise

        predictions.append(image_pred_object)

    print_step(GET_PREDICTIONS, [''], complete=True)
    return predictions  # Predictions (base + faulty)


# Launches the configured fault injection experiments. Experiments are launched in the order they
# are defined in the experiments configuration file
def launch_experiments(exp_config, providers_config):
    experiments = exp_config['experiments']
    for experiment_name in experiments:
        curr_experiment = experiments[experiment_name]
        print('\n- Experiment: "{}"\n'.format(experiment_name))

        # Setup the configured provider/service
        service_client = get_client(curr_experiment, providers_config)
        if service_client is None:
            return

        # Get the configured dataset and set the temp dir
        exp_data = get_experiment_data(DEFAULT_DATASET_DIR, curr_experiment)
        recreate_dir(DEFAULT_TEMP_DIR)

        # Inject data faults into the dataset
        inject_faults(exp_data, curr_experiment['data_faults'])

        if has_key(curr_experiment, 'mitigations'):
            apply_mitigations(curr_experiment['mitigations'])

        # Get the base and faulty predictions from service
        predictions = perform_predictions(curr_experiment, exp_data, service_client)

        # Save the experiment results
        print_step(SAVE_RESULTS)
        save_results(curr_experiment, experiment_name, predictions)
        print_step(SAVE_RESULTS, complete=True)

    print('\nAll experiments finished')
