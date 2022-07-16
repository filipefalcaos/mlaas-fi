from constants import EXP_CONFIG_FILE, SERVICES_CONFIG_FILE
from experiments import launch_experiments
from utils import parse_json


if __name__ == '__main__':
    print('Fault Injector for MLaaS v0.1')

    # Parse the services config
    services_config = parse_json(SERVICES_CONFIG_FILE)
    print('Found {} configured services in {}'.format(len(services_config), SERVICES_CONFIG_FILE))

    # Parse the experiments config
    exp_config = parse_json(EXP_CONFIG_FILE)
    print('Found {} experiments in {}'.format(len(exp_config), EXP_CONFIG_FILE))

    # Launch experiments
    try:
        launch_experiments(exp_config, services_config)
    except BaseException as err:
        print('\nUnexpected Error: {}, {}\n'.format(err, type(err)))
        raise
