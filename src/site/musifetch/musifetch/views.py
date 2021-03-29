from django.shortcuts import render, redirect
import sys

sys.path.append("..")  # Adds higher directory to python modules path.

from fingerprints import fingerprints_generator


def register(request):
    return render(request, 'home/register.html')


def find(request):
    if request.method == 'POST':
        ytb_link = request.POST['video_link']

        try:
            algo = fingerprints_generator.Algo()
            algo.choice("find", ytb_link)

            return render(request, 'home/find.twig', {'ytblink': ytb_link, 'occurences': algo.occurences})
        except:
            pass

    return redirect('/home')


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

        # ytb_link = request.POST['video_link']
        # playlist_link = request.POST['playlist_link']
        # if (ytb_link != ""):
        #     algo = fingerprints_generator.Algo()
        #     algo.choice("create", ytb_link)
        # elif (playlist_link != ""):
        #     algo = fingerprints_generator.Algo()
        #     algo.choice("createPlaylist",playlist_link)
    return redirect('/home')
