#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 21:34:07 2017

@author: carlos
"""

from moviepy.editor import *
import numpy as np
from threading import Thread
from threading import Lock

class video_cutter (Thread):         
    def __init__(self, filename, magnitude, period):
        Thread.__init__(self)
        self.clip = VideoFileClip(filename)
        
        # extract audio
        self.audio = self.clip.audio.to_soundarray()
        
        # join channels  and normalize
        self.join_audio = abs(self.audio).sum(axis=1)/self.clip.audio.nchannels
        self.max_vol = self.join_audio.max()
        
        periodThresholds = [2, 5, 10]
        magnitudeThresholds = [0.1, 0.2, 0.3]
        
        self.minTime = periodThresholds[period]
        self.volThreshold = magnitudeThresholds[magnitude]
        
        self.cut_filename = filename
        self.finished = False
        self.state = 'init'
        self.sent = False
        
        self.mutex = Lock()
    
    def run(self):
        cuts = list()
        growing = False
        
        self.mutex.acquire(1)
        self.state = 'analyzing'
        self.mutex.release()
        
        for i in range(self.audio.shape[0]):
            if self.join_audio[i] < self.volThreshold*self.max_vol:
                if growing:
                    end = i
                else:
                    growing = True
                    start = i
            else:
                if growing and end-start > self.clip.audio.fps * self.minTime:
                    cuts.append([start, end])
                    
                growing = False
                
        self.mutex.acquire(1)
        self.state = 'converting'
        self.mutex.release()
                
        inactiveTimes = 1.0*np.array(cuts)/self.clip.audio.fps
        
        if inactiveTimes.size > 0:
            activeTimes = np.roll(np.concatenate((inactiveTimes, 
                                    np.array([[self.clip.duration, 0]])), 
                                axis=0), 1)
            
            listOfClips = list()
            for i in range(activeTimes.shape[0]):
                listOfClips.append(self.clip.subclip(activeTimes[i,0], 
                                                     activeTimes[i,1]))
            
            final_clip = concatenate_videoclips(listOfClips)
        
            #filename.rpartition('/')[-1] = 
            cut_filename = self.cut_filename+"_cut.mp4"
            
            final_clip.write_videofile(cut_filename)
            self.cut_filename = cut_filename
            
        self.mutex.acquire(1)
        self.state = 'finished'
        self.mutex.release()
        
        self.finished = True
            
    def get_cut_filename():
        return self.cut_filename
    
