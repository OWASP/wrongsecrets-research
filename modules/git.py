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


def get_note_created_date(note_ref):
    print("need to do this")
