
def fetch_branches(datetime_now):
    return {}

def fetch_instances():
    _inst_list = []
    for row in _inst_list:
        yield row

def terminate_instances(instance_ids):
    print("to terminate:", instance_ids)
    for row in instance_ids:
      print("terminated:", row)


def main():
    # generate datetime
    _datetime_now = ""
    
    # fetch the branches
    _branches = fetch_branches(_datetime_now)
    print(_branches)

    # check if each instance hits the threshold to recycle
    _to_recycle = []
    for row in fetch_instances():
        # add to recycle list if the commit is too old
        _to_recycle.add(row)
    print(_to_recycle)
    
    # terminate the candidates ids
    terminate_instances(_to_recycle)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print("undefined exception:", err)
