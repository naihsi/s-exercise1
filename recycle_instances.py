import logging
import sys
import os
from datetime import datetime

import nboto3
import ngithub


def fetch_branches(repo_name, token):
    return ngithub.fetch_branches(repo_name, token)


def commit_older_than_datetime(sha, datetime_now, shift, repo_name, token):
    return ngithub.commit_older_than_datetime(sha, datetime_now, shift,
                                              repo_name, token)


def fetch_instances():
    return nboto3.fetch_instances()


def terminate_instances(instance_ids):
    nboto3.terminate_instances(instance_ids)


def main():
    # check for required env variables
    _to_check = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_DEFAULT_REGION', 'GITHUB_TOKEN', 'REPO_NAME', 'TERMINATION_THRESHOLD']
    for row in _to_check:
        if row not in os.environ:
            logger.fatal("please set env variable {} to execute this script".format(row))
            return 1
    
    # read setting from env variables
    _repo_name = os.environ["REPO_NAME"]
    _token = os.environ["GITHUB_TOKEN"]
    _shift = int(os.environ["TERMINATION_THRESHOLD"])

    # generate datetime
    _datetime_now = datetime.utcnow()

    # fetch the branches
    _branches = fetch_branches(_repo_name, _token)
    logger.debug(_branches)

    # check if each instance hits the threshold to recycle
    _to_recycle = []
    for row in fetch_instances():
        _branch_name = row["branch_name"]
        _sha = _branches[_branch_name]

        if commit_older_than_datetime(_sha, _datetime_now, _shift, _repo_name,
                                      _token):
            # add to recycle list if the commit is too old
            _to_recycle.append(row["instance_id"])
            logger.info("{}({}) queues to terminate".format(
              row["instance_id"], row["branch_name"]))
        else:
            logger.info("{}({}) remains".format(row["instance_id"],
                                                row["branch_name"]))
    logger.debug("to recycle: {}".format(_to_recycle))

    # terminate the candidates ids
    if len(_to_recycle) == 0:
        logger.info("no instances to recycle")
        return 0

    terminate_instances(_to_recycle)


if __name__ == "__main__":
    try:
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.StreamHandler())
        if "--debug" in sys.argv:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        main()
    except Exception as err:
        logging.fatal("undefined exception:", err)
