from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PostListView(ListView):
    """Представление списка всез постов на основе класса"""
    queryset = Post.objects.filter(status='published')  # published
    context_object_name = 'posts'  # переменная для обращения в шаблоне (по умолчанию object_list)
    paginate_by = 3
    template_name = 'blog/post/list.html'  # по умолчанию blog/post_list.html


def post_list(request, tag_slug=None):
    """Представление на основе функции"""
    object_list = Post.objects.filter(status='published')
    tag = None
    # если в строке запроса есть tag/... - выводим список только тех постов в которых есть данный тег
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    # Пагинация
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')  # запрос номера страници
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    # print(dir(request))
    # print(request.user)
    # print(request.body)
    # print(request.GET)
    # print(request.content_params)
    # print(request.path)
    # print(request.scheme)
    # print(request.path_info)
    # print(request.headers['Content-Type'])
    # print(request.get_port())
    # print(request.get_host())


    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag
                                                   })


def post_detail(request, year, month, day, post):
    """Конкретный пост + добавление комментариев"""
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    added_comment = False

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()  # метод save доступен только для ModelForm, а не для Form
            added_comment = True
    else:
        comment_form = CommentForm()
    # List of similar posts
    # https://pocoz.gitbooks.io/django-v-primerah/content/glava-2-uluchshenie-bloga-s-pomoshyu-rasshirennyh-vozmozhnostej/poluchenie-zapisej-po-shodstvu.html
    post_tags_ids = post.tags.values_list('id', flat=True)  # извлекаем список id тегов которые есть у данного поста
    # TODO отфильтровать published
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)  # отбор потов с такими же тегами
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    # print(similar_posts)
    # print(similar_posts.annotate(same_tags=Count('tags')))
    # print(Count('tags'))
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'added_comment': added_comment,
                                                     'similar_posts': similar_posts
                                                     })


# TODO разобраться с ошибкой new_comment
#  https://pocoz.gitbooks.io/django-v-primerah/content/glava-2-uluchshenie-bloga-s-pomoshyu-rasshirennyh
#  -vozmozhnostej/sozdanie-sistemy-kommentariev/dobavlenie-kommentariev-v-shablon-post-detail.html


def post_share(request, post_id):
    """Отправка ссылки названия поста по почте"""
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data  # словарь полей форм и их значений (form.error - Список ошибок)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'r.boyko@standart.ua', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent
                                                    })
