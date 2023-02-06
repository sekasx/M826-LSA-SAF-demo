from src.main.processSnapImage import execute
import argparse
import yaml
from os import listdir
from os.path import isfile, join

from src.main.process_lsa_image_example import lsa_example


def main():


    # Define command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", nargs='?', default='local', type=str, required=False, choices=["dev", "prod"], help="The environment to use")
    args = parser.parse_args()

    # Load the appropriate YAML file based on the environment
    env = args.env
    with open(f"../resources/properties-{env}.yml", "r") as file:
        properties = yaml.safe_load(file)
    execute()
    # lsa_example()

if __name__ == "__main__":

    main()


