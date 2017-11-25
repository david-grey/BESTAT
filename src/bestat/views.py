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
from bestat.models import Profile, Review, NeighborInfo, Neighbor, City, CrimeRecord
from bestat.decorator import check_anonymous, login_required, anonymous_only
from bestat.forms import UserCreationForm, LoginForm, ChangePasswordForm, \
    ProfileForm, UsernameForm, ResetPassword
from bestat.utils import is_anonymous
from django.http import JsonResponse, Http404
import datetime
import json
import random
from bestat.ranking import get_neighbor_score
from django.utils.html import escape
from bestat.tasks import test,emailto

@check_anonymous
@require_GET
def home(request):
    test.delay("aaaa")
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
        user.is_active = False
        user.save()
        profile = Profile.objects.create(user=user,
                                         nick_name=params['nick_name'])
        profile.save()
        token = default_token_generator.make_token(user)

        email_body = '''
           Welcome to bestat. Please click the link below to verify your email address and complete the registration proceess. http://%s%s
           ''' % (request.get_host(),
                  reverse('bestat:confirm', args=(user.username, token)))
        emailto.delay(email_body,user.email)
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
        context['form'] = form
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
                print('login success')
                login(request, user)
                return redirect('/')

            else:
                print('flag1')
                errors = ['password incorrect']
                try:
                    u = User.objects.get(username=username)
                    if not u.is_active:
                        token = default_token_generator.make_token(u)
                        email_body = '''
                           Welcome to bestat. Please click the link below to verify your email address and complete the registration proceess. http://%s%s
                           ''' % (request.get_host(),
                                  reverse('bestat:confirm', args=(u.username, token)))
                        emailto.delay(email_body, u.email)
                        errors = ['User not activated. A new email has been sent to you.']
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

    try:
        user = User.objects.get(username=username)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
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
    neighbor_id = request.POST['neighbor_id']

    review = Review.objects.create(
        block=NeighborInfo.objects.get(neighbor=Neighbor.objects.get(regionid=neighbor_id)),
        author=user,
        text=request.POST['text'],
        safety=request.POST['safety'],
        convenience=request.POST['convenience'],
        public_service=request.POST['public'],
        create_time=datetime.datetime.now()
    )
    review.save()

    return render(request, 'detail.html')




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
        context['msg'] = 'Your password reset link has been send to your register email.'
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
        cityob = City.objects.filter(name=city)[0]
    except:
        return render(request, 'blank.html', {'msg': 'City not exist!'})
    coordinate = json.loads(cityob.point.geojson)[
                     'coordinates'][::-1]
    return render(request, 'map.html', {"city": city, "coordinate": coordinate})


def get_all_city(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        results = [c.name for c in City.objects.filter(activate=1).filter(name__icontains=q)[:5]]
        data = json.dumps(results)
    else:
        data = "No"
    return HttpResponse(data, "application/json")


def detail(request, neighbor_id):
    return render(request, 'detail.html', {'neighbor_id': neighbor_id})


def get_neighbor_detail(request, neighbor_id):
    if request.is_ajax():
        neighbor = Neighbor.objects.get(regionid=neighbor_id)
        overall, public_service, live_convenience, security_score = get_neighbor_score(
            neighbor)

        context = {}
        context['neighbor_name'] = neighbor.name
        context['overview_score'] = round(overall, 2)
        context['security_score'] = round(security_score, 2)
        context['public_service'] = round(public_service, 2)
        context['live_convenience'] = round(live_convenience, 2)

        return JsonResponse(context)


def get_reviews(request, neighbor_id):
    if request.is_ajax():
        neighbor = Neighbor.objects.get(regionid=neighbor_id)
        reviews = Review.objects.filter(block=NeighborInfo.objects.get(neighbor=neighbor)).order_by("-create_time")

        reviews_html = ""
        for review in reviews:
            s = ('<div class="row"><div class="col-sm-3 review-title">'
                 '<img src="https://thesocietypages.org/socimages/files/2009/05/nopic_192.gif" class="img-rounded" height="70px" width="70px">'
                 '<div class="review-block-name"><a href="#"> %s </a></div>'
                 '<div class="review-block-date"> %s </div></div>'
                 '<div class="col-sm-9 review-content"><div class="review-block-rate">'
                 '<div class="col-md-4">'
                 '<label>Safety: </label>'
                 '<select class="review_safety">'
                 '%s'
                 '</select></div>'
                 '<div class="col-md-4">'
                 '<label>Public Service: </label>'
                 '<select class="review_public">'
                 '%s'
                 '</select></div>'
                 '<div class="col-md-4">'
                 '<label>Convenience: </label>'        
                 '<select class="review_convenience">'
                 '%s'
                 '</select></div></div><hr/>'
                 '<div class="col-md-12 "> %s '
                 '</div></div></div><hr/>') % (review.author.username, review.create_time.strftime('%b %d %Y'),
                                               setStar(review.safety), setStar(review.public_service),
                                               setStar(review.convenience), escape(review.text))

            reviews_html += s

        return JsonResponse({"html": reviews_html})


def setStar(star):
    s = ''
    for i in range(1, 6):
        if i == star:
            s += '<option value="' + str(i) + '" selected>' + str(i) + '</option>'
        else:
            s += '<option value="' + str(i) + '">' + str(i) + '</option>'

    return s

