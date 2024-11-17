from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

# Create your tests here.

class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='<test.gmail.com>',
            password='<parol>'
        )
        self.post = Post.objects.create(
            title='Test title',
            body='Test text',
            summary = 'summary',
            author=self.user
        )
    def test_string_representation(self):
        post = Post(title = 'test mavzusi')
        self.assertEqual(str(post), post.title)
    def test_post_content(self):
        self.assertEqual(f'{self.post.title}','Test title')
        self.assertEqual(f'{self.post.body}','Test text')
        self.assertEqual(f'{self.post.author}','testuser')
        self.assertEqual(f'{self.post.summary}','summary')
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test title')
        self.assertTemplateUsed(response, 'home.html')
    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/2/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(no_response.status_code,404)
        self.assertTemplateUsed(response, 'post_detail.html')
        self.assertContains(response, 'Test title')
        self.assertContains(response, 'Test text')
        self.assertContains(response, 'summary')
    def test_post_delete_view(self):
        response = self.client.get('/post/1/delete/')
        no_response = self.client.get('/post/2/delete/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(no_response.status_code,404)
        self.assertTemplateUsed(response, 'post_delete.html')
        self.assertContains(response, 'Test title')

        del_response = self.client.post(f'/post/1/delete/')
        self.assertEqual(del_response.status_code, 302)
        self.assertRedirects(del_response, reverse('home'))

        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'Test title')

    def test_post_update_view(self):
        response = self.client.get('/post/1/edit/')
        no_response = self.client.get('/post/2/edit/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(no_response.status_code,404)
        self.assertTemplateUsed(response , 'post_edit.html')
        self.assertContains(response, 'Test title')

        response = self.client.post(f'/post/1/edit/', {
            'title': 'Updated Test Title',
            'body': 'Updated Test Body',
            'summary': 'Updated Summary',
            'author': self.user.id
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(f'/post/1/')

        self.assertContains(response, 'Updated Test Title')
        self.assertContains(response, 'Updated Test Body')
        self.assertContains(response, 'Updated Summary')
        self.assertContains(response, self.user)

    def test_post_create_view(self):
        response = self.client.get('/post/new/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'post_new.html')
        new_response = self.client.post(reverse('post_new'), {
            'title': 'New Test title',
            'body': 'New Test text',
            'summary': 'New Summary',
            'author': self.user
        })
        new_response = self.client.get(reverse('post_detail',args=[2]))
        xatolik xatolik xatolik!



