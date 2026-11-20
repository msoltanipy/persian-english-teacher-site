from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactMessageForm
from .models import Booklet, Post, PostCategory, TeacherProfile


def _get_telegram_handle() -> str:
    profile = TeacherProfile.objects.first()
    return profile.clean_telegram_username if profile else "inatlosm"


def home(request):
    featured_booklets = Booklet.objects.filter(is_available=True)[:4]
    latest_posts = Post.objects.filter(is_published=True).select_related("category")[:3]
    telegram_handle = _get_telegram_handle()
    for item in featured_booklets:
        item.telegram_url = item.get_telegram_order_url(telegram_handle)

    context = {
        "featured_booklets": featured_booklets,
        "latest_posts": latest_posts,
        "booklets_count": Booklet.objects.filter(is_available=True).count(),
        "posts_count": Post.objects.filter(is_published=True).count(),
    }
    return render(request, "academy/home.html", context)


def profile_view(request):
    profile = TeacherProfile.objects.first()
    return render(request, "academy/profile.html", {"profile": profile})


def post_list(request):
    category_slug = request.GET.get("category", "").strip()
    query = request.GET.get("q", "").strip()

    posts = Post.objects.filter(is_published=True).select_related("category")
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(excerpt__icontains=query)
            | Q(content__icontains=query)
        )

    categories = PostCategory.objects.all()
    context = {
        "posts": posts,
        "categories": categories,
        "active_category": category_slug,
        "search_query": query,
    }
    return render(request, "academy/post_list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related("category"), slug=slug, is_published=True)
    related_posts = (
        Post.objects.filter(is_published=True)
        .exclude(pk=post.pk)
        .select_related("category")[:3]
    )
    return render(
        request,
        "academy/post_detail.html",
        {"post": post, "related_posts": related_posts},
    )


def booklet_list(request):
    item_type = request.GET.get("type", "").strip()
    level = request.GET.get("level", "").strip()
    query = request.GET.get("q", "").strip()

    booklets = Booklet.objects.filter(is_available=True)
    if item_type in ("booklet", "pamphlet"):
        booklets = booklets.filter(item_type=item_type)
    if level:
        booklets = booklets.filter(level=level)
    if query:
        booklets = booklets.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(description__icontains=query)
        )

    telegram_handle = _get_telegram_handle()
    booklets_list = list(booklets)
    for item in booklets_list:
        item.telegram_url = item.get_telegram_order_url(telegram_handle)

    context = {
        "booklets": booklets_list,
        "active_type": item_type,
        "active_level": level,
        "search_query": query,
        "level_choices": Booklet.LEVEL_CHOICES,
    }
    return render(request, "academy/booklet_list.html", context)


def booklet_detail(request, slug):
    booklet = get_object_or_404(Booklet, slug=slug, is_available=True)
    telegram_handle = _get_telegram_handle()
    telegram_url = booklet.get_telegram_order_url(telegram_handle)
    telegram_message = booklet.get_telegram_message()
    other_booklets = Booklet.objects.filter(is_available=True).exclude(pk=booklet.pk)[:3]
    for item in other_booklets:
        item.telegram_url = item.get_telegram_order_url(telegram_handle)

    context = {
        "booklet": booklet,
        "telegram_url": telegram_url,
        "telegram_message": telegram_message,
        "other_booklets": other_booklets,
    }
    return render(request, "academy/booklet_detail.html", context)


def contact_view(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "پیام شما با موفقیت ثبت شد. در کوتاه‌ترین زمان با شما تماس می‌گیرم.",
            )
            return redirect("academy:contact")
    else:
        form = ContactMessageForm()

    return render(request, "academy/contact.html", {"form": form})
