from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from habits.models import Habit

class HabitViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('bob', password='secret')
        self.client.login(username='bob', password='secret')

    def test_habit_list_requires_login(self):
        self.client.logout()
        resp = self.client.get(reverse('habit_list'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login/', resp.url)

    def test_add_and_delete_habit(self):
        # добавляем привычку через POST на habit_list
        resp = self.client.post(
            reverse('habit_list'),
            {'name': 'Read', 'target_per_day': 2},
            follow=True
        )
        self.assertContains(resp, 'Read')
        habit = Habit.objects.get(name='Read')

        # удаляем
        resp = self.client.get(
            reverse('delete_habit', args=[habit.id]),
            follow=True
        )
        self.assertNotContains(resp, 'Read')
        self.assertFalse(Habit.objects.filter(pk=habit.id).exists())

    def test_complete_habit(self):
        h = Habit.objects.create(user=self.user, name='Walk', target_per_day=1)
        url = reverse('complete_habit', args=[h.id])
        resp = self.client.get(url, follow=True)
        self.assertRedirects(resp, reverse('habit_list'))
        h.refresh_from_db()
        self.assertEqual(h.done_today, 1)
        self.assertTrue(h.is_completed)
