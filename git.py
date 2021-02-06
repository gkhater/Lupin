from github import Github, InputGitAuthor
from pprint import pprint

import config
from utils import getJournalPath, getCurrentTime, getTimestamp
from dictionaries import git_messages

#file_path = utils.getJournalPath()

GitHubToken = config.GitHubToken
GitHubFullRepo = config.GitHubUser + "/" + config.GitHubRepo
GitHubBranch = config.GitHubBranch
BotName = config.BotName

g = Github(GitHubToken)
repo = g.get_repo(GitHubFullRepo)



def push(path, message, content, branch, update=False):
    author = InputGitAuthor(
        config.GitHubAuthor,
        config.GitHubEmail
    )
    #source = repo.get_Branch(Branch)
    #repo.create_git_ref(ref=f"refs/heads/{Branch}", sha=source.commit.sha)  # Create new Branch from master
    if update:  # If file already exists, update it
        #pass
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author)  # Add, commit and push Branch
    else:  # If file doesn't exist, create it
        #pass
        repo.create_file(path, message, content, branch=branch, author=author)  # Add, commit and push Branch

def updateJournal(entry):
    file = repo.get_contents(getJournalPath(), ref=GitHubBranch)  # Get file from Branch
    data = file.decoded_content.decode("utf-8")  # Get raw string data
    data += "\n" + config.defaultIndentLevel + " " + getCurrentTime() + " " + entry  # Modify/Create file

    push(getJournalPath(), git_messages['COMMIT_MESSAGE'].format(BotName, getTimestamp()) , data, GitHubBranch, update=True)