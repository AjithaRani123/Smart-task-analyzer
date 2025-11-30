import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .scoring import calculate_task_score




@csrf_exempt
def analyze_tasks(request):
"""POST: accepts JSON array of tasks and returns them with scores sorted desc"""
if request.method != 'POST':
return HttpResponseBadRequest('Only POST allowed')


try:
body = json.loads(request.body.decode('utf-8'))
# Accept both dict {"tasks": [...]} or raw list
tasks = body.get('tasks') if isinstance(body, dict) and 'tasks' in body else body
if not isinstance(tasks, list):
return HttpResponseBadRequest('Expected a JSON array of tasks')
except Exception as e:
return HttpResponseBadRequest('Invalid JSON payload')


enriched = []
for idx, t in enumerate(tasks):
# ensure dictionary
if not isinstance(t, dict):
continue
# attach an id if missing
t_id = t.get('id', idx + 1)
t['id'] = t_id
score, explanation = calculate_task_score(t)
enriched.append({**t, 'score': score, 'explanation': explanation})


# sort by score desc
enriched.sort(key=lambda x: x['score'], reverse=True)
return JsonResponse(enriched, safe=False)




def suggest_tasks(request):
"""GET: simple suggestion endpoint: receives optional ?source=... JSON in body is not used here.
For demonstration, expects a POST with tasks body or query param to reuse analyze logic.
To keep API simple, accept POST same as analyze but return top 3 with textual reasons.
"""
if request.method == 'GET':
return JsonResponse({'message': 'Send POST with tasks to get suggestions'}, status=200)


# reuse analyze logic for POST
return analyze_tasks(request)