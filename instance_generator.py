import logging
import sys
import os
import argparse
import nboto3
import ngithub


def create_instance(branch_name):
    nboto3.create_instance(branch_name)


def branch_exists(branch_name, repo_name, token):
    return ngithub.branch_exists(branch_name, repo_name, token)


def launch_instance(branch_name):
    # check for required env variables
    _to_check = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_DEFAULT_REGION', 'GITHUB_TOKEN', 'REPO_NAME']
    for row in _to_check:
        if row not in os.environ:
            logger.fatal("please set env variable {} to execute this script".format(row))
            return 1
    
    # read setting from env variables
    _token = os.environ["GITHUB_TOKEN"]
    _repo_name = os.environ["REPO_NAME"]
    _branch_name = branch_name
    
    # check if the input branch name exists
    if not branch_exists(_branch_name, _repo_name, _token):
        logger.error("branch {} not found, stop the launch of instance".format(_branch_name))
        return 1
    
    # create the instance
    create_instance(_branch_name)


if __name__ == "__main__":
    try:
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.StreamHandler())
        
        parser = argparse.ArgumentParser()
        parser.add_argument("-b", "--branch", help="set the branch name", required=True)
        parser.add_argument("-d", "--debug", help="go debug mode", action="store_true")
        
        args = parser.parse_args()
        if args.debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        launch_instance(args.branch)
    except Exception as err:
        logging.fatal("undefined exception:", err)
