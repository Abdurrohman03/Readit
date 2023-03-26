from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Article, Category, Tag, Comment
from .forms import CommentForm


def index(request):
    articles = Article.objects.order_by('-id')
    ctx = {
        'object_list': articles
    }
    return render(request, 'readit/index.html', ctx)


def article_list(request):
    articles = Article.objects.order_by('-id')
    cat = request.GET.get('cat')
    tag = request.GET.get('tag')
    search = request.GET.get('search')
    if search:
        articles = articles.filter(title__icontains=search)
    if cat:
        articles = articles.filter(category__title__exact=cat)
    if tag:
        articles = articles.filter(tags__title__exact=tag)
    ctx = {
        'object_list': articles
    }
    return render(request, 'readit/blog.html', ctx)


def article_detail(request, pk):
    article = get_object_or_404(Article, id=pk)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    last_3_articles = Article.objects.order_by('-id')[:3]
    form = CommentForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(reverse('blog:detail', kwargs={'pk': pk}))
        form = CommentForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author_id = request.user.profile.id
            obj.article_id = article.id
            obj.save()
            return redirect(reverse('blog:detail', kwargs={'pk': pk}))

    ctx = {
        'object': article,
        'categories': categories,
        'tags': tags,
        'last_3_articles': last_3_articles,
        'form': form
    }
    return render(request, 'readit/blog-single.html', ctx)


