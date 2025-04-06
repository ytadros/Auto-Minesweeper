## 🚧 Project Under Active Refactor (April 2025)

This project is currently undergoing a major refactor to improve structure, maintainability, and performance. Over the coming weeks, expect the following:

### 🔧 In Progress:
- Separating game logic from the Tkinter GUI (moving toward MVC pattern)
- Improving code structure to follow SOLID principles
- Replacing list-based queues with `collections.deque`
- Implementing unit tests and setting up CI via GitHub Actions

### 🛣️ Planned (Later Stages):
- Performance profiling using `cProfile` and `py-call-graph`
- Improved UI/UX and potential for headless/batch play
- Optional logging and configurable game settings (via JSON/YAML)
- Possible probability-based move logic in solver

### 📅 Rough Timeline:
| Week of | Focus |
|---|---|
| April 7–14 | Code structure refactor, unit test setup |
| April 15–21 | Profiling + performance optimizations |
| April 22–30 | Logging, config cleanup, optional features |

<p style="color:red; font-weight:bold;"> ⚠️ Recruiters/Reviewers: This repo reflects ongoing improvements! Please check commit history and PRs for recent progress.

---
---

# Auto-Minesweeper
My first Python project

This is my first ever object oriented project.
I used Python and tkinter.

This is a minesweeper game with the capacity to solve itself where possible.

There are options to highlight and showcase certain process executions, visualizing the solving process.

There are also options to change the solving style.
(Try starting a new game with percent_mined set to 0, then try out all the different
  process directions -- make sure the "to_clear" checkbox is checked in the "Display Processes" Panel)
