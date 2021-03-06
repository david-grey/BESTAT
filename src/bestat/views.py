import datetime
import json
import random
import queue
import os
import subprocess

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
        emailto.delay("Welcome to bestat", email_body, user.email)
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
                        emailto.delay("Verification email from bestat",
                                      email_body, u.email)
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
    if request.is_ajax():

        return JsonResponse(res)
    else:
        image_data = open("bestat/" + res['link'], "rb").read()
        return HttpResponse(image_data, content_type="image/png")


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
    if request.method == 'GET' or not request.is_ajax():
        return render(request, 'blank.html', {'msg': 'illegal request'})

    review_form = ReviewForm(request.POST)

    if review_form.is_valid():
        neighbor_id = review_form.cleaned_data.get('neighbor_id')
        review = Review.objects.create(
            block=NeighborInfo.objects.get(
                neighbor=Neighbor.objects.get(regionid=neighbor_id)),
            author=request.user,
            text=review_form.cleaned_data.get('text'),
            safety=review_form.cleaned_data.get('safety'),
            convenience=review_form.cleaned_data.get('convenience'),
            public_service=review_form.cleaned_data.get('public'),
            create_time=datetime.datetime.now()
        )

        review.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'err', 'err': 'invalid review'})


def map(request):
    return render(request, 'map.html')


def get_preference(request):
    weights = default_weights.copy()
    crime_weight = weights['crime']
    del weights['crime']

    if not is_anonymous(request):
        crime_weight = request.user.preference.crime
        pref = request.user.preference
        for k in weights:
            weights[k] = getattr(pref, k, 5.)

    crime_weight = my_sigmoid(crime_weight, (8, 2)) * 2
    mean = np.asarray(list(weights.values())).mean()
    for k in weights:
        weights[k] /= mean
    return weights, crime_weight


def load_city(request, city):
    context = {}
    map_data = {}
    recommendation = []
    features = []
    neighbors = Neighbor.objects.filter(city=city)
    weights, crime_weight = get_preference(request)

    que = queue.PriorityQueue()

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

        # Priorityqueue
        que.put(BlockScore(neighbor.regionid, neighbor.name, overall))
        if que.qsize() > 3:
            que.get()

    map_data['type'] = 'FeatureCollection'
    map_data['features'] = features

    while not que.empty():
        recommendation.append(que.get().as_dict())

    context['map_data'] = map_data
    context['recommendation'] = recommendation

    return JsonResponse(context)


@require_http_methods(['GET'])
def get_city(request):
    city = request.GET.get('name', '')
    cityob = City.objects.filter(name=city)
    if len(cityob) == 0:
        return render(request, 'blank.html', {'msg': 'It is not a valid city!'})
    try:

        cityob = cityob.filter(activate=1)[0]
    except:
        return render(request, 'blank.html',
                      {'msg': 'We are moving to this city soon!'})
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
    try:
        neighbor = Neighbor.objects.get(regionid=neighbor_id)
        if neighbor is None:
            return render(request, 'blank.html',
                          {'msg': 'This neighbor does not exist!'})
        return render(request, 'detail.html',
                      {'neighbor_id': neighbor_id, 'neighbor': neighbor.name,
                       'city': neighbor.city})
    except Neighbor.DoesNotExist:
        return render(request, 'blank.html', {'msg': 'Neighbor non exist!'})


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
    pref = Preference.objects.get(user=request.user)

    if request.method == 'GET':
        return JsonResponse(pref.as_dict())
    else:
        form = PreferenceForm(request.POST, instance=pref)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        return JsonResponse(Preference.objects.get(user=request.user).as_dict())


def cities(request):
    if request.method != 'GET':
        return Http404
    rank = request.GET.get("rank")
    context = {}
    citiall = City.objects.all()
    citi = []
    income = {'Washington', 'Boston', 'San Jose', 'San Francisco', 'Honolulu',
              'Seattle', 'Minneapolis', 'Denver',
              'Portland', 'Sarasota', 'Anchorage'}
    happy = set()
    if rank == "population":
        citi = citiall.order_by("-population")[:20]
    elif rank == "income":
        for c in citiall:
            if c.name in income:
                citi.append(c)
            if len(citi) == len(income):
                break
    elif rank == "happiness":
        for c in citiall:
            if c.name in happy:
                citi.append(c)
            if len(citi) == len(happy):
                break
    else:
        ran = random.sample(range(1, len(citiall)), 10)
        for i in ran:
            citi.append(citiall[i])
    context['cities'] = citi
    return render(request, "cities.html", context)


def neighbors(request):
    if request.method != 'GET':
        return Http404
    rank = request.GET.get("rank")
    nis_all = NeighborInfo.objects.all()
    nis = []
    if rank == "top":
        nis = nis_all[:10]
    else:
        ran = random.sample(range(1, len(nis_all)), 10)
        for i in ran:
            nis.append(nis_all[i])
    context = {"nis": nis}
    return render(request, "neighbors.html", context)


def get_city_pic(request):
    city = request.GET.get('city')

    gp = Picture("AIzaSyAQi5ECDVGwZ6jpPShEjL1GbLZBvDlee8c")
    res = gp.find_picture(city)
    if res == "/static/img/region/NA.png":
        return HttpResponse()
    image_data = open("bestat/" + res, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


@require_http_methods(['GET', 'POST'])
@anonymous_only("you've already login")
def forget_password(request):
    context = {}
    if request.method == 'GET':
        context['form'] = ForgetPasswordForm()
        return render(request, 'forget_password.html', context)

    else:
        form = ForgetPasswordForm(request.POST)
        if not form.is_valid():
            context['form'] = form
            render(request, 'forget_password.html', context)
        username = form.cleaned_data['username']
        user = User.objects.get(username=username)
        generator = PasswordResetTokenGenerator()
        token = generator.make_token(user)

        email_body = '''
        Please click the link below to reset your password. http://%s%s
           ''' % (request.get_host(),
                  reverse('bestat:reset', args=(user.username, token)))
        emailto.delay("Reset your password", email_body, user.email)
        context[
            'msg'] = 'Your password reset link has been send to your register' \
                     ' email %s.' % user.email
        return render(request, 'blank.html', context)


@require_GET
def reset_password_check(request, user_id, token):
    generator = PasswordResetTokenGenerator()
    try:
        user = User.objects.get(username=user_id)
        if generator.check_token(user, token):
            login(request, user)
            return render(request, 'reset_password.html',
                          {'form': ResetPasswordForm()})

    except User.DoesNotExist:
        return render(request, 'blank.html', {'msg': 'user non exist!'})


@require_POST
def reset_password(request):
    context = {'errors': []}

    form = ResetPasswordForm(request.POST)
    if not form.is_valid():
        errors = [v.as_text() for k, v in form.errors.items()]
        context['errors'].extend(errors)
        context['form'] = ResetPasswordForm()
        return render(request, 'reset_password.html', context)
    else:
        password = form.cleaned_data['password']
        request.user.set_password(password)
        request.user.save()
        return redirect(reverse('bestat:signin'))


def build(request):
    if request.method != 'GET':
        return HttpResponse("illegal")
    key = request.GET.get("key")
    if key == "buildbestatDavid":
        output = subprocess.Popen(['sh', '/home/liuziqicmu/auto_deploy.sh'])
        return HttpResponse("success")
    else:
        return HttpResponse("illegal")


class BlockScore:
    def __init__(self, nid, name, score):
        self.id = nid
        self.name = name
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
