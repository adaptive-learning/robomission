def has_attempted(student, task):
    return any(ts.task == task for ts in student.task_sessions.all())


def has_solved(student, task):
    return any(ts.solved for ts in student.task_sessions.all() if ts.task == task)


def get_time(student, task):
    """Return the best time from solved sessions, or last time if not solved.
    """
    task_sessions = [ts for ts in student.task_sessions.all() if ts.task == task]
    if not task_sessions:
        return None
    solved_sessions = [ts for ts in task_sessions if ts.solved]
    if solved_sessions:
        times = [ts.time_spent for ts in solved_sessions]
        return min(times)
    last_task_session = max(task_sessions, key=lambda ts: ts.end)
    return last_task_session.time_spent
