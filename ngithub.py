import os
from github import Github
from github import GithubException
from datetime import datetime


def fetch_branches(repo_name, token):
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    _branches = {}
    for row in repo.get_branches():
        _branches[row.name] = row.commit.sha
    
    return _branches


#def get_commit_datetime(sha, repo_name, token):
def commit_older_than_datetime(sha, datetime_now, shift, repo_name, token):
    g = Github(token)
    repo = g.get_repo(repo_name)
    commit = repo.get_commit(sha=sha)
    _commit_date = commit.commit.committer.date
    _diff = int((datetime_now - _commit_date).total_seconds())
    _mark = "<="
    if _diff > shift:
        _mark = ">"
    print("{} - {} = {} {} {}".format(datetime_now, _commit_date, _diff, _mark, shift))
    if _diff > shift:
        return True
    else:
        return False


def branch_exists(branch_name, repo_name, token):
    g = Github(token)
    repo = g.get_repo(repo_name)
    try:
        _response = repo.get_branch(branch=branch_name)
        if _response.name == branch_name:
            return True
        
        # here should not be reached except something goes wrong in PyGithub or github API
        return False
    except GithubException as err:
        if err.status == 404:
            print("branch {} not found".format(branch_name))
        else:
            print("other execption: {}".format(err))
        return False


##### ##### ##### #####
# for testing

def test():
    _datetime_now = datetime.utcnow()
    _repo_name = "naihsi/s-exercise1"
    _token = os.environ["TOKEN"]
    
    _branch_name = "dev_2"
    _existance = branch_exists(_branch_name, _repo_name, _token)
    print("{}: {}".format(_branch_name, _existance))
    return 0
    
    _branches = fetch_branches(_repo_name, _token)
    print(_branches)
    
    for k,v in _branches.items():
        if commit_older_than_datetime(v, _datetime_now, 100, _repo_name, _token):
            print("{} is too old".format(k))


if __name__ == "__main__":
    test()
