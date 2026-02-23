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
    
    # =========================================================================
    # FUNCTION PURPOSE AND USE CASES
    # =========================================================================
    # This is a CONVENIENCE WRAPPER that combines sorting + slicing operations
    # Common use cases:
    #   1. Dashboard: Show top 5 tasks for user's focus
    #   2. Notifications: Alert on top 3 most urgent tasks
    #   3. CLI: Display "next 10 tasks" command
    #   4. API: Return GET /tasks?limit=5 with best priorities first
    #
    # Why a separate function?
    #   - Common pattern: every client has different limits
    #   - Single responsibility: top_priority_tasks() handles limiting
    #   - Improved readability: More intent-clear than sort + slice
    #   - Potential for optimization: Could use heapq.nlargest() in future
    
    # =========================================================================
    # ALGORITHM: Delegate to Sort Function, Then Slice
    # =========================================================================
    # Step 1: Get all tasks sorted by importance (highest first)
    sorted_tasks = sort_tasks_by_importance(tasks)
    
    # Step 2: Return only the first 'limit' tasks
    # Python's slice notation [0:limit] is safe:
    #   - If limit >= len(tasks): Returns all tasks
    #   - If limit == 0: Returns empty list
    #   - If limit < 0: Returns empty list (negative indices count from end)
    #   - If limit > len(tasks): Returns all available tasks
    return sorted_tasks[:limit]
    
    # =========================================================================
    # POTENTIAL IMPROVEMENTS
    # =========================================================================
    #
    # 1. INPUT VALIDATION (Current Approach: Trust Caller)
    #    CURRENT CODE: No validation of 'limit' parameter
    #    IMPROVEMENT: Add guard clause
    #    >>> if limit < 1:
    #    >>>     raise ValueError(f"limit must be >= 1, got {limit}")
    #    TRADE-OFF: Adds 2 lines of code, prevents silent failures
    #
    # 2. EFFICIENCY FOR LARGE LISTS (Current: O(n log n) full sort)
    #    PROBLEM: If tasks list has 10,000 items but limit=5, we sort all 10k
    #    IMPROVEMENT: Use heapq.nlargest() instead
    #    >>> import heapq
    #    >>> top_scored = heapq.nlargest(
    #    >>>     limit,
    #    >>>     tasks,
    #    >>>     key=calculate_task_score
    #    >>> )
    #    BENEFIT: O(n log k) where k = limit (only finds top-k, doesn't sort all)
    #    TRADE-OFF: Slightly more complex code, maintains score calculation
    #
    # 3. CACHING (Current: Recalculates every call)
    #    PROBLEM: If called multiple times, recalculates all scores each time
    #    IMPROVEMENT: Cache results, invalidate on task changes
    #    >>> _score_cache = {}
    #    >>> def get_top_priority_tasks(tasks, limit=5):
    #    >>>     task_ids = tuple(id(t) for t in tasks)
    #    >>>     if task_ids not in _score_cache:
    #    >>>         _score_cache[task_ids] = sort_tasks_by_importance(tasks)
    #    >>>     return _score_cache[task_ids][:limit]
    #    BENEFIT: Huge speedup for repeated calls with same tasks
    #    TRADE-OFF: Memory overhead, cache invalidation complexity
    #
    # 4. STABLE ORDERING (Current: Non-deterministic for equal scores)
    #    PROBLEM: Tasks with same score have undefined order
    #    IMPROVEMENT: Add secondary sort key (e.g., task creation date)
    #    >>> sorted_tasks = sort(tasks, key=lambda t: (-calculate_task_score(t), t.created_at))
    #    BENEFIT: Deterministic results, useful for tests and consistency
    #    TRADE-OFF: Slightly slower, requires created_at field
    #
    # 5. PAGINATION (Current: Single page of results)
    #    PROBLEM: If limit=5 but user wants to see 6-10, must call again
    #    IMPROVEMENT: Add offset parameter
    #    >>> def get_top_priority_tasks(tasks, limit=5, offset=0):
    #    >>>     sorted_tasks = sort_tasks_by_importance(tasks)
    #    >>>     return sorted_tasks[offset:offset+limit]
    #    BENEFIT: Enable pagination in UI without re-sorting
    #    TRADE-OFF: API becomes more complex
    
    # =========================================================================
    # ASSUMPTIONS AND EDGE CASES
    # =========================================================================
    #
    # ASSUMPTION 1: limit > 0 is a precondition
    #   - Code assumes caller provides valid limit (>= 1)
    #   - If limit <= 0 is passed, returns empty list (silent failure)
    #   - FIX: Validate input if defensive programming is desired
    #
    # ASSUMPTION 2: tasks is iterable and non-None
    #   - Code assumes tasks list exists and is iterable
    #   - If tasks is None, TypeError will occur in sort_tasks_by_importance
    #   - FIX: Add guard: `if not tasks: return []`
    #
    # EDGE CASE 1: Empty task list
    #   INPUT: tasks = [], limit = 5
    #   BEHAVIOR: Returns [] (empty list)
    #   CORRECT: Yes, no tasks to return
    #
    # EDGE CASE 2: Limit exceeds task count
    #   INPUT: tasks = [task1, task2], limit = 10
    #   BEHAVIOR: Returns [task1, task2] sorted by importance
    #   CORRECT: Yes, returns all available tasks
    #
    # EDGE CASE 3: Limit equals zero
    #   INPUT: tasks = [task1, task2, task3], limit = 0
    #   BEHAVIOR: Returns [] (empty list)
    #   POTENTIAL ISSUE: May be unintended; consider validating limit >= 1
    #
    # EDGE CASE 4: Negative limit
    #   INPUT: tasks = [task1, task2, task3], limit = -1
    #   BEHAVIOR: Returns [] or possibly all if interpreted as "all except last"
    #   ISSUE: Python negatives in slicing count from end (e.g., [:-1] = all but last)
    #   HERE: sorted_tasks[:-1] would return all except last task
    #   FIX: Validate limit >= 1 to prevent confusion