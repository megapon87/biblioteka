from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Book, SavedBook


class BookModelTests(TestCase):
    def test_str(self):
        book = Book.objects.create(title="Тест", author="Автор", pages_total=10)
        self.assertEqual(str(book), "Тест — Автор")

    def test_books_are_seeded(self):
        # книги додаються міграціями
        self.assertGreaterEqual(Book.objects.count(), 75)


class PublicPagesTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Унікальна Книга", author="Унікальний Автор",
            pages_total=100, summary="Короткий переказ",
        )

    def test_home_page_opens(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_book_detail_opens(self):
        response = self.client.get(reverse('book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Унікальна Книга")
        self.assertContains(response, "Короткий переказ")

    def test_book_detail_404(self):
        response = self.client.get(reverse('book_detail', args=[999999]))
        self.assertEqual(response.status_code, 404)

    def test_all_books_open(self):
        for book in Book.objects.all():
            response = self.client.get(reverse('book_detail', args=[book.id]))
            self.assertEqual(response.status_code, 200, book.title)


class SearchTests(TestCase):
    def setUp(self):
        Book.objects.create(title="Унікальна Книга", author="Унікальний Автор", pages_total=1)

    def test_search_by_title(self):
        response = self.client.get(reverse('home'), {'q': 'Унікальна'})
        self.assertContains(response, "Унікальна Книга")

    def test_search_by_author(self):
        response = self.client.get(reverse('home'), {'q': 'Унікальний'})
        self.assertContains(response, "Унікальна Книга")

    def test_search_no_results(self):
        response = self.client.get(reverse('home'), {'q': 'zzzzнемаємотакої'})
        self.assertContains(response, "нічого не знайдено")


class AuthTests(TestCase):
    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'reader', 'email': '',
            'password1': 'verysecret123', 'password2': 'verysecret123',
        })
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(User.objects.filter(username='reader').exists())

    def test_register_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'reader', 'email': '',
            'password1': 'verysecret123', 'password2': 'different999',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='reader').exists())

    def test_register_duplicate_username(self):
        User.objects.create_user('reader', password='x12345678')
        response = self.client.post(reverse('register'), {
            'username': 'reader', 'email': '',
            'password1': 'verysecret123', 'password2': 'verysecret123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username='reader').count(), 1)

    def test_login_success(self):
        User.objects.create_user('reader', password='verysecret123')
        response = self.client.post(reverse('login'), {
            'username': 'reader', 'password': 'verysecret123',
        })
        self.assertRedirects(response, reverse('profile'))

    def test_login_wrong_password(self):
        User.objects.create_user('reader', password='verysecret123')
        response = self.client.post(reverse('login'), {
            'username': 'reader', 'password': 'wrong',
        })
        self.assertContains(response, "Невірний логін або пароль")

    def test_logout(self):
        User.objects.create_user('reader', password='verysecret123')
        self.client.login(username='reader', password='verysecret123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))

    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")


class SavedBookTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('reader', password='verysecret123')
        self.book = Book.objects.create(title="Збережена", author="А", pages_total=1)
        self.client.login(username='reader', password='verysecret123')

    def test_save_book(self):
        self.client.post(reverse('toggle_save', args=[self.book.id]))
        self.assertTrue(SavedBook.objects.filter(user=self.user, book=self.book).exists())

    def test_toggle_removes_book(self):
        url = reverse('toggle_save', args=[self.book.id])
        self.client.post(url)
        self.client.post(url)
        self.assertFalse(SavedBook.objects.filter(user=self.user, book=self.book).exists())

    def test_saved_book_shows_in_profile(self):
        SavedBook.objects.create(user=self.user, book=self.book)
        response = self.client.get(reverse('profile'))
        self.assertContains(response, "Збережена")

    def test_save_requires_login(self):
        self.client.logout()
        response = self.client.post(reverse('toggle_save', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(SavedBook.objects.exists())

    def test_users_have_separate_saved_lists(self):
        other = User.objects.create_user('other', password='verysecret123')
        SavedBook.objects.create(user=other, book=self.book)
        response = self.client.get(reverse('profile'))
        self.assertNotContains(response, "Збережена")