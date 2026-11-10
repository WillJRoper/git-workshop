# git-workshop

A one-hour, remote-friendly introduction to git: fifteen minutes of slides,
then a hands-on bug hunt with `git bisect`.

- Slides: <https://willjroper.github.io/git-workshop/>
- Exercise repo: <https://github.com/WillJRoper/git-bisect-glider-hunt>

## Running order

| Time | What |
|------|------|
| 0:00 | Why version control, a short history, how git thinks about your files |
| 0:05 | Commits, branches, merging, remotes, forks and pull requests |
| 0:12 | Good and bad habits, `git bisect` |
| 0:15 | Exercise: fork the glider repo, bisect the bug, fix it on a branch, add a test, open a PR |
| 0:55 | Wrap up |

Participants need a GitHub account, git, Python 3, and a way to push to GitHub
(`gh auth login` or an SSH key) before the session. The exercise README
covers this. GitHub Codespaces works for anyone without a local setup.

## Layout

```
slides/     Slidev deck (slides.md, style.css, components/)
exercise/   seed_history.py, which generates the exercise repository
.github/    Builds the slides and deploys them to GitHub Pages on push to main
```

## Slides

```bash
cd slides
npm install
npm run dev                   # live preview at http://localhost:3030
npm run build                 # static site in slides/dist
npm run export -- --with-clicks   # PDF
```

The deck uses the terminal-style theme from my Durham colloquium talk.
Content is condensed and paraphrased from the Oxford RSE
[version control](https://github.com/OxfordRSE/training-slides-core)
training deck.

## Regenerating the exercise repository

The exercise repo is a seeded history: forty realistic commits from four fictional
authors, a `v0.1` tag that works, and one commit that quietly breaks the
glider. The script writes every commit, checks the tests pass at each one,
and checks the glider dies at exactly the intended commit.

```bash
python exercise/seed_history.py /path/to/git-bisect-glider-hunt
```

It refuses to overwrite an existing directory. The exercise repo does not
contain the script, so participants cannot grep for the answer. Push the
result to GitHub as a fresh repository. Between workshops, delete merged
fix branches on the exercise repo and leave `main` alone, or regenerate it.
