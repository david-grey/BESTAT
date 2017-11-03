# encoding: utf-8

'''

@author: ZiqiLiu


@file: views.py

@time: 2017/10/25 下午2:54

@desc:
'''

from mimetypes import guess_type

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator, \
    PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods, require_GET, \
    require_POST

from django.urls import reverse
from bestat.models import Profile, Review, Comment, NeighborInfo, Neighbor
from bestat.decorator import check_anonymous, login_required, anonymous_only
from bestat.forms import UserCreationForm, LoginForm, ChangePasswordForm, \
    ProfileForm, UsernameForm, ResetPassword
from bestat.utils import is_anonymous
from django.http import JsonResponse, Http404
import datetime
import json

@check_anonymous
@require_GET
def home(request):
    return render(request, 'home-page.html')


@anonymous_only("You have already login!")
@check_anonymous
def signup(request):
    context = {}
    if request.method == "GET":
        context['form'] = UserCreationForm()
        return render(request, 'sign-up.html', context)
    else:
        form = UserCreationForm(request.POST)
        context['form'] = form

        if not form.is_valid():
            errors = [v.as_text() for k, v in form.errors.items()]
            context['errors'] = errors
            return render(request, 'sign-up.html', context)

        params = form.cleaned_data
        user = User.objects.create_user(params['username'], params['email'],
                                        params['password'],
                                        first_name=params['first_name'],
                                        last_name=params['last_name'])
        user.save()
        profile = Profile.objects.create(user=user,
                                         nick_name=params['nick_name'])
        profile.save()
        token = default_token_generator.make_token(user)

        email_body = '''
           Welcome to bestat. Please click the link below to verify your email address and complete the registration proceess. http://%s%s
           ''' % (request.get_host(),
                  reverse('confirm', args=(user.username, token)))
        send_mail(subject="Verify your email address",
                  message=email_body,
                  from_email="ziqil1@andrew.cmu.edu",
                  recipient_list=[user.email])
        context['msg'] = 'Your confirmation link has been send to your register email.'
        return render(request, 'blank.html', context)


@require_http_methods(['GET', 'POST'])
@anonymous_only("You've already login!")
@check_anonymous
def signin(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        pass
    else:
        form = LoginForm(request.POST)
        if not form.is_valid():
            errors = [v.as_text() for k, v in form.errors.items()]
            context['errors'] = errors
        else:
            params = form.cleaned_data
            username = params['username']
            password = params['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                print('flag2')
                # login success
                if user.is_active:
                    print('login success')
                    login(request, user)
                    return redirect('/')
                else:
                    context['errors'] = ['account banned!']
            else:
                print('flag1')
                errors = ['password incorrect']
                try:
                    User.objects.get(username=username)
                except User.DoesNotExist:
                    errors = ['user not exist']
                context["errors"] = errors

    return render(request, 'sign-in.html', context=context)


@require_http_methods(['GET', 'POST'])
@login_required("you haven't login!")
def change_password(request):
    context = {'errors': []}
    if request.method == 'GET':
        context['form'] = ChangePasswordForm()
    else:

        form = ChangePasswordForm(request.POST)
        if not form.is_valid():
            errors = [v.as_text() for k, v in form.errors.items()]
            context['errors'].extend(errors)
        else:
            old_password = form.cleaned_data['old_password']
            password = form.cleaned_data['password']
            user = authenticate(username=request.user.username,
                                password=old_password)
            if user is not None:
                request.user.set_password(password)
                request.user.save()
                return redirect('/')
            else:
                context['errors'].append('old password not correct!')
        context['form'] = ChangePasswordForm()
    return render(request, 'change_password.html', context)


@require_http_methods(['GET', 'POST'])
@login_required("you haven't login!")
def edit_profile(request):
    user = request.user
    context = {'errors': []}
    if request.method == 'GET':
        context['form'] = ProfileForm(
            {'first_name': user.first_name, 'last_name': user.last_name,
             'email': user.email, 'nick_name': user.profile.nick_name})

    else:
        form = ProfileForm(request.POST,
                           request.FILES if request.FILES else None)
        if not form.is_valid():
            errors = [v.as_text() for k, v in form.errors.items()]
            context['errors'].extend(errors)
        else:
            params = form.cleaned_data
            user.first_name = params['first_name']
            user.last_name = params['last_name']
            user.email = params['email']
            user.save()
            if form.cleaned_data['img']:
                user.profile.img = form.cleaned_data['img']
            user.profile.nick_name = params['nick_name']
            user.profile.save()
            context['success'] = True
            context['form'] = form
    return render(request, 'profile.html', context)


@require_GET
def get_photo(request, user_id):
    user = User.objects.get(id=user_id)
    content_type = guess_type(user.profile.img.name)
    return HttpResponse(user.profile.img, content_type=content_type)


@require_GET
@login_required("you haven't login!")
def logout_user(request):
    logout(request)
    return redirect('/')

@require_GET
def confirm(request, username, token):
    generator = PasswordResetTokenGenerator()
    try:
        user = User.objects.get(username=username)
        if generator.check_token(user, token):
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'blank.html', {'msg': 'token not valid'})
    except User.DoesNotExist:
        return render(request, 'blank.html', {'msg': 'user non exist!'})


@require_GET
def about(request):
    context = {'user': request.user}
    return render(request, 'about.html', context)


@require_GET
def contact(request):
    return render(request, 'contact.html')


@require_POST
@login_required('to create review, you must login first')
def create_review(request):
    user = request.user
    review = Review.objects.create(author=user, text=request.POST['text'])
    return redirect('/profile')


@check_anonymous
@require_POST
@login_required('to add comment, you must login first')
def add_comment(request):
    user = request.user

    review = get_object_or_404(Review, id=request.POST['review_id'])
    ts = datetime.datetime.now()
    new_comment = Comment.objects.create(review=review, author=user,
                                         text=request.POST['text'],
                                         create_time=ts)
    return JsonResponse({'comment': render_to_string('ajax_comment.html', {
        'comment': new_comment, }, request)})


@check_anonymous
@require_POST
@login_required('to delete comment, you must login first')
def delete_comment(request):
    comment_id = request.POST.get('comment_id', None)
    if comment_id:
        comment = get_object_or_404(Comment, id=comment_id)
        review = comment.review
        if review.author != request.user:
            return render(request, 'blank.html', {
                "msg": "you can not delete comments from others' blog"})
        comment.delete()
        return JsonResponse({'comments_num': review.comments_num})

    return Http404


@require_GET
@login_required('to delete review, you must login first')
def delete_review(request, review_id):
    user = request.user
    review = get_object_or_404(Review, id=review_id)
    if review.author == user:
        review.delete()
    else:
        return HttpResponse("Hey bro, don't try to delete others' blogs!")
    return redirect('/profile')


@require_GET
@login_required()
def likes(request, block_id):
    blog = get_object_or_404(NeighborInfo, id=block_id)
    flag = True
    if blog.liked(request.user):
        blog.likes.remove(request.user)
        flag = False
    else:
        blog.likes.add(request.user)
    return JsonResponse({'likes_num': blog.likes_num, 'liked': flag})


@check_anonymous
@require_POST
@login_required()
def update_reviews(request):
    params = dict(request.POST)
    time = params.get('max_time', None)

    _personal = params.get('personal', None)
    _stream = params.get('stream', False)
    user = request.user
    if time:
        time = int(time[0])
        max_time = Review.get_max_time()

        _blogs = Review.get_changes(time, user if _personal else None, _stream)

        blogs = [render_to_string('ajax_blog.html', {'blog': bl, 'user': user},
                                  request) for bl in _blogs]
        context = {'max_time': max_time, 'blogs': blogs}
        return JsonResponse(data=context)
    return Http404


@check_anonymous
@require_GET
@login_required("to access profile, you must login first")
def profile(request, user_id=None):
    if user_id is None:
        user_id = request.user.id
    try:
        user = User.objects.get(id=user_id)
    except (User.DoesNotExist, ValueError) as e:
        return render(request, 'blank.html', {'msg': 'User non exist!'})
    return _profile(request, user)


def _profile(request, target_user):
    user = request.user
    context = {'user': user, 'target_user': target_user,
               'max_time': Review.get_max_time()}

    blogs = target_user.blogs.order_by('-create_time')
    context['personal_blogs'] = blogs

    if user == target_user:
        # get personal streaming blogs
        followees = user.profile.followees.all()
        stream_blogs = []
        for f in followees:
            stream_blogs.extend(f.user.blogs.all())
        stream_blogs = sorted(stream_blogs, key=lambda blog: blog.id,
                              reverse=True)
        context['stream_blogs'] = stream_blogs
        context['own'] = True
    else:
        context['followed'] = True
        try:
            request.user.profile.followees.get(user=target_user)
        except Profile.DoesNotExist:
            context['followed'] = False

            # access his own profile

    return render(request, 'personal.html', context)


def get_comments(blog):
    '''

    :param blog: 
    :return: list of comments
    '''
    _comments = blog.comments
    comments = []
    for com in _comments:
        comments.append({'author_id': com.author.id, 'text': com.text,
                         'create_time': com.create_time})


@require_http_methods(['GET', 'POST'])
@anonymous_only("you've already login")
def forget_password(request):
    context = {}
    if request.method == 'GET':
        context['form'] = UsernameForm()
        return render(request, 'forget_password.html', context)

    else:
        form = UsernameForm(request.POST)
        if not form.is_valid():
            context['form'] = form
            render(request, 'forget_password.html', context)
        username = form.cleaned_data['username']
        user = User.objects.get(username=username)
        generator = PasswordResetTokenGenerator()
        token = generator.make_token(user)

        email_body = '''
           Welcome to bestat. Please click the link below to verify your email address and complete the registration proceess. http://%s%s
           ''' % (request.get_host(),
                  reverse('reset', args=(user.username, token)))
        send_mail(subject="Verify your email address",
                  message=email_body,
                  from_email="ziqil1@andrew.cmu.edu",
                  recipient_list=[user.email])
        context[
            'msg'] = 'Your password reset link has been send to your register email.'
        return render(request, 'blank.html', context)


@require_GET
def reset_password_check(request, user_id, token):
    generator = PasswordResetTokenGenerator()
    try:
        user = User.objects.get(username=user_id)
        if generator.check_token(user, token):
            login(request, user)
            return render(request, 'reset_password.html',
                          {'form': ResetPassword()})

    except User.DoesNotExist:
        return render(request, 'blank.html', {'msg': 'user non exist!'})


@require_POST
@login_required("you haven't login!")
def reset_password(request):
    context = {'errors': []}

    form = ResetPassword(request.POST)
    if not form.is_valid():
        errors = [v.as_text() for k, v in form.errors.items()]
        context['errors'].extend(errors)
        context['form'] = ChangePasswordForm()
        return render(request, 'change_password.html', context)
    else:
        password = form.cleaned_data['password']
        request.user.set_password(password)
        request.user.save()
        return redirect('/')


def map(request):
    return render(request, 'map.html')


def load_city(request, city):
    context = {}
    features = []
    neighbors = Neighbor.objects.filter(city=city)
    for neighbor in neighbors:
        features.append(neighbor.geom.json)

    features = features[0: -1]
    context['type'] = 'FeatureCollection'
    context['features'] = features

    return JsonResponse(context)

