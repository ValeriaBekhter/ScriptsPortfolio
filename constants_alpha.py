# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 15:42:27 2020

@author: bekhter
"""


# my exp.constants:

# screen: 2880 x 1800
DISPSIZE = (1536, 864) # w x h

FGC = (0, 0, 1) # foreground colour
# BGC = (-1, -1, -1) # backgr colour (black)
BGC = (-0.75, -0.75, -0.75) # backgr colour (black)


EMO = ['neutral', 'pleasant', 'unpleasant']
FREQS = [15, 20]
SWITCH15=[34, 40] # IN 15 HZ CYCLES, switchtime at 2200 and 2600 ms
SWITCH20=[45, 53] # IN 20 HZ CYCLES, switchtime at 2200 and 2600 ms
# in 17 Hz and 21.25 Hz cycles:
    
# SWITCH15=[25, 31] # IN 15 HZ CYCLES, switchtime at 1600 and 2000 ms
# SWITCH20=[33, 41] # IN 20 HZ CYCLES, switchtime at 1600 and 2000 ms

TRIALREPEATS = 20 # better make 25, to come down to 200 trials
# in case I decide to go with 3 valence conds and 20 Hz freq, I get 60 or 80 pics per cond, and 180 or 240 trials respectively

ALPHATIME = 2.0 # 2 sec

#FIXTIME = 2 # wait 2 seconds for response for valence/arousal/ present the SAM rating for that long?


LOGFILENAME = input('Participant name: ') # instead of "raw_input"
SESSIONFILE = input('Session name: ')
LOGFILE = LOGFILENAME + '_' + SESSIONFILE


## commments related to the scientific content:
# stimfreqs:
# 20 Hz will have 3 frames in 60Hz resfresh
# 15 Hz will have 4 frames in 60Hz refresh  

# 85Hz refresh:
# 14.167 Hz ( 1000/70.58823529411765) and 17 Hz (1000/58.8235294117647 --> 6 frames of 85Hz)
# 21.25 Hz (1000/47.05882352941177) 

# 17 and 21.25 Hz
# or
# 15 and 20 Hz

# 17.5 and 14 Hz with 70Hz refresh
# 12 and 15 Hz with 60 Hz refresh
# 15 and 20 with 120 Hz refresh (Petro, 2019)

# Seven seconds from image onset, the visual rating
# scales of valence and arousal were presented using the Self-
# Assessment Manikin (SAM; Lang, 1980). After the ratings, a
# blank interval lasting between 2 and 3 s was presented (intertrial
# interval, ITI). Codispoti et al. 2012

# Campagnoli, 2019:
# 