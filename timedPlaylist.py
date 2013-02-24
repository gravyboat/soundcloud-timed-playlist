#!/bin/python
# Author: Forrest
import soundcloud
import random

class timedListen(object):

    # Here we just set up the client data so we can authenticate to the
    # account and access the API.
    def setClientDetails(self, myId, mySecret, myUsername, myPassword):
        self.myId = myId
        self.mySecret = mySecret
        self.myUsername = myUsername
        self.myPassword = myPassword
        client = soundcloud.Client(client_id = self.myId,
                                   client_secret = self.mySecret,
                                   username = self.myUsername,
                                   password = self.myPassword)
        return(client)


    def createPlaylist(self, musicGenre, timer, clientData):
        self.timer = timer
        self.musicGenre = musicGenre
        self.clientData = clientData
        # The time that gets passed through is multiplied by 60000
        # because track times are always in milliseconds, and we need to
        # convert our minutes to milliseconds.
        listenTime = timer * 60000
        trackList = {}
        songIdList = []
        totalTime = 0

        tracks = self.clientData.get('/tracks', genres = self.musicGenre)
        for track_id in tracks:
            trackList[track_id.id] = track_id.duration

        for key, value in trackList.iteritems():
            # Now that we have the track id as the key, and the time as
            # the value, we need to start heading towards our time
            # requirement.
            totalTime += value
            songIdList.append(key)

            # We set the time range to within 180000 in both directions
            # so we have 3 minutes of time to play with, otherwise we
            # might not get anything.
            if totalTime in range(listenTime - 180000, listenTime + 180000):
                print('time request met: ' + str(totalTime / 60000.0))
                break
        random.shuffle(songIdList)
        return(songIdList)

    def uploadPlaylist(self, clientData, songIdList, playlistTitle, shareIt):
        self.clientData = clientData
        self.songIdList = songIdList
        self.playlistTitle = playlistTitle
        self.shareIt = shareIt

        setClient = soundcloud.Client(access_token='https://api.soundcloud.com/oauth2/token')
        theTracks = map(lambda id: dict(id = id), self.songIdList)
        self.clientData.post('/playlists', playlist = {
                    'title': self.playlistTitle,
                    'sharing': self.shareIt,
                    'tracks': theTracks
        })

if __name__ == '__main__':
    timedListenInstance = timedListen()
    clientInstance = timedListenInstance.setClientDetails('YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET', 'YOUR_USERNAME', 'YOUR_PASSWORD')
    songIdListInstance = timedListenInstance.createPlaylist('electronic', 30, clientInstance)
    timedListenInstance.uploadPlaylist(clientInstance, songIdListInstance, 'testPlaylist', 'public')
