

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.validators import *
import sys
from fingerprints import fingerprints_generator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .permissions import is_in_group_contributor
from .models import History, Music

import lxml
from lxml import etree
import urllib.request

sys.path.append("..")  # Adds higher directory to python modules path.


# routes


def index(request):
    return render(request, 'home/index.html')


@login_required(login_url="/login/")
def history_view(request):
    user = request.user.id
    history_user = History.objects.filter(id_user=user)
    videos_titles = []
    results = []



    for i in history_user:
        dict = {}
        dict['id_video'] = i.id_video

        youtube_watch_url = 'https://www.youtube.com/watch?v='
        youtube_watch_url += i.id_video
        youtube = etree.HTML(urllib.request.urlopen(youtube_watch_url).read().decode('utf-8'))
        videos_titles.append(youtube.xpath("//title")[0].text) #get xpath using firepath firefox addon
        dict['titre'] = youtube.xpath("//title")[0].text
        results.append(dict)








    return render(request, 'home/historique.twig', {'histories': history_user, 'videos_titles': videos_titles,'results':results})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            return render(request, 'home/login.html', {'error': 'Invalid username or password, please try again'})
    return render(request, 'home/login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        donnees = [email, username, password, confirm_password]
        errors = validatorRegister(donnees)
        if errors == {}:
            try:
                user = User.objects.create_user(username, email, password)
                login(request, user)
                return redirect('/home')
            except:
                html = "<html><body>Erreur inconnue</body></html>"
                return HttpResponse(html)
        else:
            errors['keep_email'] = email
            errors['keep_username'] = username
            return render(request, 'home/register.html', errors)
    return render(request, 'home/register.html')


def logout_view(request):
    logout(request)
    return redirect('/home')


def find(request):
    if request.method == 'POST':

        ytb_link = request.POST['video_link']
        if request.user.is_authenticated:
            user = request.user.id
            id_video = ytb_link.split("=")[1]
            history = History(id_video=id_video, id_user=user)
            history.save()
        try:
            algo = fingerprints_generator.Algo()
            algo.choice("find", ytb_link)

            return render(request, 'home/find.twig', {'ytblink': ytb_link, 'occurences': algo.occurences})
        except:
            pass

    return redirect('/home')


@login_required(login_url="/login/")
@user_passes_test(is_in_group_contributor, login_url='/home/')
def create(request):
    if request.method == 'GET':
        return render(request, 'home/create.twig', {})

    if request.method == 'POST':

        type_link = request.POST['typeLink']

        if type_link == "videoLink":
            algo = fingerprints_generator.Algo()
            algo.choice("create", request.POST['link'])
        elif type_link == "playlistLink":
            algo = fingerprints_generator.Algo()
            algo.choice("createPlaylist", request.POST['link'])

    return redirect('/home')


# external functions

def validatorRegister(donnees):
    errors = {}

    # email
    try:
        validate_email(donnees[0])
    except ValidationError:
        errors['email_error'] = 'Please enter a valid email address'

    # username
    if len(donnees[1]) < 4:
        errors['username_error'] = 'Username must contain at least 4 character'
    elif len(donnees[1]) > 16:
        errors['username_error'] = 'Username cannot contain more than 16 character'

    # password
    if len(donnees[2]) < 6:
        errors['password_error'] = 'Password must contain at least 6 character'

    # confirm password
    if donnees[2] != donnees[3]:
        errors['confirm_password_error'] = 'Passwords do not match'

    return errors
