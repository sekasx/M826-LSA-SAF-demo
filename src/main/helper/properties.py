import argparse

import yaml


def load_properties():
    # Define command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", nargs='?', default='local', type=str, required=False,
                        help="The environment to use")
    args = parser.parse_args()
    # Load the appropriate YAML file based on the environment
    env = args.env
    properties = None
    with open(f"../resources/properties-{env}.yml", "r") as file:
        properties = yaml.safe_load(file)
    return properties
