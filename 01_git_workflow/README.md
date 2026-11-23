# 01 · Git workflow

Exercise from the slides ("Your first git workflow", slide 26). It covers the full beginner workflow in 11 parts: config, first repo, commits, diff/log, branches, a bash script on a feature branch, merging, pushing to GitHub, deleting and cloning back, and reflection questions.

> Run these commands yourself in a terminal: the point of the exercise is to build the reflex. This file is the reference solution.

## Parts 1–5: setup, first repository, commits, exploration

```bash
git --version
git config --global user.name "Louis Khousakoun"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main

mkdir git-practice && cd git-practice
git init
echo "# Git practice" > README.md

git status                      # README.md is untracked (red)
git add README.md               # stage it (green)
git commit -m "Add README"      # snapshot
git log                         # full history

echo "Learning Git step by step." >> README.md
git status                      # modified
git diff                        # what changed vs the last commit
git add README.md
git commit -m "Describe the purpose of the repo"
git log --oneline               # compact history
```

## Parts 6–8: branch, bash script on a branch, merge

```bash
git branch                       # list branches (* = current)
git switch -c feature/install-script   # create + switch (older: git checkout -b)
git branch                       # verify

cp ../scripts/install_dev_env.sh .     # or write it (see scripts/install_dev_env.sh)
chmod +x install_dev_env.sh
git add install_dev_env.sh
git commit -m "Add development environment install script"

git switch main
git merge feature/install-script # fast-forward merge
git log --oneline --graph --all
git branch -d feature/install-script
```

## Parts 9–10: push to GitHub, delete and clone back

```bash
# create an EMPTY public repo "git-practice" on github.com first (no README)
git remote add origin https://github.com/<your-username>/git-practice.git
git push -u origin main

cd .. && rm -rf git-practice                  # the local copy is gone…
git clone https://github.com/<your-username>/git-practice.git
cd git-practice && git log --oneline          # …but the full history came back
```

## Part 11: reflection questions

| Question | Answer |
|---|---|
| Why use version control? | Full history of who changed what and when, the ability to undo mistakes, safe parallel work on branches, collaboration, and an off-site backup on GitHub. |
| Staging vs committing? | `git add` puts changes in the staging area, which is the draft of the next snapshot. You choose exactly what goes in. `git commit` records that draft permanently in history with a message. |
| Why branches? | To develop a feature or fix in isolation without breaking `main` (which should stay production-ready), then merge it once it works. |
| What makes a good commit message? | Short, imperative, specific: "Fix null pointer in login handler", not "updates". It should explain what changed and, if needed, why. |
| Three classic mistakes | Not committing often enough; no `.gitignore` (committing `__pycache__/`, `.env`, API keys); panicking on merge conflicts instead of reading the `<<<<<<<` / `=======` / `>>>>>>>` markers. |
