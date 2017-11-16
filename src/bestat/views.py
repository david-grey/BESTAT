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
from bestat.models import Profile, Review, Comment, NeighborInfo, Neighbor, \
    City, CrimeRecord
from bestat.decorator import check_anonymous, login_required, anonymous_only
from bestat.forms import UserCreationForm, LoginForm, ChangePasswordForm, \
    ProfileForm, UsernameForm, ResetPassword
from bestat.utils import is_anonymous
from django.http import JsonResponse, Http404
import datetime
import json
import random
from bestat.ranking import get_neighbor_score


@check_anonymous
@require_GET
def home(request):
    return render(request, 'homepage.html')


@anonymous_only("You have already login!")
@check_anonymous
def signup(request):
    context = {}
    if request.method == "GET":
        context['form'] = UserCreationForm()
        return render(request, 'signup.html', context)
    else:
        form = UserCreationForm(request.POST)
        context['form'] = form

        if not form.is_valid():
            errors = [v.as_text() for k, v in form.errors.items()]
            context['errors'] = errors
            return render(request, 'signup.html', context)

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

        login(request, user)

        email_body = '''
           Welcome to bestat. Please click the link below to verify your email address and complete the registration proceess. http://%s%s
           ''' % (request.get_host(),
                  reverse('bestat:confirm', args=(user.username, token)))
        send_mail(subject="Verify your email address",
                  message=email_body,
                  from_email="ziqil1@andrew.cmu.edu",
                  recipient_list=[user.email])
        context[
            'msg'] = 'Your confirmation link has been send to your register email.'
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

    return render(request, 'signin.html', context=context)


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
    review.save()
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
        return render(request, 'blank.html', {'msg': 'user not exist!'})


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
    city_obj = City.objects.filter(name=city)

    for neighbor in neighbors:
        properties = {}
        block = json.loads(neighbor.geom.json)
        properties['id'] = neighbor.regionid
        properties['name'] = neighbor.name
        properties['random'] = random.randint(0, 10)
        overall, public_service, live_convenience, security_score = get_neighbor_score(
            neighbor)
        # larger, better, [0,10]
        properties['overview_score'] = round(overall, 2)
        properties['security_score'] = round(security_score, 2)
        properties['public_service'] = round(public_service, 2)
        properties['live_convenience'] = round(live_convenience, 2)
        block['properties'] = properties
        features.append(block)

    context['type'] = 'FeatureCollection'
    context['features'] = features

    return JsonResponse(context)


@require_http_methods(['GET'])
def get_city(request):
    city = request.GET.get('name', '')
    try:
        cityob = City.objects.get(name=city)
    except:
        return render(request, 'blank.html', {'msg': 'City not exist!'})
    coordinate = json.loads(cityob.point.geojson)[
                     'coordinates'][::-1]
    return render(request, 'map.html', {"city": city, "coordinate": coordinate})


def get_all_city(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        results = [c.name for c in City.objects.filter(name__icontains=q)[:5]]

        data = json.dumps(results)
    else:
        data = "No"
    return HttpResponse(data, "application/json")


def detail(request):
    return render(request, 'detail.html')
