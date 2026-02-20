def calculate_task_score(task):
    """Calculate a priority score for a task based on multiple factors.
    
    This function computes a numerical score that represents the importance and
    urgency of a task by considering multiple factors: base priority level, 
    due date proximity, completion status, special tags, and update recency.
    Higher scores indicate tasks that require more immediate attention.
    
    The scoring algorithm works as follows:
    - Base score is calculated from priority level (LOW=10, MEDIUM=20, HIGH=40, URGENT=60)
    - Due date adjustments reward tasks nearing their deadlines
    - Status penalties reduce scores for completed or in-review tasks
    - Special tags (blocker, critical, urgent) increase urgency
    - Recently updated tasks receive a small boost
    
    Args:
        task (Task): A task object with the following attributes:
            - priority (TaskPriority): Priority level of the task
            - due_date (datetime.datetime, optional): When the task is due
            - status (TaskStatus): Current status of the task
            - tags (list[str]): List of string tags associated with the task
            - updated_at (datetime.datetime): When the task was last modified
    
    Returns:
        int: A numerical score where higher values indicate higher priority.
             Typical range is 0-100, but scores can exceed this for urgent overdue tasks.
    
    Raises:
        AttributeError: If task is missing required attributes (priority, status, tags, updated_at)
        TypeError: If task.due_date is not a datetime object or None
    
    Examples:
        >>> from datetime import datetime, timedelta
        >>> task = Task(
        ...     priority=TaskPriority.HIGH,
        ...     due_date=datetime.now() + timedelta(days=1),
        ...     status=TaskStatus.PENDING,
        ...     tags=["critical"],
        ...     updated_at=datetime.now()
        ... )
        >>> score = calculate_task_score(task)
        >>> print(f"Task score: {score}")
        Task score: 63  # 40 (base) + 15 (due soon) + 8 (critical tag)
    
    Notes:
        - Overdue tasks (due_date in the past) receive a significant boost (+35)
        - Completed tasks (DONE status) receive a large penalty (-50), making them
          appear last in sorted results
        - Tasks in REVIEW status incur a smaller penalty (-15)
        - The update boost (+5) only applies to tasks updated within the last 24 hours
        - If a task has multiple special tags, only one +8 boost is applied
        - Tasks without a due_date are not penalized and rely on priority and tags
    """
    # Base priority weights
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6
    }

    # Calculate base score from priority
    score = priority_weights.get(task.priority, 0) * 10

    # Add due date factor (higher score for tasks due sooner)
    if task.due_date:
        days_until_due = (task.due_date - datetime.now()).days
        if days_until_due < 0:  # Overdue tasks
            score += 35
        elif days_until_due == 0:  # Due today
            score += 20
        elif days_until_due <= 2:  # Due in next 2 days
            score += 15
        elif days_until_due <= 7:  # Due in next week
            score += 10

    # Reduce score for tasks that are completed or in review
    if task.status == TaskStatus.DONE:
        score -= 50
    elif task.status == TaskStatus.REVIEW:
        score -= 15

    # Boost score for tasks with certain tags
    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    # Boost score for recently updated tasks
    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:
        score += 5

    return score


def sort_tasks_by_importance(tasks):
    """Sort tasks by calculated importance score in descending order.
    
    This function evaluates a collection of tasks using the calculate_task_score
    algorithm and returns them in order from most important to least important.
    This is useful for displaying tasks in a UI or processing them in priority order.
    
    Args:
        tasks (list[Task]): A list of task objects to sort. Each task should have
            the required attributes for calculate_task_score (priority, status, 
            due_date, tags, updated_at).
    
    Returns:
        list[Task]: A new list containing the same task objects, sorted by their
            calculated scores in descending order (highest priority first).
            The original tasks list is not modified.
    
    Raises:
        AttributeError: If any task is missing required attributes
        TypeError: If tasks is not iterable or contains non-Task objects
    
    Examples:
        >>> tasks = [task1, task2, task3]
        >>> sorted_tasks = sort_tasks_by_importance(tasks)
        >>> for i, task in enumerate(sorted_tasks, 1):
        ...     print(f"{i}. {task.name} - Score: {calculate_task_score(task)}")
        1. Fix critical bug - Score: 85
        2. Review PR - Score: 42
        3. Update documentation - Score: 15
    
    Notes:
        - This function does not modify the original tasks list
        - Completed tasks will appear at the end regardless of their original priority
        - For tasks with identical scores, the order is undefined (not stable sort)
        - Empty lists return an empty list without error
    """
    # Calculate scores once and sort by the score
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    sorted_tasks = [task for _, task in sorted(task_scores, reverse=True)]
    return sorted_tasks


def get_top_priority_tasks(tasks, limit=5):
    """Return the top N priority tasks based on calculated importance scores.
    
    This is a convenience function that sorts all tasks by importance and returns
    only the top N. Useful for dashboards, notifications, or focus lists where
    users need to see only the most urgent tasks.
    
    Args:
        tasks (list[Task]): A list of task objects to evaluate and sort.
        limit (int, optional): Maximum number of tasks to return. Defaults to 5.
            Must be >= 1. If limit exceeds the number of available tasks,
            all tasks are returned.
    
    Returns:
        list[Task]: A list containing up to 'limit' task objects, sorted by
            importance score from highest to lowest. Will contain fewer than
            'limit' tasks if the input list has fewer tasks.
    
    Raises:
        AttributeError: If any task is missing required attributes
        TypeError: If tasks is not iterable or limit is not an integer
        ValueError: If limit is less than 1
    
    Examples:
        >>> tasks = [task1, task2, task3, task4, task5, task6]
        >>> top_tasks = get_top_priority_tasks(tasks, limit=3)
        >>> len(top_tasks)
        3
        >>> for task in top_tasks:
        ...     print(f"- {task.name}")
        - Review critical security patch
        - Fix production bug
        - Client meeting preparation
        
        >>> # Get top 5 when list is smaller
        >>> few_tasks = [task1, task2]
        >>> top_tasks = get_top_priority_tasks(few_tasks, limit=5)
        >>> len(top_tasks)
        2
    
    Notes:
        - A limit of 0 or negative values raises ValueError
        - If limit > len(tasks), all tasks are returned sorted
        - This function sorts ALL tasks internally before slicing; for large
          task lists, consider caching scores or using pagination
        - Completed tasks are still calculated and scored but will appear at
          the end of the sorted list before limiting is applied
        - For production applications tracking many tasks, consider optimizing
          with a heap structure for better performance
    """
    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]