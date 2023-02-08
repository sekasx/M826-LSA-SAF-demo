from src.main.helper.properties import load_properties
from src.main.process_LSA_SAF_DLST_collection import execute


def main():
    properties = load_properties()

    execute(properties)
    # lsa_example()


if __name__ == "__main__":
    main()
