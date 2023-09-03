import subprocess


def get_notes_count(repo):
    git_notes_count = subprocess.run(
        "git notes list | wc -l", shell=True, stdout=subprocess.PIPE, cwd="repositories/" + repo["name"]
    )
    git_notes_count = git_notes_count.stdout.decode().strip()
    return int(git_notes_count)


def get_notes(repo):
    result = subprocess.run(
        ["git", "notes", "list"],
        capture_output=True,
        check=True,
        text=True,
        cwd="repositories/" + repo["name"],
    )
    output = result.stdout.split("\n")
    output.remove("")
    notes = []
    for line in output:
        note = line.split(" ")[1]
        notes.append(note)
    return notes


def get_note_content(note_ref, repo):
    result = subprocess.run(
        ["git", "notes", "show", note_ref],
        capture_output=True,
        check=True,
        text=True,
        cwd="repositories/" + repo["name"],
    )
    return result.stdout


def get_note_created_date(note_id, repo):
    result = subprocess.run(
        ["git", "log", "-1", "--date=format-local:%Y-%m-%d %H:%M:%S", "--pretty=format:\"%cd\"", note_id],
        capture_output=True,
        check=True,
        text=True,
        cwd="repositories/" + repo["name"],
    )
    result_with_ms = result.stdout.replace("\"", "") + ".123Z"
    return result_with_ms


def get_note_author(note_id, repo):
    result = subprocess.run(
        ["git", "show", "-q", note_id],
        capture_output=True,
        check=True,
        text=True,
        cwd="repositories/" + repo["name"],
    ).stdout
    author_line = [line for line in result.split('\n') if line.startswith("Author:")][0]
    author_info = author_line.split(": ", 1)[1].strip()
    return author_info
