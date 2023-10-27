import time
from ulid import ULID
import modules.git as git
import requests

ulid = ULID()


def save_repo_details_to_repo_table(repo, conn):
    for i in range(3):
        contributors = get_contributor_count(repo["contributors_url"])
        if contributors is not None:
            break
        else:
            print(
                f"No contributors could be found for {repo['name']}: Retrying {i + 1}"
            )
            continue
    if repo.get("license", None) and repo["license"].get("key", None):
        conn.sql(
            """
    INSERT INTO repos
    (id, NAME, license, stars, total_contributors, repo_created_at, repo_updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
            (
                ulid.generate(),
                repo["name"],
                repo["license"]["key"],
                repo["stargazers_count"],
                contributors,
                repo["created_at"],
                repo["updated_at"],
            ),
        )
    else:
        conn.sql(
            """
    INSERT INTO repos
    (id, NAME, stars, total_contributors, repo_created_at, repo_updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
            (
                ulid.generate(),
                repo["name"],
                repo["stargazers_count"],
                contributors,
                repo["created_at"],
                repo["updated_at"],
            ),
        )
    conn.commit()


def get_repo_id(repo, conn):
    id = conn.sql(
        f"""
            SELECT id 
            FROM repos
            WHERE name = '{repo["name"]}'
        """
    )
    return id.fetchone()


def get_contributor_count(contributors_url):
    contributors = []
    page = 1
    token = "__ADD YOUR PAT HERE__"
    headers = {"Authorization": f"Bearer {token}"}
    while True:
        response = requests.get(
            f"{contributors_url}?page={page}&per_page=100", headers=headers
        )
        if response.status_code == 200:
            page_contributors = response.json()
            if not page_contributors:
                return len(contributors)
            contributors.extend(page_contributors)
            page += 1
            time.sleep(0.5)
        else:
            print(f"Failed to fetch contributors. Status code: {response.status_code}")
            break


def save_notes_details_to_notes_table(repo_id, note_id, conn, repo):
    note_content = git.get_note_content(note_id, repo)
    note_created_date = git.get_note_created_date(note_id, repo)
    note_author = git.get_note_author(note_id, repo)
    conn.sql(
        f"""
            INSERT INTO notes
                (id,
                repo_id,
                content,
                note_ref,
                author,
                note_created_at
                )
            VALUES     
                ('{ulid.generate()}',
                '{repo_id[0]}',
                '{note_content.replace("'", "''")}',
                '{note_id}',
                '{note_author}',
                '{note_created_date}')
        """
    )


def update_repo_notes_count(repo_id, conn):
    notes_count = conn.sql(
        f"""
                                SELECT COUNT(*) 
                                FROM notes
                                WHERE repo_id = '{repo_id[0]}'
                            """
    )
    conn.sql(
        f"""
            UPDATE repos
            SET notes_count = {notes_count.fetchone()[0]}
            WHERE id = '{repo_id[0]}'
        """
    )


def update_repo_notes_bool(bool, repo_id, conn):
    conn.sql(
        f"""
            UPDATE repos
            SET has_notes = '{bool}'
            WHERE id = '{repo_id[0]}'
        """
    )
