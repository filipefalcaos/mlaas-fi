from experiments import launch_experiments
from utils import parse_json


if __name__ == '__main__':
    print('Fault Injector for MLaaS v0.1')

    # Get the experiments config
    config_file = 'expconfig.json'
    expconfig = parse_json(config_file)
    print('Found {} experiments in configuration file'.format(len(expconfig)))

    # Launch experiments
    print('Lauching experiments...')
    launch_experiments(expconfig)
