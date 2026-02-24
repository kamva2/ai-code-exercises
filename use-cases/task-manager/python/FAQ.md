# FAQ — Task Manager (Python)

This FAQ is for:
- **Non-programmer users** who want to manage tasks from the command line.
- **Junior developers** on the team who need to understand core use-case features and common support issues.

---

## 1) Getting Started

### Q1: What is this application used for?
**A:** It is a todo/task management tool. You can create tasks, assign priority, set due dates, add tags, and track task status from start to completion.

### Q2: Who should use this tool?
**A:** Anyone in the team who needs a simple way to organize work. Non-programmers can follow copy/paste commands. Developers can also extend the logic in `app.py`, `cli.py`, and `storage.py`.

### Q3: What do I need before I can use it?
**A:** You need Python installed, terminal access, and access to the project folder `use-cases/task-manager/python`.

### Q4: How do I verify the program is ready?
**A:** Run the help command:
```bash
python -m task_manager.cli --help
```
If help text appears, the CLI is available.

### Q5: What is the quickest way to add my first task?
**A:** Run:
```bash
python -m task_manager.cli create "My first task"
```
Then confirm with:
```bash
python -m task_manager.cli list
```

---

## 2) Common Features & Functionality

### Q6: How do I create a detailed task?
**A:** Use title + optional description, priority, due date, and tags:
```bash
python -m task_manager.cli create "Finish sprint report" -d "Prepare and submit report" -p 3 -u 2026-03-01 -t work,reporting
```

### Q7: What do priority numbers mean?
**A:** Priority accepts values `1` to `4` (from lower to higher urgency based on project defaults).

### Q8: How do I see only specific tasks?
**A:** Use filters:
- By status:
```bash
python -m task_manager.cli list -s todo
```
- By priority:
```bash
python -m task_manager.cli list -p 4
```
- Overdue only:
```bash
python -m task_manager.cli list -o
```

### Q9: How do I change a task’s status?
**A:** Use:
```bash
python -m task_manager.cli status <task_id> done
```
Valid statuses are `todo`, `in_progress`, `review`, `done`.

### Q10: How do I add or remove tags?
**A:**
```bash
python -m task_manager.cli tag <task_id> urgent
python -m task_manager.cli untag <task_id> urgent
```

### Q11: How do I view one task in detail?
**A:**
```bash
python -m task_manager.cli show <task_id>
```

### Q12: How do I remove a task I no longer need?
**A:**
```bash
python -m task_manager.cli delete <task_id>
```

### Q13: Can I see dashboard-like progress quickly?
**A:** Yes. Use:
```bash
python -m task_manager.cli stats
```
This shows totals, counts by status, counts by priority, overdue tasks, and recent completions.

---

## 3) Troubleshooting Common Issues

### Q14: I get `No module named task_manager`. What should I do?
**A:** You are likely running commands from the wrong directory or package context.

Try:
1. Move into the project directory.
2. Re-run:
```bash
python -m task_manager.cli --help
```

### Q15: Why do I get `Invalid date format. Use YYYY-MM-DD`?
**A:** Due dates must use this exact format: `YYYY-MM-DD` (example: `2026-03-01`).

### Q16: Why does update/delete fail with `Task not found`?
**A:** The task ID is incorrect, outdated, or copied incompletely.

Fix:
1. Run `list`.
2. Copy the exact task ID.
3. Retry the command.

### Q17: Why are my tasks missing after restart?
**A:** Most often, commands were run from a different working directory, so a different `tasks.json` file is being used.

Fix:
- Use one consistent working directory.
- Check where `tasks.json` was created.

### Q18: Why does nothing happen when I run a command?
**A:** Possible causes:
- Typo in command or option.
- Missing required argument.
- Environment not activated.

Fix:
```bash
python -m task_manager.cli --help
```
Then rerun with valid arguments.

---

## 4) Specific Area of Interest: Use-Case Features

### Q19: Which feature should non-programmers start with first?
**A:** Start with four commands: `create`, `list`, `status`, and `stats`. This covers most daily usage.

### Q20: What is the recommended team workflow for tasks?
**A:** A simple flow is:
1. `create` task with title, due date, and tags.
2. Move status: `todo` → `in_progress` → `review` → `done`.
3. Check `list` and `stats` daily.

### Q21: How should we use tags effectively?
**A:** Use short, consistent tags by category, e.g., `bug`, `feature`, `docs`, `urgent`. Avoid many near-duplicate tags.

### Q22: How should juniors debug command behavior?
**A:** Start with CLI output, then trace command handling in `cli.py`, business logic in `app.py`, and persistence in `storage.py`.

### Q23: Is this tool multi-user by default?
**A:** Not by default. It stores tasks in a local file (`tasks.json`) for a local workflow unless extended.

---

## Generated Known Issues / Frequently Asked Team Questions

### Q24: “I created tasks, but my teammate cannot see them.”
**A:** The current setup is local-file based. Share/export task data or implement shared storage if team-wide visibility is required.

### Q25: “I used spaces in tags and got unexpected results.”
**A:** Tags are comma-separated values. Use `-t work,backend,urgent`.

### Q26: “Priority values are confusing for users.”
**A:** Add a team convention in docs (for example: `1=Low`, `2=Medium`, `3=High`, `4=Urgent`) and train users to follow it.

### Q27: “Can we automate recurring task creation?”
**A:** Not currently built-in. This can be added by extending `TaskManager` in `app.py`.

### Q28: “How do we prevent accidental deletes?”
**A:** Current delete executes immediately. A confirmation prompt can be added in `cli.py` as a future enhancement.

---

## Quick Command Cheat Sheet

```bash
python -m task_manager.cli --help
python -m task_manager.cli create "Write meeting notes" -d "Summarize weekly sync" -p 2 -u 2026-03-05 -t docs,team
python -m task_manager.cli list
python -m task_manager.cli status <task_id> in_progress
python -m task_manager.cli status <task_id> done
python -m task_manager.cli stats
```
