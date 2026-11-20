from urllib.parse import quote

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class TeacherProfile(models.Model):
    full_name = models.CharField("نام و نام خانوادگی", max_length=120, default="محمد سلطانی")
    headline = models.CharField(
        "عنوان تخصصی",
        max_length=200,
        default="مدرس تخصصی زبان انگلیسی | مکالمه، گرامر و آمادگی آیلتس",
    )
    short_bio = models.TextField(
        "معرفی کوتاه (صفحه اصلی)",
        default="آموزش اصولی و کاربردی زبان انگلیسی با تمرکز بر مکالمه روان، ساختارهای استاندارد و جزوات دست‌نویس و طبقه‌بندی‌شده.",
    )
    full_bio = models.TextField(
        "بیوگرافی کامل",
        default="این بخش را می‌توانید از طریق پنل مدیریت جنگو متناسب با سوابق تحصیلی، مدارک تدریس و روش آموزشی خود ویرایش کنید.",
    )
    teaching_philosophy = models.TextField(
        "روش و فلسفه تدریس",
        blank=True,
        default="یادگیری زبان انگلیسی زمانی ماندگار است که قواعد پیچیده به زبان ساده توضیح داده شوند و بلافاصله در مکالمه و نوشتار واقعی تمرین شوند.",
    )
    credentials = models.TextField(
        "مدارک و افتخارات (هر مورد در یک خط)",
        blank=True,
        help_text="هر مدرک یا سابقه را در یک خط جدید بنویسید.",
    )
    specialties = models.TextField(
        "حوزه‌های تخصصی تدریس (هر مورد در یک خط)",
        blank=True,
        default="مکالمه کاربردی و روان (Speaking)\nگرامر ساده و ساختاری\nآمادگی آزمون آیلتس (IELTS)\nانگلیسی عمومی و دانشگاهی",
    )
    avatar = models.ImageField("تصویر پروفایل", upload_to="profile/", blank=True, null=True)
    email = models.EmailField("ایمیل", default="msoltani021@gmail.com")
    phone = models.CharField("شماره تماس (اختیاری)", max_length=40, blank=True)
    telegram_username = models.CharField(
        "آیدی تلگرام (بدون @)",
        max_length=64,
        default="inatlosm",
        help_text="نام کاربری تلگرام بدون علامت @ وارد شود (مثلاً inatlosm).",
    )
    instagram_url = models.URLField("لینک اینستاگرام (اختیاری)", blank=True)
    youtube_url = models.URLField("لینک یوتیوب (اختیاری)", blank=True)
    office_hours = models.CharField(
        "ساعات پاسخ‌گویی",
        max_length=120,
        blank=True,
        default="شنبه تا پنج‌شنبه، ساعت ۱۰ تا ۲۰",
    )
    updated_at = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "پروفایل مدرس"
        verbose_name_plural = "پروفایل مدرس"

    def __str__(self) -> str:
        return self.full_name

    @property
    def clean_telegram_username(self) -> str:
        handle = (self.telegram_username or settings.TELEGRAM_USERNAME or "inatlosm").strip()
        return handle.lstrip("@")

    def get_credentials_list(self) -> list[str]:
        return [line.strip() for line in self.credentials.splitlines() if line.strip()]

    def get_specialties_list(self) -> list[str]:
        return [line.strip() for line in self.specialties.splitlines() if line.strip()]

    def get_telegram_contact_url(self) -> str:
        message = (
            "سلام استاد، وقت بخیر. "
            "از طریق وب‌سایت آموزشی پیام می‌دهم و درباره کلاس‌ها و منابع آموزشی سوال داشتم."
        )
        return f"https://t.me/{self.clean_telegram_username}?text={quote(message)}"


class PostCategory(models.Model):
    name = models.CharField("نام دسته‌بندی", max_length=80)
    slug = models.SlugField("اسلاگ (انگلیسی)", max_length=100, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = "دسته‌بندی مقاله"
        verbose_name_plural = "دسته‌بندی‌های مقالات"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    title = models.CharField("عنوان نوشته", max_length=200)
    slug = models.SlugField("اسلاگ", max_length=220, unique=True, allow_unicode=True)
    category = models.ForeignKey(
        PostCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="دسته‌بندی",
    )
    excerpt = models.TextField("خلاصه نوشته", max_length=360)
    content = models.TextField("متن کامل نوشته")
    english_tip = models.TextField(
        "نکته یا مثال انگلیسی (اختیاری)",
        blank=True,
        help_text="متن انگلیسی این بخش به‌صورت چپ‌به‌راست (LTR) نمایش داده می‌شود.",
    )
    cover_image = models.ImageField("تصویر شاخص", upload_to="posts/", blank=True, null=True)
    reading_minutes = models.PositiveSmallIntegerField("زمان مطالعه (دقیقه)", default=4)
    is_published = models.BooleanField("منتشر شده", default=True)
    is_featured = models.BooleanField("نمایش ویژه در صفحه اصلی", default=False)
    created_at = models.DateTimeField("تاریخ انتشار", auto_now_add=True)
    updated_at = models.DateTimeField("آخرین ویرایش", auto_now=True)

    class Meta:
        verbose_name = "نوشته / مقاله"
        verbose_name_plural = "نوشته‌ها و مقالات"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("academy:post_detail", kwargs={"slug": self.slug})


class Booklet(models.Model):
    ITEM_TYPE_CHOICES = [
        ("booklet", "کتابچه"),
        ("pamphlet", "جزوه"),
    ]
    LEVEL_CHOICES = [
        ("A1-A2", "مقدماتی (A1–A2)"),
        ("B1-B2", "متوسط (B1–B2)"),
        ("C1-C2", "پیشرفته (C1–C2)"),
        ("IELTS", "آمادگی آیلتس (IELTS)"),
        ("ALL", "مناسب همه سطوح"),
    ]
    FORMAT_CHOICES = [
        ("PDF", "فایل PDF با کیفیت بالا"),
        ("PDF+AUDIO", "فایل PDF + فایل صوتی"),
        ("PRINT", "نسخه چاپی"),
    ]

    title = models.CharField("عنوان جزوه یا کتابچه", max_length=200)
    slug = models.SlugField("اسلاگ", max_length=220, unique=True, allow_unicode=True)
    item_type = models.CharField("نوع منبع", max_length=20, choices=ITEM_TYPE_CHOICES, default="pamphlet")
    level = models.CharField("سطح آموزشی", max_length=20, choices=LEVEL_CHOICES, default="ALL")
    delivery_format = models.CharField("فرمت ارائه", max_length=20, choices=FORMAT_CHOICES, default="PDF")
    pages_count = models.PositiveIntegerField("تعداد صفحات", default=40)
    price_toman = models.PositiveIntegerField("قیمت (تومان)", default=150000)
    discount_price_toman = models.PositiveIntegerField(
        "قیمت با تخفیف (تومان - اختیاری)",
        blank=True,
        null=True,
    )
    short_description = models.TextField("توضیح کوتاه", max_length=320)
    description = models.TextField("توضیحات کامل و سرفصل‌ها")
    highlights = models.TextField(
        "ویژگی‌های کلیدی (هر مورد در یک خط)",
        blank=True,
        help_text="هر ویژگی یا سرفصل مهم را در یک خط جداگانه وارد کنید.",
    )
    cover_image = models.ImageField("تصویر جلد", upload_to="booklets/", blank=True, null=True)
    is_available = models.BooleanField("موجود برای سفارش", default=True)
    is_featured = models.BooleanField("نمایش ویژه در صفحه اصلی", default=True)
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "جزوه / کتابچه"
        verbose_name_plural = "جزوات و کتابچه‌ها"
        ordering = ["-is_featured", "-created_at"]

    def __str__(self) -> str:
        return f"{self.get_item_type_display()} — {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def effective_price(self) -> int:
        if self.discount_price_toman and self.discount_price_toman < self.price_toman:
            return self.discount_price_toman
        return self.price_toman

    @property
    def has_discount(self) -> bool:
        return bool(self.discount_price_toman and self.discount_price_toman < self.price_toman)

    def get_highlights_list(self) -> list[str]:
        return [line.strip() for line in self.highlights.splitlines() if line.strip()]

    def get_absolute_url(self) -> str:
        return reverse("academy:booklet_detail", kwargs={"slug": self.slug})

    def get_telegram_message(self) -> str:
        price_str = f"{self.effective_price:,}"
        return (
            f"سلام استاد، وقت بخیر. "
            f"قصد خرید {self.get_item_type_display()} «{self.title}» "
            f"(سطح: {self.get_level_display()} | مبلغ: {price_str} تومان) را دارم. "
            f"لطفاً شرایط دریافت و پرداخت را ارسال بفرمایید."
        )

    def get_telegram_order_url(self, username: str | None = None) -> str:
        handle = (username or settings.TELEGRAM_USERNAME or "inatlosm").strip().lstrip("@")
        return f"https://t.me/{handle}?text={quote(self.get_telegram_message())}"


class ContactMessage(models.Model):
    full_name = models.CharField("نام و نام خانوادگی", max_length=120)
    email = models.EmailField("ایمیل", blank=True)
    telegram_or_phone = models.CharField("آیدی تلگرام یا شماره تماس", max_length=80)
    subject = models.CharField("موضوع پیام", max_length=180)
    message = models.TextField("متن پیام")
    is_read = models.BooleanField("خوانده شده", default=False)
    created_at = models.DateTimeField("تاریخ ارسال", auto_now_add=True)

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.full_name} — {self.subject}"
