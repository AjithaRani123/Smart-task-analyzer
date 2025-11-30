from datetime import date, datetime


# Safe extraction with defaults
importance = int(task_data.get('importance') or DEFAULT_IMPORTANCE)
est_hours = int(task_data.get('estimated_hours') or 1)
dependencies = task_data.get('dependencies') or []
due = parse_date(task_data.get('due_date'))


# 1) Urgency
if due is None:
explanation.append('No due date — treated as low urgency')
else:
days_until = (due - today).days
if days_until < 0:
score += weights['urgency_overdue']
explanation.append(f'OVERDUE by {-days_until} day(s)')
elif days_until <= 3:
score += weights['urgency_soon']
explanation.append(f'Due in {days_until} day(s) — very soon')
else:
# Add a small linear urgency factor
urgency_factor = max(0, 30 - days_until) # fades with time
score += urgency_factor
explanation.append(f'Due in {days_until} day(s) — moderate urgency')


# 2) Importance
score += importance * weights['importance']
explanation.append(f'Importance {importance} adds {importance * weights["importance"]} points')


# 3) Effort (quick wins)
if est_hours <= weights['effort_bonus_hours']:
score += weights['effort_small_bonus']
explanation.append(f'Quick task ({est_hours}h) bonus +{weights["effort_small_bonus"]}')
else:
# penalize very large tasks slightly to prefer smaller wins when similar score
penalty = min(20, (est_hours - weights['effort_bonus_hours']))
score -= penalty
explanation.append(f'Large task penalty -{penalty}')


# 4) Dependencies
# If other tasks depend on this task (i.e., it's a blocker) we expect the caller to pass info.
# Here we treat length of dependencies as indicator that task *depends on others* (not a blocker).
# But if the task has a special flag 'is_blocker' treat it as blocking.
if task_data.get('is_blocker'):
score += weights['dependency_block_bonus']
explanation.append('Marked as blocker for other tasks')


# If dependencies is non-empty and unresolved, increase priority for unblock? We'll slightly boost
if dependencies:
score += 5
explanation.append(f'Has {len(dependencies)} dependency(ies) — +5')


# Final normalization: ensure score is not negative
final_score = max(0, int(score))


return final_score, explanation