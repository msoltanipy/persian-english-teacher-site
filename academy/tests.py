from urllib.parse import unquote

from django.test import TestCase
from django.urls import reverse

from .models import Booklet, ContactMessage, Post, PostCategory, TeacherProfile


class AcademyViewsTest(TestCase):
    def setUp(self):
        self.profile = TeacherProfile.objects.create(
            full_name="محمد سلطانی",
            telegram_username="inatlosm",
            email="msoltani021@gmail.com",
        )
        self.category = PostCategory.objects.create(name="گرامر", slug="grammar")
        self.post = Post.objects.create(
            title="تست مقاله آموزشی",
            slug="test-post",
            category=self.category,
            excerpt="خلاصه کوتاه مقاله",
            content="متن کامل مقاله آموزشی",
            is_published=True,
        )
        self.booklet = Booklet.objects.create(
            title="جزوه مکالمه سریع",
            slug="fast-speaking",
            item_type="pamphlet",
            level="B1-B2",
            price_toman=150000,
            short_description="توضیح کوتاه جزوه",
            description="توضیح کامل جزوه",
            is_available=True,
        )

    def test_pages_return_200(self):
        urls = [
            reverse("academy:home"),
            reverse("academy:profile"),
            reverse("academy:post_list"),
            reverse("academy:post_detail", kwargs={"slug": self.post.slug}),
            reverse("academy:booklet_list"),
            reverse("academy:booklet_detail", kwargs={"slug": self.booklet.slug}),
            reverse("academy:contact"),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed on {url}")

    def test_telegram_order_link_contains_handle_and_persian_message(self):
        url = self.booklet.get_telegram_order_url("inatlosm")
        self.assertTrue(url.startswith("https://t.me/inatlosm?text="))
        decoded = unquote(url)
        self.assertIn("جزوه مکالمه سریع", decoded)
        self.assertIn("سلام استاد", decoded)

    def test_contact_form_submission(self):
        response = self.client.post(
            reverse("academy:contact"),
            {
                "full_name": "علی رضایی",
                "telegram_or_phone": "@alirezaei",
                "email": "ali@example.com",
                "subject": "مشاوره کلاس",
                "message": "سلام، درباره کلاس مکالمه سوال داشتم.",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)
