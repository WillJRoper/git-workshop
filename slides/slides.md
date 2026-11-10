---
theme: default
title: Version Control with Git
info: One-hour workshop. History, the mental model, good habits, and a bug hunt with git bisect.
author: Will Roper
colorSchema: dark
aspectRatio: 16/9
fonts:
  sans: JetBrains Mono
  mono: JetBrains Mono
  provider: none
transition: fade
mdc: true
routerMode: hash
layout: center
class: text-center
---

<div class="muted text-sm mb-6">will@laptop:~$ ./workshop --topic=git --minutes=60</div>

<h1 class="blink !text-5xl !mb-4">Version Control<br>with Git</h1>

<div class="text-lg mt-8">Will Roper</div>

<div class="muted text-sm mt-1">History, the mental model, good habits, and a bug hunt</div>

<img src="/img/oxford_logo.png" class="absolute left-6 bottom-6 h-16" alt="University of Oxford" />
<img src="/img/oxrse_logo.png" class="absolute right-6 bottom-6 h-16" alt="OxRSE" />

<div class="absolute bottom-6 left-0 right-0 text-center text-xs muted">Condensed from the OxRSE <a href="https://github.com/OxfordRSE/training-slides-core" target="_blank">version control</a> training deck</div>

<!--
15 minutes of slides, 45 hands-on. Keep moving.
-->

---

# Agenda

<div class="body">
<div class="term text-lg leading-loose">
<div class="term-bar"><span /><span /><span /></div>

<div class="muted">$ git log --oneline --reverse</div>
<div><span class="warn">a1f3c0d</span> Why version control exists</div>
<div><span class="warn">9c02e1b</span> How Git thinks: working tree, staging, local, remote</div>
<div><span class="warn">77be4a2</span> Branches, merges, pull requests</div>
<div><span class="warn">5d3e831</span> Habits: good, bad, and <span class="bad">never</span></div>
<div><span class="warn">b15ec7f</span> <span class="accent">(HEAD -> main)</span> Hunt a bug with git bisect, fix it, open a PR</div>

</div>

<div class="mt-8 text-center muted">15 minutes of talking. Then your terminal.</div>
</div>

---

# Which Of These Have You Done?

<div class="body">
<div class="grid grid-cols-2 gap-4 text-sm">
<div class="term warn-card"><div class="accent mb-1">[1] "I lost my code"</div><div class="muted">One laptop. Disk died, got stolen, or <code>rm -rf</code> in the wrong directory.</div></div>
<div class="term warn-card"><div class="accent mb-1">[2] final_v7_REAL_final2.py</div><div class="muted">Versions tracked by filename. Which one made Figure 3?</div></div>
<div class="term warn-card"><div class="accent mb-1">[3] "I can't reproduce my results"</div><div class="muted">Script changed since the paper went in. The old version is gone.</div></div>
<div class="term warn-card"><div class="accent mb-1">[4] "Can you email me your code?"</div><div class="muted">Two people edit. One overwrites the other. Nobody notices for a month.</div></div>
</div>

<div v-click class="mt-6 text-center text-lg">Same root cause: <strong>no structured history</strong>. No safe way to undo, explore, or combine work.</div>
</div>

<!--
Remote poll via chat. Wait ~20 s, read a few out.
-->

---

# What Version Control Is

<div class="body">
<div class="grid grid-cols-2 gap-10">
<div>

- A tool that records **changes** to files: what, who, when, and *why*
- Built for plain text: code, config, docs, tests, LaTeX
- Like Wikipedia page history, or Track Changes, but for the whole project

</div>
<div>

<div v-click>

- **Backup**: every state recoverable, copy off-machine <span class="muted">(1)</span>

</div>
<div v-click>

- **Reproducibility**: tag the exact version that made the paper <span class="muted">(2, 3)</span>

</div>
<div v-click>

- **Collaboration**: independent edits combined, conflicts surfaced <span class="muted">(4)</span>

</div>
</div>
</div>
</div>

---
class: section-card
---

# ./history --brief

<div class="muted mt-4">fifty years in one slide</div>

---

# A Short History

<div class="body">
<div class="timeline">
<div v-click class="tl"><b>1972</b>SCCS<span class="muted">one file at a time, deltas</span></div>
<div v-click class="tl"><b>1982</b>RCS<span class="muted">reverse deltas</span></div>
<div v-click class="tl central"><b>1986</b>CVS<span class="muted">central server, concurrent edits</span></div>
<div v-click class="tl central"><b>2000</b>Subversion<span class="muted">atomic commits, still central</span></div>
<div v-click class="tl dist"><b>2005</b>Git, Mercurial<span class="muted">distributed: every clone holds the full history</span></div>
<div v-click class="tl dist"><b>2008</b>GitHub<span class="muted">Git + web + social</span></div>
</div>

<div class="flex gap-8 justify-center mt-6 text-xs muted">
<span><span class="theory">▬</span> centralised: one server owns the history</span>
<span><span class="accent">▬</span> distributed: everyone owns the history</span>
</div>

<div v-click class="term mt-10 text-sm w-fit mx-auto">Git: written by Linus Torvalds in about two weeks in 2005, after the Linux kernel's previous tool revoked its free licence.</div>
</div>

---

# Why Git Won

<div class="body">
<div class="grid grid-cols-[1.1fr_1fr] gap-10 items-center">
<div>

- **Distributed.** No single point of failure. Works offline.
- **Snapshots, not deltas.** Each commit stores the whole tree. Unchanged files are stored once, by hash.
- **Branches are pointers**, not copies. Instant.
- Built for **thousands** of contributors. Your group of three is fine.
- **GitHub** turned it into a network.

</div>
<div class="term text-sm">
<div class="term-bar"><span /><span /><span /></div>
<div class="muted mb-2">$ git log --stat</div>
<div class="grid grid-cols-4 gap-2 text-center">
<div class="muted">C1</div><div class="muted">C2</div><div class="muted">C3</div><div class="muted"></div>
<div class="snap">A1</div><div class="snap ref">A1</div><div class="snap">A2</div><div class="muted text-xs self-center">plot.py</div>
<div class="snap">B1</div><div class="snap">B2</div><div class="snap ref">B2</div><div class="muted text-xs self-center">test_plot.py</div>
<div class="snap">C1</div><div class="snap ref">C1</div><div class="snap ref">C1</div><div class="muted text-xs self-center">README.md</div>
</div>
<div class="muted text-xs mt-3"><span class="snap ref inline-block px-2">grey</span> = unchanged, points at the earlier blob</div>
</div>
</div>
</div>

<style>
.snap { border: 1px solid var(--line); border-radius: 4px; padding: 2px 0; color: var(--warn); }
.snap.ref { color: #555; border-style: dashed; }
</style>

---
class: section-card
---

# git --mental-model

<div class="muted mt-4">four places your code lives</div>

---
clicks: 7
---

# The Four Places Your Code Lives

<div class="body">
<FourPlaces :step="$clicks" />

<div v-click="7" class="text-center mt-4 text-sm muted">Run <code>git status</code> constantly. It tells you which box every change is sitting in.</div>
</div>

<!--
Click through: add, commit, push, fetch, pull, clone, status.
Emphasise: commit is local. Nothing leaves your machine until you push.
Staging lets you split one editing session into several commits.
-->

---

# Vocabulary

<div class="body">
<div class="grid grid-cols-3 gap-4 text-sm">
<div class="term"><div class="accent mb-1">repository</div><div class="muted">Your project folder plus a hidden <code>.git/</code> holding the full history. You rarely look inside.</div></div>
<div class="term"><div class="accent mb-1">commit</div><div class="muted">A labelled snapshot of the whole project: author, date, message, and a pointer to its parent.</div></div>
<div class="term"><div class="accent mb-1">branch</div><div class="muted">A movable pointer to a commit. An independent line of work. <code>HEAD</code> is where you are now.</div></div>
<div class="term"><div class="accent mb-1">working tree</div><div class="muted">The files you actually see and edit.</div></div>
<div class="term"><div class="accent mb-1">staging area</div><div class="muted">The changes you have picked for the <em>next</em> commit. Lets you commit part of your edits.</div></div>
<div class="term"><div class="accent mb-1">remote</div><div class="muted">A copy hosted elsewhere (GitHub). Your off-site backup and the meeting point for collaborators.</div></div>
</div>
</div>

---

# A Commit

<div class="body">
<div class="grid grid-cols-[1.2fr_1fr] gap-8 items-center">
<div class="term text-sm">
<div class="term-bar"><span /><span /><span /></div>

```text {*}{lines:false}
$ git show 5d3e831
commit 5d3e831e867d5a4f1a83750ad82fd46041ac58e5
Author: Ada Lovelace <ada@example.org>
Date:   Tue Nov 4 10:12:33 2026 +0000

    Stop axis labels being clipped in saved figures

diff --git a/plot.py b/plot.py
@@ -22,7 +22,7 @@ def save(fig, path):
-    fig.savefig(path)
+    fig.savefig(path, bbox_inches="tight")
```

</div>
<div class="text-sm">

- **Hash**: computed from content + parent. Tamper-evident chain.
- **Author, date**
- **Message**: says *why*. The diff already says what.
- **Snapshot** of every file
- **Parent**: this is what makes it a history

<div class="muted mt-4 text-xs">
<code>git diff a1f3 5d3e</code> compares any two points.
</div>

</div>
</div>

<div v-click class="mt-4">
<svg viewBox="0 0 960 90" class="chain">
  <text x="0" y="24" class="cmd">$ git log --oneline</text>
  <text x="0" y="60" class="dots">···</text>
  <line x1="60" y1="55" x2="780" y2="55" class="edge" />
  <circle cx="240" cy="55" r="13" class="node" /><text x="240" y="86" class="lbl">c91a0f2</text>
  <circle cx="420" cy="55" r="13" class="node" /><text x="420" y="86" class="lbl">7b2d4e9</text>
  <circle cx="600" cy="55" r="13" class="node" /><text x="600" y="86" class="lbl">a1f3c02</text>
  <circle cx="780" cy="55" r="13" class="node head" /><text x="780" y="86" class="lbl head">5d3e831</text>
  <text x="780" y="24" class="ref">HEAD -> main</text>
  <text x="250" y="24" class="note">newest first, each pointing at its parent</text>
</svg>
</div>
</div>

<style>
.chain { width: 100%; height: auto; overflow: visible; font-family: var(--mono); }
.chain .edge { stroke: #555; stroke-width: 3; }
.chain .node { fill: #555; stroke: #000; stroke-width: 3; }
.chain .node.head { fill: var(--accent); }
.chain .lbl { fill: var(--muted); font-size: 15px; text-anchor: middle; }
.chain .lbl.head { fill: var(--ink); }
.chain .ref { fill: var(--accent); font-size: 15px; font-weight: 700; text-anchor: middle; }
.chain .cmd { fill: var(--warn); font-size: 15px; }
.chain .dots { fill: #555; font-size: 22px; }
.chain .note { fill: var(--muted); font-size: 14px; }
</style>

---
clicks: 3
---

# Branching

<div class="muted text-sm -mt-4 mb-2">A branch is a pointer. Commits on it don't disturb <code>main</code>.</div>

<BranchGraph :step="$clicks" />

<div v-click="3" class="text-sm mt-2">

- One branch per task. Short-lived. Named for the change.
- <code>git switch main</code> flips your working tree back instantly.

</div>

---

# Merging

<BranchGraph :step="4" />

<div class="grid grid-cols-2 gap-8 text-sm mt-2">
<div v-click="1">
<div class="accent">usually automatic</div>
Different files, or different lines of the same file: Git combines them. No human needed.
</div>
<div v-click="2">
<div class="bad">sometimes a conflict</div>

```text {*}{lines:false}
<<<<<<< HEAD
    fig.savefig(path, dpi=150)
=======
    fig.savefig(path, dpi=300)
>>>>>>> new-feature
```

Same lines edited on both sides. Git stops, marks the file, you choose. Then <code>add</code> and <code>commit</code>.
</div>
</div>

<!--
Conflicts aren't failures; it's Git refusing to guess. We'll probably see one live when the second PR lands.
-->

---

# Live: Watch The Graph Move

<div class="body">
<div class="grid grid-cols-[1fr_1.2fr] gap-10 items-center">
<div>

<a href="https://git-school.github.io/visualizing-git/" target="_blank" rel="noopener" class="term block text-center !border-solid !border-b-solid" style="border-color: var(--theory)"><div class="muted text-sm">$ open</div><div>git-school.github.io/<br>visualizing-git</div></a>

<div class="muted text-sm mt-4">A sandbox. Nothing can break. Open it and type along.</div>

</div>
<div class="term text-sm">
<div class="term-bar"><span /><span /><span /></div>

```bash {*}{lines:false}
git commit
git commit
git checkout -b feature
git commit
git checkout main
git commit
git merge feature
```

</div>
</div>
</div>

<!--
Two minutes max. Branch pointer moves, merge makes a two-parent node.
Optionally `git checkout HEAD~2` to show detached HEAD, which they'll meet in bisect.
-->

---
clicks: 5
---

# Working With A Remote

<div class="body">
<RemoteFlow :step="$clicks" />

<div v-click="5" class="text-sm mt-4">

- The remote is just another copy of the repo. Off-machine backup for free.
- Same history everywhere. Commit locally, <code>push</code> to share, <code>pull</code> to catch up.

</div>
</div>

<div class="credit">Pushing needs authentication: an SSH key or <code>gh auth login</code>. Set up before today, see the README.</div>

<!--
Build it up: create an empty repo on GitHub, add it as origin, push. Clone it on another machine, push from there, pull back on the laptop.
Point out: nothing special about the remote. It's a clone that happens to live on GitHub.
-->

---
clicks: 4
---

# Working With Others

<div class="muted text-sm -mt-4 mb-2">Someone else's repo. You can't push to it. Fork it.</div>

<div class="body">
<ForkFlow :step="$clicks" />

<div v-click="4" class="text-center text-sm muted mt-4">You don't need write access to contribute. That's the point of forks.</div>
</div>

---
class: section-card
---

# ./habits --good --bad

<div class="muted mt-4">and one you never do</div>

---

# The Everyday Loop

<div class="body">
<div class="grid grid-cols-[1.35fr_1fr] gap-8 items-center">
<div class="term text-sm">
<div class="term-bar"><span /><span /><span /></div>

```bash {*}{lines:false}
git pull                          # start from the latest
git switch -c new-feature         # one branch per task
# ... edit ...
git status                        # what changed?
git diff                          # exactly what changed?
git add plot.py test_plot.py      # pick what goes in
git commit -m "Fix clipped axis labels in saved figures"
git push -u origin new-feature    # first push of a new branch
# then open a Pull Request on GitHub
```

</div>
<div class="text-sm">

- **Commit often.** Small commits are easy to review, revert, and bisect.
- **One idea per commit.** Fix and reformat? Two commits.
- **Message**: imperative, under ~70 characters, says why.
- **Pull before you push.**

</div>
</div>
</div>

---

# Spot The Smell

<div class="muted text-xs -mt-4 mb-3">Fine or not?</div>

<table class="smells">
<tbody>
<tr><td>git commit -m "fix"</td><td><span v-click><span class="verdict no">smell.</span> Fix what? Future you, bisecting at 11pm, will hate this.</span></td></tr>
<tr><td>git commit -m "Clamp timestep to avoid NaN in leapfrog"</td><td><span v-click><span class="verdict ok">good.</span> Imperative, specific, says why.</span></td></tr>
<tr><td>git add .venv/ data/*.hdf5</td><td><span v-click><span class="verdict no">smell.</span> Environments and big data don't belong in history. <code>.gitignore</code> them.</span></td></tr>
<tr><td>git add config.py &nbsp;<span class="muted"># API_KEY = "sk-..."</span></td><td><span v-click><span class="verdict no">never.</span> History is forever and clones are public. Rotate the key today.</span></td></tr>
<tr><td>git commit -am "Refactor + fix bug + new plots" &nbsp;<span class="muted"># 47 files</span></td><td><span v-click><span class="verdict no">smell.</span> Unreviewable, unrevertable, unbisectable.</span></td></tr>
<tr><td>git push --force origin main</td><td><span v-click><span class="verdict no">smell.</span> Rewrites shared history. Everyone's clone now disagrees with the remote.</span></td></tr>
<tr><td>git commit -m "WIP" &nbsp;<span class="muted"># own branch, tidied before PR</span></td><td><span v-click><span class="verdict ok">fine.</span> Your branch, your mess. Clean it before anyone else reads it.</span></td></tr>
</tbody>
</table>

---

# What Belongs In A Repo

<div class="body">
<div class="grid grid-cols-2 gap-6 text-sm">
<div class="term good">
<div class="accent mb-2">yes</div>

- Source code, scripts, notebooks (outputs stripped)
- Config, environment specs (<code>requirements.txt</code>)
- Docs, tests, small test fixtures
- Anything plain-text whose line diffs mean something

</div>
<div class="term bad-card">
<div class="bad mb-2">no</div>

- Simulation outputs, large data, regenerable figures
- Binaries, <code>__pycache__/</code>, <code>.venv/</code>, <code>build/</code>
- Editor and OS junk: <code>.DS_Store</code>, <code>.idea/</code>
- **Secrets.** Keys, passwords, tokens, personal data

</div>
</div>

<div v-click class="term text-sm mt-6 w-fit mx-auto">
<div class="muted">$ cat .gitignore</div>
<div>__pycache__/<br>.venv/<br>*.hdf5<br>.DS_Store</div>
</div>
</div>

---
class: section-card
---

# git bisect

<div class="muted mt-4">binary search over your history</div>

---
clicks: 9
---

# Finding The Commit That Broke Things

<GitBisect :step="Math.min($clicks, 7)" />

<div class="grid grid-cols-[1.2fr_1fr] gap-8 text-sm mt-1">
<div class="term">
<div class="term-bar"><span /><span /><span /></div>

```bash {*}{lines:false}
git bisect start
git bisect bad              # HEAD is broken
git bisect good v0.1        # this tag worked
# git checks out the middle commit. test it.
git bisect good             # or: git bisect bad
# ... repeat ~log2(N) times ...
# "<sha> is the first bad commit"
git bisect reset            # back to where you were
```

</div>
<div>

- 64 commits: 6 tests. 1000 commits: about 10.
- You don't need to understand the code. You need a test.
<div v-click="8">

- Automate it: <code>git bisect run python check.py</code> <span class="muted">(exit 0 = good)</span>

</div>
<div v-click="9">

- Only works with small commits and honest messages. This is why we nag.

</div>
</div>
</div>

<!--
Walk the animation: each click tests the midpoint and halves the range.
During bisect you're in detached HEAD. Always `git bisect reset` before branching.
-->

---

# Your Turn: The Glider Died

<div class="body">
<div class="grid grid-cols-[1.3fr_1fr] gap-8 items-start">
<div class="text-sm">

1. **Fork** <a href="https://github.com/WillJRoper/git-bisect-glider-hunt" target="_blank">WillJRoper/git-bisect-glider-hunt</a>, then <code>git clone</code> your fork.
2. Run <code>python life.py glider</code>. It should fly forever. It dies. Tag <code>v0.1</code> worked.
3. <code>git bisect</code> to find the commit that killed it. Read its diff.
4. <code>git bisect reset</code>, then <code>git switch -c fix-glider</code>.
5. Fix it. Add a test so it can't come back. <code>git add</code>, <code>git commit</code>.
6. <code>git push -u origin fix-glider</code>. Open a Pull Request against the original repo.

</div>
<div class="term text-sm">
<div class="term-bar"><span /><span /><span /></div>
<div class="muted">$ cat HELP.txt</div>
<div class="mt-2">Stuck? Ask.</div>
<div class="mt-2">Full instructions in the README.</div>
<div class="mt-2">No local git? Open the fork in <strong>Codespaces</strong>.</div>
<div class="mt-4 muted">We review the PRs together at the end.</div>
</div>
</div>
</div>

<!--
~40 minutes. Share the README link in chat. Watch the PR list; merge the first good one live, then show what happens to the rest.
-->
