import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from academy.models import Booklet, Post, PostCategory, TeacherProfile


class Command(BaseCommand):
    help = "Creates default admin user and sample Persian English-teaching content if empty."

    def handle(self, *args, **options):
        User = get_user_model()
        admin_username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        admin_email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "msoltani021@gmail.com")
        admin_password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "ChangeMe1234!")

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
            )
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{admin_username}'."))

        if not TeacherProfile.objects.exists():
            TeacherProfile.objects.create(
                full_name="محمد سلطانی",
                headline="مدرس زبان انگلیسی | آموزش مکالمه، گرامر کاربردی و آمادگی آیلتس",
                short_bio=(
                    "یادگیری زبان انگلیسی بدون حفظ کردن طوطی‌وار قواعد؛ با تمرکز بر مکالمه واقعی، "
                    "درک عمیق ساختار جملات و استفاده از جزوات خلاصه و استاندارد."
                ),
                full_bio=(
                    "در این وب‌سایت آموزشی می‌توانید با مسیر تدریس من آشنا شوید، مقالات رایگان یادگیری زبان را "
                    "مطالعه کنید و جزوات و کتابچه‌های تالیفی را مستقیم از طریق تلگرام سفارش دهید. "
                    "تمامی اطلاعات این بخش از طریق پنل مدیریت سایت به‌راحتی قابل ویرایش است."
                ),
                teaching_philosophy=(
                    "هدف من در تدریس زبان انگلیسی، ایجاد اعتمادبه‌نفس در صحبت کردن و نوشتن است. "
                    "هر مبحث گرامری و واژگانی در قالب مثال‌های روزمره و تمرین‌های هدفمند آموزش داده می‌شود."
                ),
                credentials=(
                    "تدریس زبان انگلیسی عمومی و تخصصی (قابل ویرایش در پنل مدیریت)\n"
                    "طراحی جزوات طبقه‌بندی‌شده گرامر و مکالمه\n"
                    "برگزاری کلاس‌های خصوصی و آنلاین تعیین سطح و آمادگی آزمون"
                ),
                specialties=(
                    "مکالمه روان و کاربردی (Speaking)\n"
                    "گرامر به زبان ساده (Practical Grammar)\n"
                    "آمادگی آزمون آیلتس (IELTS)\n"
                    "تقویت مهارت شنیداری و تلفظ (Listening & Pronunciation)"
                ),
                email="msoltani021@gmail.com",
                telegram_username=os.environ.get("TELEGRAM_USERNAME", "inatlosm").lstrip("@"),
                office_hours="شنبه تا پنج‌شنبه، ساعت ۱۰ تا ۲۰",
            )
            self.stdout.write(self.style.SUCCESS("Seeded TeacherProfile."))

        if not PostCategory.objects.exists():
            cat_speaking = PostCategory.objects.create(name="مکالمه", slug="speaking")
            cat_grammar = PostCategory.objects.create(name="گرامر", slug="grammar")
            cat_vocab = PostCategory.objects.create(name="واژگان", slug="vocabulary")
        else:
            cat_speaking = PostCategory.objects.filter(slug="speaking").first()
            cat_grammar = PostCategory.objects.filter(slug="grammar").first()
            cat_vocab = PostCategory.objects.filter(slug="vocabulary").first()

        if not Post.objects.exists():
            Post.objects.create(
                title="چگونه بدون ترس از اشتباه، مکالمه انگلیسی را شروع کنیم؟",
                slug="how-to-start-speaking-english",
                category=cat_speaking,
                excerpt="بزرگ‌ترین مانع در صحبت کردن به زبان انگلیسی، کمال‌گرایی گرامری است. در این نوشته سه تکنیک عملی برای شکستن این سد را مرور می‌کنیم.",
                content=(
                    "بسیاری از زبان‌آموزان با وجود دانستن لغات زیاد، هنگام صحبت کردن مکث می‌کنند و نگران اشتباه گرامری هستند.\n\n"
                    "۱. به جای ترجمه کلمه‌به‌کلمه، عبارت‌های آماده (Chunks) یاد بگیرید.\n"
                    "۲. روزی ۱۰ دقیقه با صدای بلند درباره کارهای روزمره خود به انگلیسی صحبت کنید (تکنیک Shadowing و Self-Talk).\n"
                    "۳. اشتباه کردن بخشی طبیعی از مسیر تسلط است؛ هدف اول انتقال پیام و هدف دوم دقت بیشتر است."
                ),
                english_tip="Useful opener: 'To be honest, I used to hesitate before speaking, but daily practice made a huge difference.'",
                reading_minutes=4,
                is_published=True,
                is_featured=True,
            )
            Post.objects.create(
                title="تفاوت کاربردی Present Perfect و Simple Past به زبان ساده",
                slug="present-perfect-vs-simple-past",
                category=cat_grammar,
                excerpt="یکی از پرتکرارترین سوالات زبان‌آموزان فارسی‌زبان، تشخیص دقیق زمان گذشته ساده و حال کامل است.",
                content=(
                    "هرگاه زمان انجام کار در گذشته مشخص و تمام‌شده باشد (مثل دیروز یا سال گذشته)، از Simple Past استفاده می‌کنیم.\n\n"
                    "اما اگر اثر آن کار همچنان تا لحظه حال ادامه داشته باشد یا زمان دقیق آن مهم نباشد، زمان درست Present Perfect است.\n\n"
                    "با تمرین جملات مقایسه در زندگی روزمره، این تفاوت ظرف چند روز کاملاً در ذهن شما تثبیت می‌شود."
                ),
                english_tip="Simple Past: I visited Shiraz in 2023.\nPresent Perfect: I have visited Shiraz three times.",
                reading_minutes=5,
                is_published=True,
                is_featured=True,
            )
            Post.objects.create(
                title="۵ عبارت جایگزین Very برای طبیعی‌تر صحبت کردن",
                slug="five-alternatives-to-very",
                category=cat_vocab,
                excerpt="استفاده مکرر از کلمه very باعث تکراری شدن جملات می‌شود. با جایگزین‌های دقیق‌تر، انگلیسی حرفه‌ای‌تری صحبت کنید.",
                content=(
                    "در مکالمات روزمره و آزمون آیلتس، استفاده از صفات دقیق‌تر به جای ترکیب very + صفت ساده امتیاز واژگان شما را به‌طور محسوسی بالا می‌برد.\n\n"
                    "به جای حفظ کردن فهرست‌های طولانی، هر هفته تنها ۵ صفت قوی را انتخاب کنید و در مکالمات همان هفته به کار ببرید."
                ),
                english_tip="very tired -> exhausted\nvery important -> crucial\nvery good -> outstanding\nvery big -> enormous\nvery happy -> thrilled",
                reading_minutes=3,
                is_published=True,
                is_featured=False,
            )
            self.stdout.write(self.style.SUCCESS("Seeded sample Posts."))

        if not Booklet.objects.exists():
            Booklet.objects.create(
                title="جزوه جامع گرامر کاربردی در ۳۰ روز",
                slug="practical-grammar-30-days",
                item_type="pamphlet",
                level="B1-B2",
                delivery_format="PDF",
                pages_count=68,
                price_toman=180000,
                discount_price_toman=145000,
                short_description="خلاصه تمام مباحث کلیدی گرامر انگلیسی با توضیح فارسی روان، جداول مقایسه‌ای و تمرین‌های پاسخ‌دار.",
                description=(
                    "این جزوه برای زبان‌آموزانی طراحی شده که می‌خواهند یک‌بار برای همیشه ساختار زمان‌ها، "
                    "جملات شرطی، مجهول و حروف اضافه را به شکل منظم و کاربردی یاد بگیرند. "
                    "تمامی مثال‌ها از مکالمات واقعی انتخاب شده‌اند."
                ),
                highlights=(
                    "پوشش کامل ۱۲ زمان انگلیسی با جدول مقایسه\n"
                    "تمرین‌های طبقه‌بندی‌شده همراه با پاسخنامه تشریحی\n"
                    "طراحی خوانا مناسب مطالعه روی موبایل، تبلت و چاپ"
                ),
                is_available=True,
                is_featured=True,
            )
            Booklet.objects.create(
                title="کتابچه ۵۰۰ عبارت طلایی مکالمه روزمره",
                slug="500-everyday-speaking-phrases",
                item_type="booklet",
                level="A1-A2",
                delivery_format="PDF+AUDIO",
                pages_count=92,
                price_toman=240000,
                short_description="مجموعه‌ای از پرکاربردترین اصطلاحات و جملات آماده برای موقعیت‌های روزمره، سفر، کار و گفت‌وگوهای دوستانه.",
                description=(
                    "به جای حفظ کردن کلمات پراکنده، با این کتابچه یاد می‌گیرید در هر موقعیت دقیقاً چه عبارتی به کار ببرید. "
                    "همراه با ترجمه طبیعی فارسی و نکات تلفظی."
                ),
                highlights=(
                    "دسته‌بندی‌شده در ۲۰ موضوع کاربردی روزمره\n"
                    "مثال واقعی برای هر عبارت همراه با ترجمه فارسی\n"
                    "مناسب تقویت سریع اعتمادبه‌نفس در Speaking"
                ),
                is_available=True,
                is_featured=True,
            )
            Booklet.objects.create(
                title="جزوه تکنیک‌های رایتینگ و اسپیکینگ آیلتس",
                slug="ielts-speaking-writing-pamphlet",
                item_type="pamphlet",
                level="IELTS",
                delivery_format="PDF",
                pages_count=54,
                price_toman=290000,
                discount_price_toman=250000,
                short_description="قالب‌های استاندارد پاسخ‌دهی، واژگان نمره‌آور و اشتباهات رایج داوطلبان فارسی‌زبان در آزمون آیلتس.",
                description=(
                    "این جزوه حاصل تجربه تدریس و بررسی اشتباهات پرتکرار زبان‌آموزان در بخش‌های Writing Task 2 و Speaking است "
                    "و به شما کمک می‌کند پاسخ‌های منسجم‌تر و دقیق‌تری ارائه دهید."
                ),
                highlights=(
                    "ساختار گام‌به‌گام پاراگراف‌نویسی استاندارد\n"
                    "بانک کالوکیشن‌های پرتکرار موضوعات آیلتس\n"
                    "نمونه پاسخ‌های تحلیل‌شده با نکات کلیدی"
                ),
                is_available=True,
                is_featured=True,
            )
            self.stdout.write(self.style.SUCCESS("Seeded sample Booklets."))
