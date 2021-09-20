import logging
import sys
from datetime import datetime

import nboto3
import ngithub


def fetch_branches(repo_name, token):
    return ngithub.fetch_branches(repo_name, token)

def commit_older_than_datetime(sha, datetime_now, shift, repo_name, token):
    return ngithub.commit_older_than_datetime(sha, datetime_now, shift, repo_name, token)


def fetch_instances():
    return nboto3.fetch_instances()


def terminate_instances(instance_ids):
    nboto3.terminate_instances(instance_ids)


def main():
    # generate datetime
    _datetime_now = datetime.utcnow()
    _shift = 100
    
    # fetch the branches
    _repo_name = "naihsi/s-exercise1"
    _token = "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"
    _branches = fetch_branches(_repo_name, _token)
    logger.debug(_branches)

    # check if each instance hits the threshold to recycle
    _to_recycle = []
    for row in fetch_instances():
        _branch_name = row["branch_name"]
        _sha = _branches[_branch_name]
        
        if commit_older_than_datetime(_sha, _datetime_now, _shift, _repo_name, _token ):
          # add to recycle list if the commit is too old
          _to_recycle.append(row["instance_id"])
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
