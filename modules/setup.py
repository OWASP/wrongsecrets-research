import requests
import subprocess
import duckdb
import os


def delete_old_db_file(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
            print(f"Database file '{filename}' has been deleted.")
        except Exception as e:
            print(f"Error deleting the database file: {e}")
    else:
        print(f"Database file '{filename}' does not exist.")


def create_db_and_tables(db_name):
    conn = duckdb.connect(db_name, read_only=False)
    conn.execute(
        f"""CREATE TABLE IF NOT EXISTS repos
            (
                        id                 string NOT NULL,
                        name               varchar(255) NOT NULL,
                        license            string NULL,
                        stars              int NOT NULL,
                        has_notes          bool NULL,
                        notes_count        int NULL,
                        total_contributors int NOT NULL,
                        repo_created_at    TIMESTAMP NOT NULL,
                        repo_updated_at    TIMESTAMP NOT NULL,
                        created_at         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
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


def get_repos():
    repos = []
    api_url = "https://api.github.com/search/repositories"
    params = {"q": "stars:>10000", "sort": "stars", "per_page": 100}
    for page in range(1, 2):
        params["page"] = page
        response = requests.get(api_url, params=params)
        data = response.json()
        repos.extend(data["items"])
    return repos


def clone_and_pull_notes(repo):
    subprocess.run(["git", "clone", repo["clone_url"]], cwd="repositories/")
    pull_git_notes(repo)


def delete_repo(repo):
    subprocess.run(["rm", "-rf", repo["name"]], cwd="repositories/")


def pull_git_notes(repo):
    subprocess.run(
        ["git", "fetch", "origin", "refs/notes/*:refs/notes/*"],
        cwd="repositories/" + repo["name"],
    )
