# task-manager python

A Python-based todo list application for creating, tracking, and managing tasks from the command line.

## Description
`task-manager python` is a lightweight task management project designed to help developers organize work items using simple CLI commands. It supports task creation, status updates, priorities, due dates, tags, and basic reporting.

## Features Overview
- User command-driven workflow via CLI subcommands
- Create tasks with title, description, priority, due date, and tags
- List tasks with filters (status, priority, overdue)
- Update task status, priority, and due date
- Add/remove task tags
- Show task details and delete tasks
- View summary statistics for task tracking

## Technologies Used
- Python

## Installation

### Requirements
- Python 3.11+ recommended
- Basic Python coding skills

### Setup
1. Clone or download this repository.
2. Open a terminal in this directory:
   - `use-cases/task-manager/python`
3. (Optional but recommended) Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

4. Run the CLI module from the project root (see usage examples below).

## Basic Usage Examples

### Show help
```bash
python -m task_manager.cli --help
```

### Create a task
```bash
python -m task_manager.cli create "Finish README" -d "Add project docs" -p 2 -u 2026-03-01 -t docs,writing
```

### List all tasks
```bash
python -m task_manager.cli list
```

### Filter tasks by status
```bash
python -m task_manager.cli list -s todo
```

### Update task status
```bash
python -m task_manager.cli status <task_id> done
```

### Update task priority
```bash
python -m task_manager.cli priority <task_id> 4
```

### Show statistics
```bash
python -m task_manager.cli stats
```

## Configuration Options

The application is intentionally minimal. Current configuration behavior:

- **Storage file path**
  - Default task storage file is `tasks.json`.
  - In code, this is controlled by `TaskManager(storage_path="tasks.json")` in `app.py`.
  - To use a different file, instantiate `TaskManager` with another path in your own script.

- **Date format**
  - Due dates must be provided as `YYYY-MM-DD`.

- **Priority values**
  - Priority supports integer values `1` to `4`.

- **Status values**
  - Valid statuses are: `todo`, `in_progress`, `review`, `done`.

## Code Structure Overview
Primary entry point provided:

- `app.py` — core task manager logic and operations

Related modules used by the project:

- `cli.py` — command-line interface and command routing
- `models.py` — task model, status, and priority definitions
- `storage.py` — persistence operations for tasks

## Troubleshooting

### `No module named task_manager`
Cause: running commands from the wrong directory or package path mismatch.

Fix:
- Run commands from the correct project root where the package is resolvable.
- Alternatively execute a script directly if your local structure differs.

### Date validation errors
Message: `Invalid date format. Use YYYY-MM-DD`

Fix:
- Ensure due dates use exact format: `2026-03-01`

### Task updates fail (`Task not found`)
Cause: incorrect `task_id`.

Fix:
- Run `list` first and copy the exact task id before update/delete operations.

### No tasks appear
Cause: empty storage file or wrong storage path.

Fix:
- Check whether `tasks.json` exists in your working directory.
- Confirm your runtime working directory matches where tasks were created.

## Contributing Guidelines

Contributions are welcome. Suggested process:

1. Fork the repository and create a feature branch.
2. Keep changes focused and small.
3. Follow existing code style and naming patterns.
4. Add or update documentation for behavior changes.
5. Test CLI commands manually for affected features.
6. Open a pull request with a clear summary of changes.

## License

No license file is currently specified in this project folder.

If this project is intended for public or shared team use, add a `LICENSE` file at the repository root (for example, MIT, Apache-2.0, or proprietary internal license) and update this section accordingly.
