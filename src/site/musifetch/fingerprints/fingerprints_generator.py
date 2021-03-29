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

#Youtube API dependencies
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse


# hash dependencies
import hashlib
from operator import itemgetter
from typing import List, Tuple

# bdd dependecies
import asyncpg
import asyncio
import sys




class Algo:

    def __init__(self):
        self.occurences = {}
        self.video_title = ""

    def choice(self, choix, url):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        if choix == "create":
            loop.run_until_complete(self.create(self.download_ytb(url)))
        elif choix == "find":
            loop.run_until_complete(self.find(self.download_ytb(url)))
        elif choix == "createPlaylist":
            urls = self.getPlaylistUrls(url)
            for i in range(len(urls)):
                print(""+i+"/"+len(urls)+"")
                loop.run_until_complete(self.create(self.download_ytb(urls[i])))



    def getPlaylistUrls(self,urlPlaylist):
        query = parse_qs(urlparse(urlPlaylist).query, keep_blank_values=True)
        playlist_id = query["list"][0]

        print(f'get all playlist items links from {playlist_id}')
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "AIzaSyDtljM_jIhucfzlYDHcY0Rzkfy95Kn0beU")

        request = youtube.playlistItems().list(
            part = "snippet",
            playlistId = playlist_id,
            maxResults = 50
        )
        response = request.execute()

        playlist_items = []
        while request is not None:
            response = request.execute()
            playlist_items += response["items"]
            request = youtube.playlistItems().list_next(request, response)

        print(f"total: {len(playlist_items)}")
        urls = []
        print([
            f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}' for t in playlist_items
        ])
        urls = [f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}' for t in playlist_items]
        return urls

    def download_ytb(self, url, time_start=None, time_end=None):
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
            self.video_title = info_dict.get('title', None)
        print("video title"+self.video_title)
        invalid = '<>:/"\|?*'
        test = self.video_title
        for char in invalid:
            if (char == "/"):
                test = test.replace(char, '_')
            if (char == '"'):
                test = test.replace(char, "'")
            if (char == "|"):
                test = test.replace(char, "_")
            else:
                test = test.replace(char, '')
        print ("replaced : "+test)
        sound = AudioSegment.from_wav(test + '.wav')
        sound = sound.set_channels(1)
        if time_start is not None and time_end is not None:
            t1 = time_start * 1000  # Works in milliseconds
            t2 = time_end * 1000
            if (0 <= t1 < len(sound)) and (t1 < t2 <= len(sound) and t2 > 0):
                sound = sound[t1:t2]
            else:
                print("Timecode mauvais, veuillez saisir des temps en secondes corrects")
        sound.export(test + '.wav', format="wav")

        return self.spectrogram_and_peaks(test + '.wav')

    def spectrogram_and_peaks(self, file_path, show_spectrogram=False):
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

        if show_spectrogram:
            fig, ax = plt.subplots()
            ax.imshow(arr2D)
            ax.scatter(times_filter, freqs_filter)
            ax.set_xlabel('Time')
            ax.set_ylabel('Frequency')
            ax.set_title("Spectrogram")
            plt.gca().invert_yaxis()
            plt.show()

        os.remove(file_path)

        return self.generate_hashes(local_maxima, 10)

    def generate_hashes(self, peaks: List[Tuple[int, int]], fan_value: int = 5) -> List[Tuple[str, int]]:
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

    async def create(self, hashes):
        conn = await asyncpg.connect(user='postgres', password='MusiFetch',
                                     database='MusiFetch', port="5432", host="db")

        music = await conn.fetchrow("SELECT * FROM music WHERE titre = $1", self.video_title)
        if music is None:
            new_music = await conn.execute("INSERT INTO music (titre) VALUES($1)", self.video_title)
            last_id_music = await conn.fetchval("SELECT id FROM music order by id DESC LIMIT 1")

            last_id_fingerprint = await conn.fetchval("SELECT id FROM fingerprints order by id DESC LIMIT 1")
            if last_id_fingerprint is None:
                last_id_fingerprint = 0

            for i in range(0, len(hashes)):
                hashes[i] = list(hashes[i])
                hashes[i][1] = last_id_music
                last_id_fingerprint += 1
                hashes[i].append(last_id_fingerprint)
                hashes[i] = tuple(hashes[i])

            await conn.copy_records_to_table('fingerprints', records=hashes, columns=('hashe', 'id_music', 'id'))
            await conn.close()

        else:
            return False

        return True

    async def find(self, hashes):
        conn = await asyncpg.connect(user='postgres', password='MusiFetch',
                                     database='MusiFetch', port="5432", host="db")


        last_id_user_buffer = await conn.fetchval("SELECT id_user FROM buffer order by id_user DESC LIMIT 1")
        if last_id_user_buffer is None:
            last_id_user_buffer = 0


        last_id_user_buffer = last_id_user_buffer+1


        for i in range(0, len(hashes)):
            hashes[i] = list(hashes[i])
            hashes[i][1] = last_id_user_buffer
            hashes[i] = tuple(hashes[i])

        await conn.copy_records_to_table('buffer', records=hashes,columns=('hashe','id_user'))
        results = {}
        occuring ={}
        results = await conn.fetch("SELECT COUNT (buffer.hashe) as nb, m.titre ,m.id FROM buffer "
                                   "FULL JOIN fingerprints USING (hashe) "
                                   "inner join music m on m.id = fingerprints.id_music "
                                   "WHERE id_user = $1 AND"
                                   " (buffer.hashe IS NOT NULL "
                                   "OR fingerprints.hashe IS NOT NULL) "
                                   "group by m.id order by nb DESC", last_id_user_buffer)
        await conn.execute("DELETE FROM buffer WHERE id_user = $1",last_id_user_buffer)
        print(results)
        for result in results:
            # print(result['count'])
            # print(result['titre'])
            # print(result['id'])

            occuring[result['id']]={}
            occuring[result['id']]['titre'] = result['titre']
            occuring[result['id']]['count']= result['nb']
        await conn.close()
        self.occurences = occuring
