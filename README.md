# Git Notes Research

## To do

- [x] Research what DuckDB is
- [ ] Research what the other one is
- [ ] Bring data into a lightweight DB
- [x] Decide on what data should be extracted

## Data to be extracted

### Repo table

- ID - ULID - PK
- Name of repo - string
- Does it have any notes - Bool
- Amount of notes - nullable int
- License - Emum
- Last time a note was created - timestamp
- First time a note was created - timestamp
- Amount of stars - int
- Repo creation date - timestamp
- Last commit to main branch - timestamp
- Commits in last 3 months - int (This is going to be tricky to figure out, not sure if worth it)

### Notes table

- ID - ULID - PK
- RepoID - ULID = Repo table ID
- Note content = String
- Note creation date - timestamp
- Commit ref - string
- Author - string (Github username)
