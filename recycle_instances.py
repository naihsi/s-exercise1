import logging
import sys
import nboto3


def fetch_branches(datetime_now):
    return {}


def fetch_instances():
    return nboto3.fetch_instances()


def terminate_instances(instance_ids):
    nboto3.terminate_instances(instance_ids)


def main():
    # generate datetime
    _datetime_now = ""

    # fetch the branches
    _branches = fetch_branches(_datetime_now)
    logger.debug(_branches)

    # check if each instance hits the threshold to recycle
    _to_recycle = []
    for row in fetch_instances():
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
