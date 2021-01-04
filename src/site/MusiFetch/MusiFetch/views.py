from django.shortcuts import render
import sys

sys.path.append("..")  # Adds higher directory to python modules path.

from fingerprints import fingerprints_generator


def find(request):
    if request.method == 'POST':
        ytb_link = request.POST['video_link']

        algo = fingerprints_generator.Algo("find", ytb_link)

        print(algo.occurences)

        return render(request, 'home/find.html', {'ytblink': ytb_link})

    return render(request, 'home/index.html')
