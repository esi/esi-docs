Repository for the [EVE Developer Documentation](https://developers.eveonline.com/docs/) website.

# Local environment

This project works best when you have a local environment set up, preferably via WSL2.
This will allow you to run the project locally and see the change you make in real-time.

### Fork the repository

Submitting a pull request with your changes is the preferred way to contribute to this project.
To do this, you will need to fork the repository so you can make changes to your own copy of the project.

This assumes you have a GitHub account already, so if you don't, you'll need to create one.

Head to [this page](https://github.com/esi/esi-docs/fork) and follow the instructions there to fork the repository.

### Clone the repository

Now that you have your own clone, you will need to clone it on your local machine.
If you are using Visual Studio Code, you can do this by clicking the `Clone Repository` button on the start page.

If you are using the command line, you can do this by running the following command:

```bash
git clone <path-to-your-fork>
cd esi-docs
```

### Creating a virtual environment

This project uses python, so it is recommended to create a virtual environment to manage the dependencies.
This ensures that you don't clutter your system python installation with dependencies that are only needed
for this project.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

When you are starting a new terminal session, you will need to activate the virtual environment again.
You can do this by navigating to the project directory and running the `source .venv/bin/activate` command.

Using make:
```bash
make init
```

### Installing dependencies

Now that you have a virtual environment set up, you can install the dependencies for this project.
This can be done by running the following command:

```bash
pip install -r requirements.txt
```

### Running the project

Now that you have the dependencies installed, you can run the project locally.
This can be done by running the following command:

```bash
mkdocs serve
```

This will start a local webserver that you can access by navigating to `http://127.0.0.1:8000/docs/` in your browser.

You can close the server by pressing `Ctrl+C` in the terminal.

Using make:
```bash
make serve
```

### Making changes

While the server is running, you can make changes to the project and see them reflected in real-time.
Edit the files under /docs/ and save them.
The server will automatically rebuild the relevant pages and refresh the page for you.

# Best practices

When creating a pull request, there are a few best practices that you should follow to help create a smooth review process.
To help with this, we have created a checklist that you can use to ensure that your pull request meets the standards we wish to maintain.

### Write small PRs

A pull request should fulfil a single purpose, and should not contain unrelated changes.
This makes it easier to review the changes and understand the purpose of the pull request.

### Review your own changes

Before submitting, double-check your changes to ensure that you haven't missed anything.
This includes checking for typos, broken links, and other issues that might have been introduced.

### Write good commit messages

Commit messages should be concise and descriptive.
They don't need to be long, but they should provide enough context to understand the purpose of the commit.

If you are working locally, you can always squash your commits before submitting the pull request to avoid cluttering the commit history with unnecessary commits.

### Follow existing conventions

When making changes, try to follow the existing conventions in the project.
This includes things like naming conventions, file structure, and formatting.
This helps maintain consistency, and makes it easier for others to understand your changes.
If you feel like a convention should be changed, feel free to discuss it in the pull request, or create a separate discussion for that.

# Notes about the review process.

Pull request reviews are an important part of the contribution process.
They help ensure that changes are of high quality, and that they meet the standards of the project.
This often involves providing feedback, asking questions, and requesting changes.

It is important to remember that that feedback is about the code, not the person.
It is not a personal attack, but rather a way to improve the quality of the project.
It is also important to remember that everyone makes mistakes, and that feedback is an opportunity to learn and grow.
If you do not understand a comment, or if you disagree with it, feel free to ask for clarification or to discuss it further, but do so in a respectful and constructive manner.

When reviewing a pull request, it is important to be respectful and constructive.
This means providing feedback in a clear and concise manner, and avoiding personal attacks or negative language.
It also means being open to feedback yourself, and being willing to learn from others.

It should be noted that this also means that sometimes pull requests will be rejected.
A rejection does not mean that your contribution is not valued, but rather that it is not a good fit for the project at this point in time.

# Conventions

## Snippets

There are various places where we insert code snippets into the documentation to better visualize what's going on.

Snippets are placed in the `snippets` folder, grouped in subfolders by topic. Each snippet is a separate file per language (based off of its extension), with a central (autogenerated) `.md` file that includes the snippets for each language. If you want to add a new language to a snippet, create the new file, and the build pipeline will automatically include it in the final documentation.

If you are adding the first snippet for a new language, it will need to be defined in `scripts/generate-snippets.py`, so that the build pipeline knows to include the file extension when searching for snippets, and what language to use for syntax highlighting.

When adding new snippets, write it in any supported/configured language, and include it as follows:

```markdown
--8<-- "snippets/path/to-filename.md"
```

Note the .md extension to use the autogenerated file, and the `--8<--` to indicate that this is a snippet include.

If a certain topic contains a lot of snippets, it might also be time to create a guide page for that topic, so that newer users can use that guide as a starting point.
