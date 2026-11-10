#!/usr/bin/env python3
"""Generate the git-bisect-workshop exercise repository.

Builds a fresh git repo with ~40 realistic commits of a small Game of Life,
four fictional authors, a `v0.1` tag where the glider still flies, and one
refactor commit part-way through that silently breaks it. Every commit is
checked: the unit tests pass throughout, the glider lives at v0.1 and dies
at HEAD.

    python exercise/seed_history.py ../git-bisect-workshop

The target directory must not exist. Do not commit this file to the
exercise repo: it names the culprit.
"""
from __future__ import annotations

import os
import random
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

AUTHORS = {
    "john": ("John Conway", "john.conway@example.org"),
    "ada": ("Ada Lovelace", "ada.lovelace@example.org"),
    "grace": ("Grace Hopper", "grace.hopper@example.org"),
    "margaret": ("Margaret Hamilton", "margaret.hamilton@example.org"),
}
START = datetime(2026, 8, 3, 9, 12)
CULPRIT_MESSAGE = "Extract neighbour counting into its own function"
GOOD_TAG = "v0.1"
GOOD_TAG_AFTER = "Add place() to offset patterns into the grid"
REPO_URL = "https://github.com/WillJRoper/git-bisect-workshop"


class Repo:
    def __init__(self, root: Path):
        self.root = root
        self.files: dict[str, str] = {}
        self.clock = START
        self.rng = random.Random(2026)
        self.n = 0

    # ---- file ops -------------------------------------------------------
    def add(self, path: str, content: str) -> None:
        assert path not in self.files, path
        self.files[path] = content

    def rep(self, path: str, old: str, new: str) -> None:
        text = self.files[path]
        assert text.count(old) == 1, (path, text.count(old), old[:60])
        self.files[path] = text.replace(old, new)

    def app(self, path: str, text: str) -> None:
        self.files[path] += text

    # ---- git ------------------------------------------------------------
    def git(self, *args: str, env: dict | None = None) -> str:
        e = os.environ.copy()
        if env:
            e.update(env)
        return subprocess.run(["git", *args], cwd=self.root, env=e, check=True,
                              capture_output=True, text=True).stdout

    def commit(self, who: str | None, message: str) -> None:
        self.n += 1
        for path, content in self.files.items():
            p = self.root / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
        self.git("add", "-A")
        self.clock += timedelta(hours=self.rng.randint(3, 60), minutes=self.rng.randint(0, 59))
        date = self.clock.strftime("%Y-%m-%dT%H:%M:%S+0100")
        env = {"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
        if who:
            name, email = AUTHORS[who]
            env.update(GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=email,
                       GIT_COMMITTER_NAME=name, GIT_COMMITTER_EMAIL=email)
        self.git("commit", "-q", "-m", message, env=env)
        self.check(message)
        if message == GOOD_TAG_AFTER:
            self.git("tag", "-a", GOOD_TAG, "-m", "First version with a working glider demo", env=env)
        print(f"{self.n:2d}  {message}")

    # ---- verification ---------------------------------------------------
    def py(self, code: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-c", code], cwd=self.root, capture_output=True, text=True)

    def check(self, message: str) -> None:
        if "test_life.py" in self.files:
            r = subprocess.run([sys.executable, "-m", "unittest", "-q"], cwd=self.root, capture_output=True, text=True)
            assert r.returncode == 0, f"tests fail after '{message}':\n{r.stderr}"
        if "glider" in self.files.get("life.py", "") and "def place" in self.files["life.py"]:
            r = self.py(GLIDER_CHECK)
            assert r.returncode in (0, 1), r.stderr
            flies = r.returncode == 0
            seen_culprit = self.n >= CULPRIT_INDEX
            assert flies != seen_culprit, f"glider state wrong after '{message}' (flies={flies})"


GLIDER_CHECK = """
import life
cells = life.place(life.PATTERNS["glider"], 40, 20)
for _ in range(200):
    cells = life.step(cells, 40, 20)
raise SystemExit(0 if len(cells) == 5 else 1)
"""
CULPRIT_INDEX = 28


# =========================================================================
# file contents
# =========================================================================

STEP_V1 = '''def step(alive, width, height):
    """Advance the grid by one generation and return the new live cells."""
    new = set()
    for x in range(width):
        for y in range(height):
            n = sum((x + dx, y + dy) in alive for dx, dy in OFFSETS)
            if n == 3 or (n == 2 and (x, y) in alive):
                new.add((x, y))
    return new
'''

RENDER_V1 = '''

def render(alive, width, height):
    """Return the grid as a block of text, one row per line."""
    rows = []
    for y in range(height):
        rows.append("".join("#" if (x, y) in alive else "." for x in range(width)))
    return "\\n".join(rows)
'''

MAIN_V1 = '''

def main(argv=None):
    parser = argparse.ArgumentParser(description="Conway's Game of Life.")
    parser.add_argument("pattern", help="name of the starting pattern")
    parser.add_argument("--steps", type=int, default=10, help="generations to run")
    args = parser.parse_args(argv)

    width, height = 20, 10
    alive = set(PATTERNS[args.pattern])
    for _ in range(args.steps):
        alive = step(alive, width, height)
    print(render(alive, width, height))


if __name__ == "__main__":
    main()
'''

MAIN_V2 = '''

def main(argv=None):
    parser = argparse.ArgumentParser(description="Conway's Game of Life.")
    parser.add_argument("pattern", help="name of the starting pattern")
    parser.add_argument("--steps", type=int, default=100, help="generations to run")
    args = parser.parse_args(argv)

    width, height = 20, 10
    alive = set(PATTERNS[args.pattern])
    for _ in range(args.steps):
        print("\\033[2J\\033[H" + render(alive, width, height))
        time.sleep(0.1)
        alive = step(alive, width, height)


if __name__ == "__main__":
    main()
'''

MAIN_V3 = '''

def main(argv=None):
    parser = argparse.ArgumentParser(description="Conway's Game of Life.")
    parser.add_argument("pattern", help="name of the starting pattern")
    parser.add_argument("--steps", type=int, default=100, help="generations to run")
    parser.add_argument("--width", type=int, default=40, help="grid width in cells")
    parser.add_argument("--height", type=int, default=20, help="grid height in cells")
    args = parser.parse_args(argv)

    alive = set(PATTERNS[args.pattern])
    for _ in range(args.steps):
        print("\\033[2J\\033[H" + render(alive, args.width, args.height))
        time.sleep(0.1)
        alive = step(alive, args.width, args.height)


if __name__ == "__main__":
    main()
'''

MAIN_V4 = '''

def main(argv=None):
    parser = argparse.ArgumentParser(description="Conway's Game of Life.")
    parser.add_argument("pattern", help="name of the starting pattern")
    parser.add_argument("--steps", type=int, default=100, help="generations to run")
    parser.add_argument("--width", type=int, default=40, help="grid width in cells")
    parser.add_argument("--height", type=int, default=20, help="grid height in cells")
    parser.add_argument("--no-animate", action="store_true", help="print only the final grid")
    args = parser.parse_args(argv)

    alive = set(PATTERNS[args.pattern])
    for _ in range(args.steps):
        if not args.no_animate:
            print("\\033[2J\\033[H" + render(alive, args.width, args.height))
            time.sleep(0.1)
        alive = step(alive, args.width, args.height)
    if args.no_animate:
        print(render(alive, args.width, args.height))


if __name__ == "__main__":
    main()
'''

TESTS_V1 = '''import unittest

from life import PATTERNS, step


class StillLifeTests(unittest.TestCase):
    def test_block_is_stable(self):
        block = PATTERNS["block"]
        self.assertEqual(step(block, 10, 10), block)


class OscillatorTests(unittest.TestCase):
    def test_blinker_has_period_two(self):
        blinker = PATTERNS["blinker"]
        self.assertNotEqual(step(blinker, 10, 10), blinker)
        self.assertEqual(step(step(blinker, 10, 10), 10, 10), blinker)


if __name__ == "__main__":
    unittest.main()
'''

WORKFLOW_V1 = '''name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - run: python -m unittest -v
'''

LICENSE = '''MIT License

Copyright (c) 2026 Will Roper

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

PULSAR = sorted(
    {(x, y) for x in (2, 3, 4, 8, 9, 10) for y in (0, 5, 7, 12)}
    | {(x, y) for y in (2, 3, 4, 8, 9, 10) for x in (0, 5, 7, 12)}
)

README_FINAL = f'''# git-bisect-workshop

A tiny Game of Life with a bug somewhere in its history. The hands-on half of
a one-hour git workshop. Slides: <https://willjroper.github.io/git-workshop/>.

## Get started

1. Click **Fork** at the top right of this page. Keep the defaults.
2. Clone *your* fork, not this repo:

   ```bash
   git clone https://github.com/YOUR-USERNAME/git-bisect-workshop.git
   cd git-bisect-workshop
   ```

3. Run it:

   ```bash
   python life.py glider
   ```

## The problem

The glider should glide diagonally across the grid forever, wrapping at the
edges. Instead it hits the bottom edge and freezes. Tag `v0.1` definitely
worked:

```bash
git switch --detach v0.1
python life.py glider
git switch main
```

The tests pass at every commit, so nobody noticed. Your job: find the commit
that broke it, fix it, add a test that would have caught it, and open a pull
request.

## The exercise

### 1. Find the culprit with `git bisect`

```bash
git bisect start
git bisect bad                 # the commit you are on is broken
git bisect good v0.1           # this tag worked
```

Git checks out a commit halfway between. Test it:

```bash
python life.py glider --steps 200 --no-animate
```

Five live cells in a glider shape means good, anything else means bad.
Then tell git, and it picks the next commit:

```bash
git bisect good    # or
git bisect bad
```

After about five rounds git prints `<sha> is the first bad commit`. Read
what it changed:

```bash
git show <sha>
git bisect reset               # back to main. Do not skip this.
```

Prefer to automate it? Save this as `check_glider.py` next to `life.py`
(untracked files survive checkouts):

```python
import life
cells = life.place(life.PATTERNS["glider"], 40, 20)
for _ in range(200):
    cells = life.step(cells, 40, 20)
raise SystemExit(0 if len(cells) == 5 else 1)
```

then `git bisect run python check_glider.py` does the whole search.

### 2. Fix it on a branch

```bash
git switch -c fix-glider
# edit life.py
python life.py glider          # flies again?
```

### 3. Add the test that was missing

The existing tests only use patterns that sit still in the middle of the
grid. Add a test to `test_life.py` that exercises the glider crossing an
edge. One idea: on a 40 by 20 grid the glider returns to its starting cells
after 160 generations.

```bash
python -m unittest -v
```

### 4. Commit and push

```bash
git status
git diff
git add life.py test_life.py
git commit -m "Fix glider freezing at the bottom edge"
git push -u origin fix-glider
```

### 5. Open a pull request

GitHub prints a link after the push. Open it, make sure the base is
`WillJRoper/git-bisect-workshop` and `main`, write one or two sentences about what
was wrong, and submit. The tests run automatically on the PR.

## Running the demo

```bash
python life.py --list
python life.py glider --width 60 --height 30 --delay 0.02
python life.py pulsar --steps 30 --no-animate
python -m unittest -v
```

## Contributing

Open an issue or a pull request. Keep commits small, one change each, with a
message that says why. Run the tests before you push.
'''


# =========================================================================
# history
# =========================================================================

def build(repo: Repo) -> None:
    r = repo

    r.add("README.md", "# life\n\nConway's Game of Life in plain Python.\n")
    r.add(".gitignore", "__pycache__/\n")
    r.commit("john", "Initial commit")

    r.add("life.py", "OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]\n\n\n" + STEP_V1)
    r.commit("john", "Add a bare Game of Life step function")

    r.rep("life.py", "(1, 0), (1, 1)]\n\n\n",
          "(1, 0), (1, 1)]\n\nPATTERNS = {\n    \"block\": {(0, 0), (1, 0), (0, 1), (1, 1)},\n    \"blinker\": {(0, 1), (1, 1), (2, 1)},\n}\n\n\n")
    r.commit("ada", "Add blinker and block patterns")

    r.app("life.py", RENDER_V1)
    r.commit("ada", "Add render() to draw the grid as text")

    r.rep("life.py", "OFFSETS = [", "import argparse\n\nOFFSETS = [")
    r.app("life.py", MAIN_V1)
    r.commit("grace", "Add a command line entry point")

    r.add("test_life.py", TESTS_V1)
    r.commit("ada", "Add unit tests for the block and blinker")

    r.rep("life.py", "n = sum((x + dx, y + dy) in alive for dx, dy in OFFSETS)",
          "n = sum(((x + dx) % width, (y + dy) % height) in alive for dx, dy in OFFSETS)")
    r.rep("life.py", '"""Advance the grid by one generation and return the new live cells."""',
          '"""Advance the grid by one generation and return the new live cells.\n\n    The grid wraps around at the edges, so it behaves like a torus.\n    """')
    r.commit("john", "Wrap the grid edges so it behaves like a torus")

    r.rep("life.py", '    "blinker": {(0, 1), (1, 1), (2, 1)},\n',
          '    "blinker": {(0, 1), (1, 1), (2, 1)},\n    "glider": {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)},\n')
    r.commit("grace", "Add the glider")

    r.rep("life.py", "import argparse\n", "import argparse\nimport time\n")
    r.rep("life.py", MAIN_V1, MAIN_V2)
    r.commit("ada", "Animate the grid in the terminal")

    r.rep("README.md", "Conway's Game of Life in plain Python.\n",
          "Conways Game of Life in plain Python, no dependencies.\n\n## Running it\n\n```bash\npython life.py glider\npython life.py blinker --steps 20\n```\n")
    r.commit("john", "Document how to run the demo in the README")

    r.rep("life.py", MAIN_V2, MAIN_V3)
    r.commit("grace", "Add --width and --height options")

    r.rep("life.py", MAIN_V3, MAIN_V4)
    r.commit("grace", "Add --no-animate to print only the final grid")

    r.rep("life.py", RENDER_V1, RENDER_V1 + '''

def place(pattern, width, height, x0=1, y0=1):
    """Return a copy of the pattern shifted to start at (x0, y0)."""
    return {(x + x0, y + y0) for x, y in pattern}
''')
    r.rep("life.py", "    alive = set(PATTERNS[args.pattern])\n",
          "    alive = place(PATTERNS[args.pattern], args.width, args.height)\n")
    r.commit("ada", GOOD_TAG_AFTER)  # tagged v0.1

    r.rep("life.py", '    "glider": {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)},\n',
          '    "glider": {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)},\n    "toad": {(1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2)},\n')
    r.commit("margaret", "Add the toad oscillator")

    r.rep("life.py", '    "toad": {(1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2)},\n',
          '    "toad": {(1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2)},\n    "beacon": {(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (3, 2), (2, 3), (3, 3)},\n')
    r.commit("margaret", "Add the beacon oscillator")

    r.rep("README.md", "Conways Game of Life", "Conway's Game of Life")
    r.commit("grace", "Fix typo in README")

    r.rep("life.py", '"#" if (x, y) in alive else "."', '"\u2588" if (x, y) in alive else "\u00b7"')
    r.commit("john", "Use block glyphs for live cells")

    r.rep("life.py", '    parser.add_argument("--height", type=int, default=20, help="grid height in cells")\n',
          '    parser.add_argument("--height", type=int, default=20, help="grid height in cells")\n    parser.add_argument("--delay", type=float, default=0.1, help="seconds between frames")\n')
    r.rep("life.py", "            time.sleep(0.1)\n", "            time.sleep(args.delay)\n")
    r.commit("ada", "Add --delay option to control animation speed")

    r.rep("test_life.py", "        self.assertEqual(step(step(blinker, 10, 10), 10, 10), blinker)\n",
          '''        self.assertEqual(step(step(blinker, 10, 10), 10, 10), blinker)

    def test_toad_has_period_two(self):
        toad = PATTERNS["toad"]
        self.assertNotEqual(step(toad, 10, 10), toad)
        self.assertEqual(step(step(toad, 10, 10), 10, 10), toad)

    def test_beacon_has_period_two(self):
        beacon = PATTERNS["beacon"]
        self.assertNotEqual(step(beacon, 10, 10), beacon)
        self.assertEqual(step(step(beacon, 10, 10), 10, 10), beacon)
''')
    r.commit("margaret", "Add tests for the toad and beacon")

    r.add(".github/workflows/test.yml", WORKFLOW_V1)
    r.commit("grace", "Add GitHub Actions workflow to run the tests")

    r.rep("life.py", "import argparse\n", '''"""Conway's Game of Life on a wrapping grid.

Run a named pattern and watch it evolve in the terminal:

    python life.py glider
    python life.py blinker --steps 20 --delay 0.2
"""
import argparse
''')
    r.commit("john", "Add module docstring with usage examples")

    r.rep("life.py", "    for _ in range(args.steps):\n        if not args.no_animate:\n            print(\"\\033[2J\\033[H\" + render(alive, args.width, args.height))\n",
          "    for generation in range(args.steps):\n        if not args.no_animate:\n            print(\"\\033[2J\\033[H\" + render(alive, args.width, args.height))\n            print(f\"generation {generation}\")\n")
    r.rep("life.py", "    if args.no_animate:\n        print(render(alive, args.width, args.height))\n",
          "    if args.no_animate:\n        print(render(alive, args.width, args.height))\n        print(f\"generation {args.steps}\")\n")
    r.commit("ada", "Print the generation number under the grid")

    r.rep("life.py", '    "beacon": {(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (3, 2), (2, 3), (3, 3)},\n',
          '    "beacon": {(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (3, 2), (2, 3), (3, 3)},\n    "lwss": {(1, 0), (4, 0), (0, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3)},\n')
    r.commit("margaret", "Add the lightweight spaceship")


    r.app(".gitignore", ".venv/\n")
    r.commit("john", "Ignore virtual environments")

    r.rep("life.py", '            print(f"generation {generation}")\n', '            print(f"generation {generation}, {len(alive)} alive")\n')
    r.rep("life.py", '        print(f"generation {args.steps}")\n', '        print(f"generation {args.steps}, {len(alive)} alive")\n')
    r.commit("ada", "Show the live cell count under the grid")

    r.rep("life.py", '''    """Return a copy of the pattern shifted to start at (x0, y0)."""
    return {(x + x0, y + y0) for x, y in pattern}
''', '''    """Return a copy of the pattern shifted to start at (x0, y0)."""
    cells = {(x + x0, y + y0) for x, y in pattern}
    if any(x >= width or y >= height for x, y in cells):
        raise ValueError("pattern does not fit in the grid")
    return cells
''')
    r.commit("margaret", "Reject patterns that do not fit in the grid")

    r.rep("life.py", "def step(alive, width, height):", "def step(alive: set[tuple[int, int]], width: int, height: int) -> set[tuple[int, int]]:")
    r.rep("life.py", "def render(alive, width, height):", "def render(alive: set[tuple[int, int]], width: int, height: int) -> str:")
    r.rep("life.py", "def place(pattern, width, height, x0=1, y0=1):", "def place(pattern: set[tuple[int, int]], width: int, height: int, x0: int = 1, y0: int = 1) -> set[tuple[int, int]]:")
    r.commit("grace", "Add type hints to the public functions")

    # ---- the culprit ----------------------------------------------------
    r.rep("life.py", '''def step(alive: set[tuple[int, int]], width: int, height: int) -> set[tuple[int, int]]:''',
          '''def count_neighbours(alive: set[tuple[int, int]], x: int, y: int, width: int, height: int) -> int:
    """Count the live neighbours of (x, y), wrapping at the edges."""
    return sum(((x + dx) % width, (y + dy) % width) in alive for dx, dy in OFFSETS)


def step(alive: set[tuple[int, int]], width: int, height: int) -> set[tuple[int, int]]:''')
    r.rep("life.py", "            n = sum(((x + dx) % width, (y + dy) % height) in alive for dx, dy in OFFSETS)\n",
          "            n = count_neighbours(alive, x, y, width, height)\n")
    assert r.n + 1 == CULPRIT_INDEX
    r.commit("john", CULPRIT_MESSAGE)

    r.rep("life.py", "import argparse\n", "import argparse\nimport random\n")
    r.rep("life.py", '    parser.add_argument("pattern", help="name of the starting pattern")\n',
          '    parser.add_argument("pattern", nargs="?", help="name of the starting pattern")\n    parser.add_argument("--seed", type=int, help="start from a random grid with this seed")\n')
    r.rep("life.py", "    alive = place(PATTERNS[args.pattern], args.width, args.height)\n",
          '''    if args.seed is not None:
        rng = random.Random(args.seed)
        alive = {(x, y) for x in range(args.width) for y in range(args.height) if rng.random() < 0.3}
    elif args.pattern:
        alive = place(PATTERNS[args.pattern], args.width, args.height)
    else:
        parser.error("give a pattern name or --seed")
''')
    r.commit("ada", "Add --seed option to start from a random grid")

    r.rep("life.py", '    "lwss": {(1, 0), (4, 0), (0, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3)},\n',
          '    "lwss": {(1, 0), (4, 0), (0, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3)},\n'
          '    "pulsar": {\n' + "".join("        " + ", ".join(map(str, PULSAR[i:i + 6])) + ",\n" for i in range(0, len(PULSAR), 6)) + '    },\n')
    r.commit("margaret", "Add the pulsar")

    r.rep("life.py", "import argparse\n", "import argparse\nimport os\n")
    r.rep("life.py", "import time\n", "import time\n\nCLEAR = \"cls\" if os.name == \"nt\" else \"clear\"\n")
    r.rep("life.py", '            print("\\033[2J\\033[H" + render(alive, args.width, args.height))\n',
          '            os.system(CLEAR)\n            print(render(alive, args.width, args.height))\n')
    r.commit("grace", "Clear the terminal portably on Windows")

    r.rep("test_life.py", "class OscillatorTests(unittest.TestCase):",
          '''class EmptyGridTests(unittest.TestCase):
    def test_empty_grid_stays_empty(self):
        self.assertEqual(step(set(), 10, 10), set())


class OscillatorTests(unittest.TestCase):''')
    r.commit("john", "Add a test that the empty grid stays empty")

    r.rep("life.py", '    parser.add_argument("pattern", nargs="?", help="name of the starting pattern")\n',
          '    parser.add_argument("pattern", nargs="?", choices=sorted(PATTERNS), help="name of the starting pattern")\n')
    r.commit("ada", "Validate the pattern name with argparse choices")

    r.app("README.md", "\n## Contributing\n\nOpen an issue or a pull request. Keep commits small, one change each, with a\nmessage that says why. Run the tests before you push.\n")
    r.commit("margaret", "Add a contributing section to the README")

    r.rep("life.py", '''

if __name__ == "__main__":
    main()
''', '''

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
''')
    r.commit("grace", "Exit quietly on Ctrl-C during animation")

    r.rep("life.py", '    parser.add_argument("--seed", type=int, help="start from a random grid with this seed")\n',
          '    parser.add_argument("--seed", type=int, help="start from a random grid with this seed")\n    parser.add_argument("--list", action="store_true", help="list the available patterns and exit")\n')
    r.rep("life.py", "    if args.seed is not None:\n",
          "    if args.list:\n        print(\"\\n\".join(sorted(PATTERNS)))\n        return\n    if args.seed is not None:\n")
    r.commit("john", "Add --list to show the available patterns")

    # sort the pattern table alphabetically
    text = r.files["life.py"]
    start = text.index("PATTERNS = {\n") + len("PATTERNS = {\n")
    end = text.index("\n}\n", start)
    body = text[start:end]
    entries, cur = [], []
    for line in body.split("\n"):
        cur.append(line)
        if line.startswith("    }") or (line.startswith("    \"") and line.rstrip().endswith("},")):
            entries.append("\n".join(cur)); cur = []
    assert not cur, cur
    entries.sort(key=lambda e: e.strip().split('"')[1])
    r.files["life.py"] = text[:start] + "\n".join(entries) + text[end:]
    r.commit("ada", "Sort the pattern table alphabetically")

    r.add("LICENSE", LICENSE)
    r.commit("margaret", "Add MIT licence")

    r.rep(".github/workflows/test.yml", 'python-version: "3.x"', 'python-version: "3.12"')
    r.commit("grace", "Pin the Python version in CI")

    r.files["README.md"] = README_FINAL
    r.commit(None, "Add workshop instructions to the README")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    root = Path(sys.argv[1]).resolve()
    if root.exists():
        sys.exit(f"{root} already exists, refusing to overwrite")
    root.mkdir(parents=True)
    repo = Repo(root)
    repo.git("init", "-q", "-b", "main")
    build(repo)
    print(f"\n{repo.n} commits in {root}")
    print(repo.git("log", "--oneline", "--decorate", "-5"))
    print("culprit:", repo.git("log", "--format=%h %s", "--grep", CULPRIT_MESSAGE).strip())


if __name__ == "__main__":
    main()
