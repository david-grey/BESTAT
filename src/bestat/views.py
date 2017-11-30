import datetime
import json
import random
from mimetypes import guess_type

import numpy as np
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator, \
    PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.html import escape
from django.views.decorators.http import require_http_methods, require_GET, \
    require_POST

from api.picture import Picture
from bestat.decorator import check_anonymous, login_required, anonymous_only
from bestat.forms import *
from bestat.models import *
from bestat.ranking import get_neighbor_score, default_weights, my_sigmoid
from bestat.tasks import emailto
from bestat.utils import is_anonymous


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
        user.is_active = False
        user.save()
        profile = Profile.objects.create(user=user,
                                         nick_name=params['nick_name'])
        profile.save()

        pref = Preference.objects.create(user=user)
        pref.save()

        token = default_token_generator.make_token(user)

        email_body = '''
           Welcome to bestat. Please click the link below to verify your email address and complete the registration proceess. http://%s%s
           ''' % (request.get_host(),
                  reverse('bestat:confirm', args=(user.username, token)))
        emailto.delay(email_body, user.email)
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
                # login success
                print('login success')
                login(request, user)
                return redirect('/')

            else:
                errors = ['password incorrect']
                try:
                    u = User.objects.get(username=username)
                    if not u.is_active:
                        token = default_token_generator.make_token(u)
                        email_body = '''
                           Welcome to bestat. Please click the link below to verify your email address and complete the registration proceess. http://%s%s
                           ''' % (request.get_host(),
                                  reverse('bestat:confirm',
                                          args=(u.username, token)))
                        emailto.delay(email_body, u.email)
                        errors = [
                            'User not activated. A new email has been sent to you.']
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
def get_picture(request):
    neighbor = request.GET['neighbor']
    city = request.GET['city']

    loc = neighbor + " " + city
    gp = Picture("AIzaSyAQi5ECDVGwZ6jpPShEjL1GbLZBvDlee8c")
    res = {"link": gp.find_picture(loc)}
    print(res)
    return JsonResponse(res)


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
        block=NeighborInfo.objects.get(
            neighbor=Neighbor.objects.get(regionid=neighbor_id)),
        author=user,
        text=request.POST['text'],
        safety=request.POST['safety'],
        convenience=request.POST['convenience'],
        public_service=request.POST['public'],
        create_time=datetime.datetime.now()
    )
    review.save()

    return render(request, 'detail.html')


def map(request):
    return render(request, 'map.html')


def get_preference(request):
    weights = default_weights.copy()
    crime_weight = my_sigmoid(weights['crime'], (2, 8)) * 2
    del weights['crime']
    print(request.user.is_anonymous)
    if not is_anonymous(request):
        pref = request.user.preference
        for k in weights:
            weights[k] = getattr(pref, k, 5.)

    mean = np.asarray(list(weights.values())).mean()
    for k in weights:
        weights[k] /= mean
    return weights, crime_weight


def load_city(request, city):
    context = {}
    features = []
    neighbors = Neighbor.objects.filter(city=city)
    weights, crime_weight = get_preference(request)

    for neighbor in neighbors:
        properties = {}
        block = json.loads(neighbor.geom.json)
        properties['id'] = neighbor.regionid
        properties['name'] = neighbor.name
        properties['random'] = random.randint(0, 10)
        overall, public_service, live_convenience, security_score = get_neighbor_score(
            neighbor, weights, crime_weight)
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
        results = [c.name for c in
                   City.objects.filter(activate=1).filter(name__icontains=q)[
                   :5]]
        data = json.dumps(results)
    else:
        data = "No"
    return HttpResponse(data, "application/json")


def detail(request, neighbor_id):
    neighbor = Neighbor.objects.get(regionid=neighbor_id)
    if neighbor is None:
        return render(request, 'blank.html',
                      {'msg': 'This neighbor does not exist!'})
    return render(request, 'detail.html',
                  {'neighbor_id': neighbor_id, 'neighbor': neighbor.name,
                   'city': neighbor.city})


def get_neighbor_detail(request, neighbor_id):
    if request.is_ajax():
        weights, crime_weight = get_preference(request)
        neighbor = Neighbor.objects.get(regionid=neighbor_id)
        overall, public_service, live_convenience, security_score = get_neighbor_score(
            neighbor, weights, crime_weight)

        context = {}
        context['neighbor_name'] = neighbor.name
        context['overview_score'] = round(overall, 2)
        context['security_score'] = round(security_score, 2)
        context['public_service'] = round(public_service, 2)
        context['live_convenience'] = round(live_convenience, 2)

        return JsonResponse(context)


def get_review_detail(request, neighbor_id):
    if request.is_ajax():
        neighbor = Neighbor.objects.get(regionid=neighbor_id)
        ni = NeighborInfo.objects.get(neighbor=neighbor)

        reviews = Review.objects.filter(block=ni)
        context = {"excellent": 1, "good": 1, "ok": 1, "bad": 1, "terrible": 1}
        leng = len(reviews)
        if len == 0:
            return JsonResponse(context)

        for r in reviews:
            score = r.safety + r.public_service + r.convenience
            if score > 12:
                context["excellent"] += 1
            elif score > 9:
                context["good"] += 1
            elif score > 6:
                context["ok"] += 1
            elif score > 3:
                context["bad"] += 1
            else:
                context["terrible"] += 1
        return JsonResponse(context)


def get_reviews(request, neighbor_id):
    if request.is_ajax():
        neighbor = Neighbor.objects.get(regionid=neighbor_id)
        reviews = Review.objects.filter(
            block=NeighborInfo.objects.get(neighbor=neighbor)).order_by(
            "-create_time")

        reviews_html = ""
        for review in reviews:
            s = (
                    '<div class="row">    <div class="col-sm-2 review-title">        <img src="%s" class="img-circle" height="50px" width="50px">        <div class="review-block-name"><a href="#"> %s </a></div>        <div class="review-block-date"> %s</div>    </div>    <div class="col-sm-6 review-content">        <div class="col-md-12 "> %s</div>      </div>    <div class="review-block-rate col-sm-4">        <row class="col-md-12">            <div class="col-md-6">                <label>Safety: </label>            </div>            <div class="col-md-6">                <select class="review_safety">                    %s                </select>            </div>        </row>        <row class="col-md-12">            <div class="col-md-6">                <label>Public Services: </label>            </div>            <div class="col-md-6">                <select class="review_public">                    %s                </select>            </div>        </row>        <row class="col-md-12">            <div class="col-md-6">                <label>Convenience </label>            </div>            <div class="col-md-6">                <select class="review_convenience">                    %s                </select>            </div>        </row>    </div></div><hr/>') % (
                    review.author.profile.img.url, review.author.username,
                    review.create_time.strftime('%b %d %Y'),
                    escape(review.text),
                    setStar(review.safety), setStar(review.public_service),
                    setStar(review.convenience))

            reviews_html += s

        return JsonResponse({"html": reviews_html})


def setStar(star):
    s = ''
    for i in range(1, 6):
        if i == star:
            s += '<option value="' + str(i) + '" selected>' + str(
                i) + '</option>'
        else:
            s += '<option value="' + str(i) + '">' + str(i) + '</option>'

    return s


@login_required("you haven't login!")
def preference(request):
    pref = Preference(user=request.user)

    if request.method == 'GET':
        return JsonResponse(Preference.objects.get(user=request.user).as_dict())
    else:
        form = PreferenceForm(request.POST, instance=pref)
        if not form.is_valid():
            return Http404
        else:
            form.save()
