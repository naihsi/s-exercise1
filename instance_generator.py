import logging
import sys
import os
import nboto3
import ngithub


def create_instance(branch_name):
    nboto3.create_instance(branch_name)


def branch_exists(branch_name, repo_name, token):
    return ngithub.branch_exists(branch_name, repo_name, token)


def launch_instance():
    _token = os.environ["TOKEN"]
    _repo_name = "naihsi/s-exercise1"
    _branch_name = "dev_2"
    
    if not branch_exists(_branch_name, _repo_name, _token):
        logger.error("branch {} not found, stop the launch of instance".format(_branch_name))
        return 1
    
    create_instance(_branch_name)


if __name__ == "__main__":
    try:
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.StreamHandler())
        if "--debug" in sys.argv:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        launch_instance()
    except Exception as err:
        logging.fatal("undefined exception:", err)
