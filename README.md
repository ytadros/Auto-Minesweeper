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

<br/><br/>
> ### ⚠️ Recruiters/Reviewers: This repo reflects ongoing improvements! Please check commit history and PRs for recent progress.
<br/>

---

<br/>

# Auto-Minesweeper

This project began with my love for Minesweeper and my deep fascination—shaped in part by being autistic—with patterns, logic, and visualizing how things work under the hood. While you can absolutely use this like a normal Minesweeper game, the real heart of it is the logic engine: a solver that reasons through each move, displays its thought process visually, and lets me tinker with that process in real time. I wanted to build something where I could see the logic unfold—one step at a time—and explore how small changes in the engine affect outcomes on the board.

The screenshots below show the logic engine in action, visualizing its deductions and choices as it solves the game. The interface is designed to give me full control over game generation, including manually placing mines before the first move (which triggers actual mine placement). You can even adjust how the logic engine processes its reasoning—FIFO, LIFO, directional priorities, or even random—through the direction panel. For me, it’s not just a game; it’s a playground for experimenting with logic and watching it come to life.

![Logic Engine At Work](https://github.com/user-attachments/assets/72be0ec7-9531-4c12-8c2b-a243bd46f969)
![Custom Mine Placement](https://github.com/user-attachments/assets/d1809a5c-b2b2-4b12-bee3-7cd2957f3850)
![Logic Engine Solving custom board, Direction: E](https://github.com/user-attachments/assets/37c7b527-0d01-4750-b1f5-983ba103222f)
