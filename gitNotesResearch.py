import requests
import os
import subprocess
import duckdb
from ulid import ULID


def create_db_and_table(db_name, table_name):
    conn = duckdb.connect(db_name, read_only=False)
    conn.execute(
        f"""CREATE TABLE IF NOT EXISTS {table_name}
            (
                        id string NOT NULL,
                        name            varchar(255) NOT NULL,
                        license         string NOT NULL,
                        stars           int NOT NULL,
                        has_notes       bool NULL,
                        notes_count     int NULL
                        repo_created_at datetime NOT NULL,
                        repo_updated_at datetime NOT NULL,
                        created_at      datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at      datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (id)
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


def saveGeneralRepoDetailsToDB(repo, conn):
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

def cloneAndPullNotes(repo):
    subprocess.run(["git", "clone", repo["clone_url"]])
    pullGitNotes(repo)

def pullGitNotes(repo):
    print(repo["name"])
    subprocess.run(["git", "fetch", "origin", "refs/notes/*:refs/notes/*"], cwd=repo["name"])

def saveNotesRepoDetailsToDB(repo):
    gitNotesCount = subprocess.run("git notes list | wc -l", shell=True, stdout=subprocess.PIPE)
    gitNotesCount = gitNotesCount.stdout.decode().strip()
    gitNotesCount = int(gitNotesCount)
    if gitNotesCount != 0:
        conn.sql(
            f"""
                UPDATE repos
                SET 
                    has_notes = True
                    notes_count = '{gitNotesCount}
                WHERE NAME = '{repo["name"]}';
            """
        )
    conn.sql(
            f"""
                UPDATE repos
                SET 
                    notes_count = '{gitNotesCount}
                WHERE NAME = '{repo["name"]}';
            """
        )

ulid = ULID()
repos = getRepos()
conn = create_db_and_table("gitNotesResearch.db", "repos")
for repo in repos:
    saveGeneralRepoDetailsToDB(repo, conn)
    cloneAndPullNotes(repo)
    saveNotesRepoDetailsToDB(repo)
# cloneAndPullNotes(repos)
# saveNotesRepoDetailsToDB()


# conn = duckdb.connect('gitNotesResearch.db', read_only=False)
