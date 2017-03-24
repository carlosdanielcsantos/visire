#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 21:34:07 2017

@author: carlos
"""

from moviepy.editor import *
import numpy as np

def video_cutter(filename):

    clip = VideoFileClip(filename)
    
    # extract audio
    audio = clip.audio.to_soundarray()
    
    # join channels  and normalize
    join_audio = abs(audio).sum(axis=1)/clip.audio.nchannels
    max_vol = join_audio.max()
    
    minTime = 3.0
    volThreshold = 0.2
    cuts = list()
    growing = False
    
    for i in range(audio.shape[0]):
        if join_audio[i] < volThreshold*max_vol:
            if growing:
                end = i
            else:
                growing = True
                start = i
        else:
            if growing and end-start > clip.audio.fps*minTime:
                cuts.append([start, end])
                
            growing = False
            
    inactiveTimes = 1.0*np.array(cuts)/clip.audio.fps
    
    activeTimes = np.roll(np.concatenate((inactiveTimes, 
                                          np.array([[clip.duration, 0]])), 
                                          axis=0), 1)
        
    listOfClips = list()
    for i in range(activeTimes.shape[0]):
        listOfClips.append(clip.subclip(activeTimes[i,0], activeTimes[i,1]))
        
        
    final_clip = concatenate_videoclips(listOfClips)
    
    #filename.rpartition('/')[-1] = 
    cut_filename = filename+"_cut.mp4"
    
    final_clip.write_videofile(cut_filename)
    
    return cut_filename

