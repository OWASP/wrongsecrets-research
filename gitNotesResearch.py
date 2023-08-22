import requests
import os
import subprocess
import duckdb
from ulid import ULID

## Setup
def create_db_and_tables(db_name):
    conn = duckdb.connect(db_name, read_only=False)
    conn.execute(
        f"""CREATE TABLE IF NOT EXISTS repos
            (
                        id              string NOT NULL,
                        name            varchar(255) NOT NULL,
                        license         string NOT NULL,
                        stars           int NOT NULL,
                        has_notes       bool NULL,
                        notes_count     int NULL,
                        repo_created_at TIMESTAMP NOT NULL,
                        repo_updated_at TIMESTAMP NOT NULL,
                        created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (id)
            )"""
    )
    conn.execute(
        f"""CREATE TABLE IF NOT EXISTS notes
            (
                        id              string NOT NULL,
                        repo_id         string NOT NULL,
                        content         string NOT NULL,
                        note_created_at TIMESTAMP,
                        note_ref      string NOT NULL,
                        author          string,
                        created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (id),
                        FOREIGN KEY (repo_id) REFERENCES repos (id)
            )"""
    )
    return conn

def getRepos():
    repos = []
    api_url = "https://api.github.com/search/repositories"
    params = {"q": "stars:>10000", "sort": "stars", "per_page": 5}
    for page in range(1, 2):
        params["page"] = page
        response = requests.get(api_url, params=params)
        data = response.json()
        repos.extend(data["items"])
    return repos

def cloneAndPullNotes(repo):
    subprocess.run(["git", "clone", repo["clone_url"]])
    pullGitNotes(repo)

def pullGitNotes(repo):
    print(repo["name"])
    subprocess.run(["git", "fetch", "origin", "refs/notes/*:refs/notes/*"], cwd=repo["name"])

## Get notes details
def getGitNotesCount(repo):
    gitNotesCount = subprocess.run("git notes list | wc -l", shell=True, stdout=subprocess.PIPE, cwd=repo["name"])
    gitNotesCount = gitNotesCount.stdout.decode().strip()
    return int(gitNotesCount)

def getGitNotes(repo):
    result = subprocess.run(["git", "notes", "list"], capture_output=True, check=True, text=True, cwd="wrongsecrets")
    output = result.stdout.split("\n")
    output.remove("") # It feels like there may be a nicer way to do this
    notes = []
    for line in output:
        note = line.split(" ")[1]
        notes.append(note)
    return(notes)

def getNoteContent(note_ref):
    result = subprocess.run(["git", "notes", "show", note_ref], capture_output=True, check=True, text=True, cwd="wrongsecrets")
    return result.stdout

def getNoteCreatedDate(note_ref):
    print("need to do this")

## Save to DB
def saveRepoDetailsToRepoTable(repo, conn):
    conn.sql(
        f"""
            INSERT INTO repos
                (id,
                NAME,
                license,
                stars,
                repo_created_at,
                repo_updated_at)
            VALUES     
                ('{ulid.generate()}',
                '{repo["name"]}',
                '{repo["license"]["key"]}',
                '{repo["stargazers_count"]}',
                '{repo["created_at"]}',
                '{repo["updated_at"]}') 
        """
    )

def getRepoId(repo):
    id = conn.sql(
        f"""
            SELECT id FROM repos
            WHERE name = '{repo["name"]}'
        """
    )
    return id.fetchone()

def saveNotesDetailsToNotesTable(repo_id, note_id, conn):
    noteContent = getNoteContent(note_id)
    noteCreatedDate = getNoteCreatedDate(note_id)
    conn.sql(
        f"""
            INSERT INTO notes
                (id,
                repo_id,
                content,
                note_ref)
            VALUES     
                ('{ulid.generate()}',
                '{repo_id[0]}',
                '{noteContent.replace("'", "''")}',
                '{note_id}') 
        """
    ) # This is really hacky, need to think of a better way. Will other symbols break this?

def updateRepoTableWithNotesDetails(repo, conn):
    conn.sql(
        f"""
            UPDATE repos
            SET 
                has_notes = True
                notes_count = '{gitNotesCount}'
            WHERE NAME = '{repo["name"]}';
        """
    )

## Main   
ulid = ULID()
repos = getRepos()
conn = create_db_and_tables("gitNotesResearch.db")
for repo in repos:
    saveRepoDetailsToRepoTable(repo, conn)
    repoId = getRepoId(repo)
    cloneAndPullNotes(repo)
    if getGitNotesCount(repo) == 0: # This should be != but for the sake of testing it is ==
        gitNotes = getGitNotes(repo)
        for noteId in gitNotes:
            saveNotesDetailsToNotesTable(repoId, noteId, conn)
