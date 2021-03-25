from django.shortcuts import render, redirect
import sys

sys.path.append("..")  # Adds higher directory to python modules path.

from fingerprints import fingerprints_generator


def register(request):
    return render(request, 'home/register.html')


def find(request):
    if request.method == 'POST':
        ytb_link = request.POST['video_link']

        algo = fingerprints_generator.Algo()
        algo.choice("find", ytb_link)

        return render(request, 'home/find.html', {'ytblink': ytb_link, 'occurences': algo.occurences})

    return redirect('/home')


def create(request):

    if request.method == 'GET':

        return render(request, 'home/create.html', {})

    if request.method == 'POST':
        ytb_link = request.POST['video_link']
        algo = fingerprints_generator.Algo()
        algo.choice("create", ytb_link)

    return redirect('/home')
