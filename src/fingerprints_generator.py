# youtube_dl dependencies
from __future__ import unicode_literals
import youtube_dl
import ffmpeg
import os

# spectrogram dependencies
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.io import wavfile
from scipy import signal
import numpy as np
from pydub import AudioSegment
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (binary_erosion,
                                      generate_binary_structure,
                                      iterate_structure)

# hash dependencies
import hashlib
from operator import itemgetter
from typing import List, Tuple

# bdd dependecies
import asyncpg
import asyncio
import sys


def download_ytb(url, time_start=None, time_end=None):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192', }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', None)

    sound = AudioSegment.from_wav(video_title + '.wav')
    sound = sound.set_channels(1)
    if time_start is not None and time_end is not None:
        t1 = time_start * 1000  # Works in milliseconds
        t2 = time_end * 1000
        if (0 <= t1 < len(sound)) and (t1 < t2 <= len(sound) and t2 > 0):
            sound = sound[t1:t2]
        else:
            print("Timecode mauvais, veuillez saisir des temps en secondes corrects")
    sound.export(video_title + '.wav', format="wav")

    return video_title + '.wav'


def spectrogram_and_peaks(file_path, show_spectrogram=False):
    sample_rate, samples = wavfile.read(file_path)

    arr2D = mlab.specgram(
        samples,
        NFFT=4096,
        Fs=44100,
        window=mlab.window_hanning,
        noverlap=(4096 * 0.5))[0]

    arr2D = 10 * np.log10(arr2D, out=np.zeros_like(arr2D), where=(arr2D != 0))

    # Créé une structure binaire de dimension 2 avec un connectivité de 2, en gros tous les éléments sont connectés à
    # l'élément central
    struct = generate_binary_structure(2, 2)

    # On reproduit la structure mais en l'ittérant 10 fois
    neighborhood = iterate_structure(struct, 10)

    # find local maxima using our filter mask
    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D

    # Applying erosion, the dejavu documentation does not talk about this step.
    background = (arr2D == 0)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    # Boolean mask of arr2D with True at peaks (applying XOR on both matrices).
    detected_peaks = local_max != eroded_background

    # extract peaks
    amps = arr2D[detected_peaks]
    freqs, times = np.where(detected_peaks)

    # filter peaks
    # flattern retourne l'array 2D en 1D
    amps = amps.flatten()

    # get indices for frequency and time
    filter_idxs = np.where(amps > 10)

    freqs_filter = freqs[filter_idxs]
    times_filter = times[filter_idxs]

    local_maxima = list(zip(freqs_filter, times_filter))

    if (show_spectrogram):
        fig, ax = plt.subplots()
        ax.imshow(arr2D)
        ax.scatter(times_filter, freqs_filter)
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        ax.set_title("Spectrogram")
        plt.gca().invert_yaxis()
        plt.show()

    os.remove(file_path)

    return generate_hashes(local_maxima, 10)


def generate_hashes(peaks: List[Tuple[int, int]], fan_value: int = 5) -> List[Tuple[str, int]]:
    # frequencies are in the first position of the tuples
    idx_freq = 0
    # times are in the second position of the tuples
    idx_time = 1

    peaks.sort(key=itemgetter(1))

    hashes = []
    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):

                freq1 = peaks[i][idx_freq]
                freq2 = peaks[i + j][idx_freq]
                t1 = peaks[i][idx_time]
                t2 = peaks[i + j][idx_time]
                t_delta = t2 - t1
                if 0 <= t_delta <= 200:
                    h = hashlib.sha1(f"{str(freq1)}|{str(freq2)}|{str(t_delta)}".encode('utf-8'))
                    hashes.append((h.hexdigest()[0:20], t1))

    return hashes


file = download_ytb("https://www.youtube.com/watch?v=5Psm7n4nhwk", 0, 6)

hashes = spectrogram_and_peaks(file)


async def create():
    conn = await asyncpg.connect(user='postgres', password='MusiFetch',
                                 database='MusiFetch', port="5432", host="db")

    music = await conn.fetchrow("SELECT * FROM music WHERE titre = $1", file)
    if music is None:
        new_music = await conn.execute("INSERT INTO music (titre) VALUES($1)", file)

        last_id = await conn.fetchval("SELECT id FROM music order by id DESC LIMIT 1")

        print(last_id)
        for hashe in hashes:
            value = await conn.execute("INSERT INTO fingerprints(hashe,id_music) VALUES($1,$2)", hashe[0], last_id)
    else:
        print("this music already exist in database")
    await conn.close()


async def find():
    conn = await asyncpg.connect(user='postgres', password='MusiFetch',
                                 database='MusiFetch', port="5432", host="db")
    occurs = 0
    print(len(hashes))
    for hashe in hashes:
        founds = await conn.fetchrow("SELECT id_music FROM fingerprints WHERE hashe = $1", hashe[0])
        if founds is not None:
            occurs += 1
    print(occurs)


loop = asyncio.get_event_loop()
if sys.argv[1] == "create":
    loop.run_until_complete(create())
elif sys.argv[1] == "find":
    loop.run_until_complete(find())
