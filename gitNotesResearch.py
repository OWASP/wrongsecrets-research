import requests
import json
import os
import subprocess

# Define the API endpoint and parameters
api_url = "https://api.github.com/search/repositories"
params = {
    "q": "stars:>10000", # Search for repositories with more than 0 stars
    "sort": "stars", # Sort the results by stars
    "per_page": 100 # Get 100 results per page
}

# Initialize an empty list to store the results
repos = []

# Loop over the page numbers from 1 to 10
for page in range(1, 11):
    # Update the page parameter in the params dictionary
    params["page"] = page
    # Make the API request and get the JSON response
    response = requests.get(api_url, params=params)
    data = response.json()
    # Append the items array from the response to the repos list
    repos.extend(data["items"])

# Extract the relevant information from the response
repo_names = [repo["name"] for repo in repos] # Get the names of the repositories
repo_urls = [repo["clone_url"] for repo in repos] # Get the urls of the repositories

# Print the names and urls of the top 100 repositories by stars
for name, url in zip(repo_names, repo_urls):
    print(name, url)

# Create a folder called "repositories" next to the script
try:
    os.mkdir("repositories")
except:
    print("The directory already exists")

noteCount = 0
# Loop through the repository urls and clone them into the folder
for index, url in enumerate(repo_urls):
    # Clone the repository into the subfolder
    subprocess.run(["git", "clone", url])
    # Create a Repo object for the repository
    subprocess.run(["git", "fetch", "origin", "refs/notes/*:refs/notes/*"], cwd=repo_names[index])
    # List all the git notes using git notes list command
    output = subprocess.check_output(["git", "notes", "list"], cwd=repo_names[index])

    # Convert the output from bytes to string and split it by newline characters
    output = output.decode("utf-8").split("\n")

    # Count the number of lines in the output and print it
    count = len(output) - 1
    print(f"There are {count} notes in the {repo_names[index]} repository.")
    noteCount += count

print(f"There was {noteCount} total notes")