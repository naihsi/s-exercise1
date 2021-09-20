import logging
import sys


def fetch_branches(datetime_now):
    return {}


def fetch_instances():
    _inst_list = []
    for row in _inst_list:
        yield row


def terminate_instances(instance_ids):
    logging.debug("to terminate:")
    logging.debug(instance_ids)
    for row in instance_ids:
        logging.info("terminated:", row)


def main():
    # generate datetime
    _datetime_now = ""

    # fetch the branches
    _branches = fetch_branches(_datetime_now)
    logging.debug(_branches)

    # check if each instance hits the threshold to recycle
    _to_recycle = []
    for row in fetch_instances():
        # add to recycle list if the commit is too old
        _to_recycle.add(row)
    logging.debug(_to_recycle)

    # terminate the candidates ids
    terminate_instances(_to_recycle)


if __name__ == "__main__":
    try:
        if "--debug" in sys.argv:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        main()
    except Exception as err:
        logging.fatal("undefined exception:", err)
