## 🚧 Project Mid-Refactor — Logic Engine Already Functional

This project is in the middle of a major refactor focused on modularity, performance, and code quality. But the core logic engine is already working — and it's worth exploring. The solver plays Minesweeper step-by-step using deductive logic, visually revealing how each conclusion is reached. It's more than a game; it's a testbed for reasoning systems and interactive problem-solving.

### ✅ What's Already Done:

- Built a functioning logic engine that visualizes deductions in real time  
- Implemented customizable board generation and manual mine placement  
- Enabled user control over solver behavior (FIFO, LIFO, directional priorities, random, etc.)  

### 🔧 Currently Working On:

- Planning full decoupling of GUI from game logic (toward MVC structure)  
- Evaluating migration from list-based queues to `collections.deque`  
- Adding unit tests with Python’s `unittest` framework  
- Refactoring modules for clearer separation of concerns  

### 🛣️ Upcoming (Q2 2025):

- Profiling and performance tuning (`cProfile`, `py-call-graph`)  
- Optional logging and configuration via JSON/YAML  
- UI/UX improvements and exploration of headless/batch-play modes  
- (Stretch) Probability-based fallback logic for ambiguous states  

> 🧠 **Note for Reviewers & Recruiters**: While the refactor is ongoing, the existing repo already demonstrates working logic, thoughtful design goals, and visual introspection tools. Check commit history and PRs to follow progress.

---

# Auto-Minesweeper

I built this project out of a love for Minesweeper and a fascination with how logic can be made visible. It's fully playable, but the real focus is the solver: a visual engine that steps through its reasoning in public. You can watch how it makes deductions, how it handles ambiguity, and you can tweak aspects of its internal logic as it runs.

Want to test a new rule? Try a different queueing strategy? Create an edge-case board with mines placed manually before the first click? This is the playground.

![Solver Visualization](https://github.com/user-attachments/assets/72be0ec7-9531-4c12-8c2b-a243bd46f969)  
*The solver highlighting tiles as it deduces safe moves using rule-based logic.*

![Custom Mine Placement](https://github.com/user-attachments/assets/d1809a5c-b2b2-4b12-bee3-7cd2957f3850)  
*Manual mine placement before first move — useful for testing or experimentation.*

![Logic Engine Solving custom board, Direction: E](https://github.com/user-attachments/assets/37c7b527-0d01-4750-b1f5-983ba103222f)  
*Same board in action: visual reasoning on a custom setup with directional logic control.*

Whether you're into logic, Python design patterns, or just weirdly obsessed with Minesweeper like I am—you're welcome to explore, break things, and build smarter solvers.

> ⚙️ *Note:* This was my first serious attempt at designing a structured OOP project from scratch. Since then, I’ve matured a lot as an engineer — and that’s part of what this refactor is about. Revisiting old code with new eyes has been its own kind of fun.

---
