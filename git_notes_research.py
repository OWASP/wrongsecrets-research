import modules.setup as setup
import modules.git as git
import modules.db as db

setup.delete_old_db_file("git_notes_research.db")
repos = setup.get_repos()
conn = setup.create_db_and_tables("git_notes_research.db")
for repo in repos:
    db.save_repo_details_to_repo_table(repo, conn)
    setup.clone_and_pull_notes(repo)
    repo_id = db.get_repo_id(repo, conn)
    if (
        git.get_notes_count(repo) != 0
    ):
        git_notes = git.get_notes(repo)
        for note_id in git_notes:
            db.save_notes_details_to_notes_table(repo_id, note_id, conn, repo)
        db.update_repo_notes_count(repo_id, conn)
        db.update_repo_notes_bool(True, repo_id, conn)
    else:
        db.update_repo_notes_bool(False, repo_id, conn)
    setup.delete_repo(repo)

