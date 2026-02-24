# Step-by-Step Guide: Add a Task (Beginner)

This guide explains exactly how to add a task in the Task Manager Python application using CLI commands.

## Prerequisites / Required Access
Before you begin, make sure you have:

1. Access to the project folder:
   - `use-cases/task-manager/python`
2. Python 3.11 or newer installed.
3. Basic terminal access (PowerShell, Command Prompt, or terminal in VS Code).
4. Permission to run local Python commands on your machine.

Optional but recommended:

```bash
python -m venv .venv
.venv\Scripts\activate
```

[Placeholder: Screenshot of terminal opened in the `use-cases/task-manager/python` directory]

---

## Step-by-Step: How to Add a Task

### 1) Open a terminal in the project folder
Navigate to the Python task-manager folder:

```bash
cd use-cases/task-manager/python
```

[Placeholder: Screenshot showing terminal path after `cd`]

---

### 2) Verify the CLI command is available
Run help to confirm command usage:

```bash
python -m task_manager.cli --help
```

Expected result:
- Help output listing commands like `create`, `list`, `status`, `priority`, `due`, etc.

[Placeholder: Screenshot of help output]

---

### 3) Add a new task (basic)
Use the `create` command with at least a title:

```bash
python -m task_manager.cli create "Buy groceries"
```

Expected result:
- Output similar to: `Created task with ID: <task_id>`

[Placeholder: Screenshot of successful task creation output]

---

### 4) Add a new task (full example)
Use optional fields for better task details:

```bash
python -m task_manager.cli create "Finish sprint report" -d "Prepare and submit report" -p 3 -u 2026-03-01 -t work,reporting
```

What each option means:
- `-d` / `--description`: task description
- `-p` / `--priority`: priority value (`1` to `4`)
- `-u` / `--due`: due date (`YYYY-MM-DD`)
- `-t` / `--tags`: comma-separated tags

---

### 5) Confirm your task was added
List tasks:

```bash
python -m task_manager.cli list
```

Expected result:
- Your new task appears in the list with ID, title, status, priority, due date, and tags.

[Placeholder: Screenshot of task list including new task]

---

## Common Mistakes to Avoid

1. **Wrong date format**
   - Mistake: using `03/01/2026` or `2026/03/01`
   - Correct format: `YYYY-MM-DD` (example: `2026-03-01`)

2. **Invalid priority value**
   - Mistake: using values outside `1`–`4` (for example `0` or `5`)
   - Use only: `1`, `2`, `3`, or `4`

3. **Running commands from the wrong folder**
   - If Python cannot resolve modules, move to the project path first:

```bash
cd use-cases/task-manager/python
```

4. **Forgetting quotes around multi-word titles**
   - Wrong: `create Finish sprint report`
   - Correct: `create "Finish sprint report"`

5. **Using spaces in tags instead of commas**
   - Recommended: `-t work,reporting,urgent`

---

## Troubleshooting (Common Problems)

### Problem: `No module named task_manager`
Possible causes:
- You are not running the command from the correct location.
- Your local package structure is different from the expected module path.

Try:
1. Navigate to the project folder.
2. Re-run:

```bash
python -m task_manager.cli --help
```

3. If still failing, run via direct script path if your structure is flat.

---

### Problem: `Invalid date format. Use YYYY-MM-DD`
Cause:
- Due date is in the wrong format.

Try:
- Use a date like `2026-03-01`.

---

### Problem: Task created but does not appear in list
Possible causes:
- Different working directory from where `tasks.json` is stored.
- Running command in another environment/folder.

Try:
1. Run all commands from the same folder.
2. Check whether `tasks.json` exists in your current directory.
3. Re-run:

```bash
python -m task_manager.cli list
```

---

### Problem: Command output is unclear
Try:

```bash
python -m task_manager.cli --help
```

Then review command syntax and required arguments.

---

## Quick Copy/Paste Command Set

```bash
cd use-cases/task-manager/python
python -m task_manager.cli --help
python -m task_manager.cli create "Buy groceries"
python -m task_manager.cli create "Finish sprint report" -d "Prepare and submit report" -p 3 -u 2026-03-01 -t work,reporting
python -m task_manager.cli list
```

[Placeholder: Final screenshot showing full successful flow]
