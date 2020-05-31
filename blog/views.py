from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PostListView(ListView):
    """Представление списка всез постов на основе класса"""
    queryset = Post.objects.filter(status='published')  # published
    context_object_name = 'posts'  # переменная для обращения в шаблоне (по умолчанию object_list)
    paginate_by = 3
    template_name = 'blog/post/list.html'  # по умолчанию blog/post_list.html


# def post_list(request):
#     """Представление на основе функции"""
#     object_list = Post.objects.all()
#     paginator = Paginator(object_list, 3)  # 3 posts in each page
#     page = request.GET.get('page')  # запрос номера страници
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    """Конкретный пост + комментарии"""
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)

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
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form})


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
                                                    'sent': sent})
