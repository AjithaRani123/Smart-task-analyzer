from django.test import TestCase
from .scoring import calculate_task_score
from datetime import date, timedelta


class ScoringTests(TestCase):
def test_overdue_task(self):
t = {'title':'A','due_date': (date.today()-timedelta(days=2)).isoformat(), 'importance':8, 'estimated_hours':3}
score, explanation = calculate_task_score(t)
self.assertTrue(score > 0)
self.assertIn('OVERDUE', ' '.join(explanation))


def test_quick_task_bonus(self):
t = {'title':'Quick','due_date': (date.today()+timedelta(days=10)).isoformat(), 'importance':5, 'estimated_hours':1}
score, explanation = calculate_task_score(t)
self.assertTrue(any('Quick task' in e for e in explanation))