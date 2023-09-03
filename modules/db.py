from ulid import ULID
import modules.git as git

ulid = ULID()


def save_repo_details_to_repo_table(repo, conn):
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


def get_repo_id(repo, conn):
    id = conn.sql(
        f"""
            SELECT id 
            FROM repos
            WHERE name = '{repo["name"]}'
        """
    )
    return id.fetchone()


def save_notes_details_to_notes_table(repo_id, note_id, conn, repo):
    note_content = git.get_note_content(note_id, repo)
    note_created_date = git.get_note_created_date(note_id)
    note_author = git.get_note_author(note_id)
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
    notes_count = conn.sql(f"""
                                SELECT COUNT(*) 
                                FROM notes
                                WHERE repo_id = '{repo_id[0]}'
                            """)
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
