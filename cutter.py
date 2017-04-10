#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 21:34:07 2017

@author: carlos
"""

from moviepy.editor import *
import numpy as np
from threading import Thread
from os import path

class video_cutter (Thread):
    def __init__(self, filename, magnitude, period):
        Thread.__init__(self)
        self.clip = VideoFileClip(filename)

        # extract audio
        self.audio = self.clip.audio.to_soundarray()

        # join channels and normalize
        self.join_audio = abs(self.audio).sum(axis=1)/self.clip.audio.nchannels
        self.join_audio /= self.join_audio.max()

        # pre-defined thresholds
        periodThresholds = [2, 5, 10]
        magnitudeThresholds = [0.1, 0.2, 0.3]

        # choose thresholds
        self.minTime = periodThresholds[period]
        self.volThreshold = magnitudeThresholds[magnitude]

        self.cut_filename = filename
        self.finished = False
        self.state = 'Init'

    def run(self):
        cuts = list()
        growing = False
        self.state = 'Analyzing'

        # check each sample
        for i in range(self.audio.shape[0]):
            # volume is lower than threshold
            if self.join_audio[i] < self.volThreshold:
                # if inside a silent segment
                if growing:
                    # update end position of silent segment
                    end = i
                else:
                    # start new silent segment
                    growing = True
                    start = i
            else:
                # if volume recovered and silent segment length meets threshold
                if growing and end - start > self.clip.audio.fps * self.minTime:
                    # add segment's start and end samples to list
                    cuts.append([start, end])

                growing = False

        # start/end time markers of silent segments
        inactiveTimes = 1.0 * np.array(cuts) / self.clip.audio.fps

        if inactiveTimes.size > 0:
            self.state = 'Cutting'

            # start/end time markers of non-silent segments
            activeTimes = np.roll(np.concatenate((inactiveTimes,
                                    np.array([[self.clip.duration, 0]])),
                                axis=0), 1)

            listOfClips = list()
            for i in range(activeTimes.shape[0]):
                listOfClips.append(self.clip.subclip(activeTimes[i,0],
                                                     activeTimes[i,1]))

            final_clip = concatenate_videoclips(listOfClips)

            fn = path.split(self.cut_filename)
            self.cut_filename = path.join(fn[0],'no_silence_'+fn[1])

            self.state = 'Preparing your video'

            final_clip.write_videofile(self.cut_filename)

        self.state = 'Finished'
        self.finished = True

    def get_cut_filename():
        return self.cut_filename
