#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 12:05:19 2020

@author: valeria
"""

# Experimental stimulation script

from constants_alpha import *
from psychopy.visual import Window, Circle, ImageStim, ShapeStim, TextStim
from psychopy.event import waitKeys
from psychopy.core import wait

import math
import cv2
import os
import glob
import numpy as np
import pandas as pd
import random


disp = Window(size=DISPSIZE, color=BGC, units='pix', fullscr=False) # the actual display command

fixmarkblink=Circle(disp, radius=5, edges=64, \
                lineColor=(1,1,1), fillColor=(1,1,1)) # this works with white col but not black
fixmark = ShapeStim(disp,vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),\
lineWidth=30, closeShape=False, size=2,lineColor="yellow")
        
log = open(LOGFILE + '.tsv', 'w')
header = ['trial','image_scr','image_int', 'scrambled imonset','intact imonset', 'SAM valence onset', 'SAM arousal onset', 'valence rating', 'arousal rating', 'valence RT', 'arousal RT']     
# make all values in the header into strings
line = map(str, header)
# join all string values into one string, separated by tabs (‘\t’)
line = '\t'.join(line)
# add a newline (‘\n’) to the string 
line += '\n' 
# write the header to the log file 
log.write(line) 



# # alpha berger maneauvre instructions:
# alpha_instructions1 = "Welcome!\n\nIn this short pre-experimental session, you'll be asked to sit for a few minutes with your eyes closed before we proceed with the experiment. \ \n\nTo start press any button and then close your eyes!" 
# alpha_text1 = TextStim(disp, text=alpha_instructions1, color=FGC, height=24) 
# # present the instructions
# alpha_text1.draw()
# disp.flip()
# # wait for any old keypress 
# waitKeys(maxWait=float('inf'), keyList=None, timeStamped=True)  # wait for ANY KEY to be pressed 
# alpha_instructions2 = "Please now close your eyes..." 
# alpha_text2 = TextStim(disp, text=alpha_instructions2, color=FGC, height=24) 
# # present the instructions
# alpha_text2.draw()
# disp.flip()
# print ('send marker: close your eyes') # SEND MARKER !!!
# # wait for this long:
# wait(ALPHATIME) # wait for 20 sec  




# define the experimental instructions:
expinstructions = 'Welcome!\n\nIn this experiment, an image will appear at the centre of the screen for a few seconds. Afterwards, you will be asked two questions regarding the shown image. Please press the keys from 1 to 9 to give each image your rating. \ \n\nTo start press any button!' 
# create a new text stimulus 
introtext = TextStim(disp, text=expinstructions, color=FGC, height=24) 
# present the instructions
introtext.draw()
disp.flip()
# wait for any old keypress 
waitKeys(maxWait=float('inf'), keyList=None, timeStamped=True)  # wait for ANY KEY to be pressed 









########### exp. variables: definitions
VPNum=int(LOGFILENAME) # participant's number based on what I have entered!

# load in the piclist (same for all participants):
piclist_total = pd.read_csv("../alphaflick_experiment/piclist.csv", index_col=0)

# create an empty list to contain all unique trials 
alltrials = [] 
# loop through all parameters 
for valence in EMO: # valence gives a content not an index!
    for freq in FREQS: 
        for ii, switch in enumerate(SWITCH15): # in SWITCH15 only won't do here b/c I need indices ii later on! # separate for loop for SWITCH times b/c I want every row separated by a SWITCH time
        # create a unique trial dict 
                if freq==15: 
                    trial = {'valence':valence, 'freq':freq, 'switchtime':SWITCH15[ii]}
                else:
                    trial = {'valence':valence, 'freq':freq, 'switchtime':SWITCH20[ii]}
                # this line below is inside of for ii, switch in enumerate(SWITCH15):
                alltrials.extend(TRIALREPEATS * [trial]) # the actual matrix LIST with all possible trial variations # extend list by appending each time a new trial # 320 trials in total

alltrials_df = pd.DataFrame(alltrials) 
stimplan=pd.concat([piclist_total, alltrials_df], axis=1, ignore_index=True) # combine two files together now



# do the randomisation in the same way for every subject:
np.random.seed(VPNum)

# Do I need any more restrictions on the image/cond order?
stimplan_randomised = stimplan.sample(frac = 1) # randomised order should now be reproducible for each subject
stimplan_randomised.columns=['scrambled','intact','image_id','complexity','description','content','lum_int_blue','lum_int_green','lum_int_red','std_int_blue','std_int_green','std_int_red','lum_scr_blue','lum_scr_green','lum_scr_red','std_scr_blue','std_scr_green','std_scr_red','valence','frequency','switchcycle'] # give the columns proper names!

stimplan_randomised['condition']=0 # create a new col and set all values there to 0
stimplan_randomised['condition'][(stimplan_randomised['valence'] == 'neutral') & (stimplan_randomised['frequency'] == 15)]=1 # using boolean filtering
stimplan_randomised['condition'][(stimplan_randomised['valence'] == 'neutral') & (stimplan_randomised['frequency'] == 20)]=2
stimplan_randomised['condition'][(stimplan_randomised['valence'] == 'unpleasant') & (stimplan_randomised['frequency'] == 15)]=3
stimplan_randomised['condition'][(stimplan_randomised['valence'] == 'unpleasant') & (stimplan_randomised['frequency'] == 20)]=4
stimplan_randomised['condition'][(stimplan_randomised['valence'] == 'pleasant') & (stimplan_randomised['frequency'] == 15)]=5
stimplan_randomised['condition'][(stimplan_randomised['valence'] == 'pleasant') & (stimplan_randomised['frequency'] == 20)]=6

# assign a new index to use later on:
stimplan_randomised.index.name = 'randomised' # name the old index
stimplan_randomised.reset_index(inplace=True) # stimplan_randomised.set_index = range(len(stimplan_randomised))

# write a csv file for each sub with all images from the experimental presentation:  
file=str('../alphaflick_experiment/' + 'imagelist_randomised_sub_' + str(VPNum) + '.csv')
stimplan_randomised.to_csv(file)
   

#############################################################
## Is 20 Hz a good idea b/c of 60 Hz refresh/harmocis or subharmonics??? TWo diff freqs cannot be too much apart I think,
# coz might have diff impact on AROUSAL/ATTENTION/ratings??
# what do we do with the ERP to the image change onset? what if alpha effects are there/contaminated? Is there any chance of fading in/out?
# for 60 refresh, only two options: 15 and 20 Hz
# for 80 refresh, could be : 16 Hz and 20 Hz
# trial length? 4000 ms? Any influence on alpha if many trials have the same valence?
# how do we account for diff.spatial frequency content/picture content across the pic categories? should we stick to 1 emo valence only?
# do we need any other task here? problems with just a passive viewing / eye movements etc.
# do we want to keep scrambled part of the trial in? or no scrambling at all?
# do we need to have 2 freqs tested in one exp (or just a pilot with 2 freqs will do)? With 2 freqs, each image needs to be shown twice! MAybe for
# the actual exp-t we should have unpl and pl conds and just one freq of 20 Hz?
# we have to introduce some task on a fixation? to maintain the gaze? look up how it is done in passive veiwing oaradigms to ensure fixation
#############################################################



BlockLength=40 #
BlockNr=0

# define freqs related stuff:
FramesOn_15Pics=2 # present for 2 frames on and 2 off!
FreqDiv_15Pics=4 # 15 Hz (4 frames of 60 Hz in a 15 hz stim rate)
FramesOn_20Pics=2 # present for 2 frames on and 3 off!
FreqDiv_20Pics=3 # 20 Hz (3 frames of 60 Hz in a 20 hz stim rate)

FramesBefSwitch=0 # make sure it is 0 in the beginning



# BEGIN PRESENTATION:
for i_trial, content in stimplan_randomised.iloc[0:].iterrows(): # !!! use stimplan_randomised ROW indices NOT i_trial   (so it should always be 1 index less)               # here i_trial is an index

    if i_trial==0 and ((i_trial+1) % BlockLength)==1:  #Blockanfang % here we make TrialNr and BlockLength related (cos they are) and display BlockNr once in 40 TrialNr ...
        BlockNr=BlockNr+1
        # # draw onto the offscreen area a title (Training/Block)
        block_instructions = 'Block Nr.{}'.format(BlockNr) # draw a text onto the offscreen area
        inststim = TextStim(disp, text=block_instructions, color=FGC, height=24) 

        inststim.draw()
        disp.flip() # display the offscreen
        waitKeys(maxWait=float('inf'), keyList=None, timeStamped=True)  # wait for ANY KEY to be pressed 
  
        
    elif i_trial != 0 and ((i_trial+1) % BlockLength)==1: # in case the programme  crashed after a few trials and had to be restarted since.
        BlockNr=math.ceil((i_trial+1)/BlockLength) # round up to reflect the current Block number
        
        block_instructions = 'Block Nr.{}'.format(BlockNr) # draw a text onto the offscreen area
        inststim = TextStim(disp, text=block_instructions, color=FGC, height=24) 

        inststim.draw()
        disp.flip() # display the offscreen
        waitKeys(maxWait=float('inf'), keyList=None, timeStamped=True)  # wait for ANY KEY to be pressed 
    
    else:
        BlockNr=math.ceil((i_trial+1)/BlockLength) 
   
                        
    #Marker('start') # from now on the program knows, that we start recording and activated the function 'Marker'!!!
    print("this is Trial: ", (i_trial+1), " ","from stimplan row: ", i_trial, "Cond: ", stimplan_randomised.condition[i_trial], "Image: ", stimplan_randomised.image_id[i_trial])
       
    # Do I need some kind of warning befire the trial beginning?
    fixmark.draw() # these commands only work when placed before PreTrialInterval & wait below
    disp.flip()
    # would this suffice?
    PreTrialInterval=650+math.ceil(random.uniform(0,1)*600) # varies from 650 to 1250?
    wait(PreTrialInterval/1000) # convert to sec
    imagescr = ImageStim(disp, image=stimplan_randomised.scrambled[i_trial]) # create an image to present
    imageint = ImageStim(disp, image=stimplan_randomised.intact[i_trial]) # create an image to present
    
    
    for i_FrameNr in range(1,276): # from 1 through to 240 or longer 276 frames
        CycleNrPic15=math.ceil(i_FrameNr/FreqDiv_15Pics) # need to be defined here, otherwise may not exist when I need it at the end of the i_Frame loop...
        CycleNrPic20=math.ceil(i_FrameNr/FreqDiv_20Pics)
        
        if stimplan_randomised.frequency[i_trial]==15: 
            FramesBefSwitch=i_FrameNr-((stimplan_randomised.switchcycle[i_trial]-1)*FreqDiv_15Pics+1)
            #print(FramesBefSwitch)
            # if it's still pre switch period and cycle frame is < 2:
            if CycleNrPic15 < stimplan_randomised.switchcycle[i_trial]:
                if FramesBefSwitch % FreqDiv_15Pics < FramesOn_15Pics:
                    imagescr.draw() # # fill the screen with a scr image

                fixmark.draw() # fill with a cross (regardless of whether the current frame is an on- or off- frame)
                if i_FrameNr==1:
                    scrimonset = disp.flip() # after flipping the frame ends. so make sure it is the very last step in the for-loop
                else:
                    disp.flip()
                    
            else: # if it it's after swtich period but cycle frame is still < 2:   
                if FramesBefSwitch % FreqDiv_15Pics < FramesOn_15Pics:
                    imageint.draw() # fill the screen with a int image
                    
                fixmark.draw() # fill with a cross
                if np.logical_and(CycleNrPic15==stimplan_randomised.switchcycle[i_trial],FramesBefSwitch==0):
                    # IS THIS THE CORRECT PLACE TO LOG THE TIMING?
                    intimonset=disp.flip() # log the time of intact image onset 
                    print(stimplan_randomised.condition[i_trial]) # !!! send Marker for Condition when the frame the Image in switches to Intact
                else:
                    disp.flip()

                
        if stimplan_randomised.frequency[i_trial]==20:
            FramesBefSwitch=i_FrameNr-((stimplan_randomised.switchcycle[i_trial]-1)*FreqDiv_20Pics+1)
            #print(FramesBefSwitch)
            # if it's still pre switch period and cycle frame is < 3:
            if CycleNrPic20 < stimplan_randomised.switchcycle[i_trial]:
                if FramesBefSwitch % FreqDiv_20Pics < FramesOn_20Pics:
                    imagescr.draw() # # fill the screen with a scr image

                fixmark.draw() # fill with a cross
                if i_FrameNr==1:
                    scrimonset = disp.flip() # LOG TIME SOMEHOW ??? IS THIS THE CORRECT PLACE TO DO THAT?
                else:
                    disp.flip()
                    
            else: # if it it's after swtich period but cycle frame is still < 3: 
                if FramesBefSwitch % FreqDiv_20Pics < FramesOn_20Pics:
                   imageint.draw() # fill the screen with a int image
                   
                fixmark.draw()
                if np.logical_and(CycleNrPic20==stimplan_randomised.switchcycle[i_trial], FramesBefSwitch==0):
                    # IS THIS THE CORRECT PLACE TO LOG THE TIMING?
                    intimonset=disp.flip() # log the time of intact image onset 
                    print(stimplan_randomised.condition[i_trial]) # !!! send Marker for Condition when the frame the Image in switches to Intact
                else:
                     disp.flip()
               
                       

    # how do I make the ITI jittered either here or at the beginning of the trial?    
    for FrameNr in range(1,60):  # just a 1000ms blank screen before the instruction for valence/arousal:
        fixmarkblink.draw()  
        disp.flip()
        
    ######## present SAM manikins now:##########
    SAM_valence = ImageStim(disp, image='../SAM/SAM_Valenz.png', size=(600,115))
    SAM_valence.draw() # fill the screen with a int image
    valenceimonset=disp.flip()    
   # wait(SAMDISPLAYTIME) # do I want a fixed dispaly time???  
   
   # wait until response 
    resplist_V = waitKeys(maxWait=float('inf'), keyList=['1','2','3','4','5','6','7','8','9'], \
        timeStamped=True)
    # select the first response from the response list 
    response_V, presstime_V = resplist_V[0] 
    # turn the lowercase response into uppercase 
    response_V = response_V.upper()
    # calculate the reaction time 
    RT_valence = presstime_V - valenceimonset     

    ########
    SAM_arousal = ImageStim(disp, image='../SAM/SAM_Arousal.png', size=(600,115))
    SAM_arousal.draw() # fill the screen with a int image
    arousalimonset=disp.flip()   
    # wait until response 
    resplist_A = waitKeys(maxWait=float('inf'), keyList=['1','2','3','4','5','6','7','8','9'], \
        timeStamped=True)
    # select the first response from the response list 
    response_A, presstime_A = resplist_A[0] 
    # turn the lowercase response into uppercase 
    response_A = response_A.upper()
    # calculate the reaction time 
    RT_arousal = presstime_A - arousalimonset  
    
    # collect all interesting values in a single list 
    # THIS IS HOW EVERY ROW IN THE CSV.FILE IS CREATED:
    # create as many columns in the CSV.FILE as vars below:
    line = [i_trial, stimplan_randomised.scrambled[i_trial], stimplan_randomised.intact[i_trial], scrimonset, intimonset, valenceimonset, arousalimonset, \
                                response_V, response_A, RT_valence, RT_arousal] 
    # turn all values into a string 
    line = map(str, line) 
    # merge all individual values into a single string, separated by tabs 
    line = '\t'.join(line) 
    # add a newline (‘\n’) to the string 
    line += '\n' 
    # write the data string to the log file 
    log.write(line) # write a new line for every trial

    
    if  (i_trial+1) % BlockLength==0:
        print('Block has ended')
        blockend_instructions = 'End of Block Nr.{}'.format(BlockNr)  # draw a text onto the offscreen area
        inststim2 = TextStim(disp, text=blockend_instructions, color=FGC, height=24) 

        inststim2.draw()
        disp.flip() # display the offscreen
        waitKeys(maxWait=float('inf'), keyList=None, timeStamped=True) # why does it not flip without this command?
        
                                                    
# close the log file
log.close() # 1st command outside the for loop (after FOR loop has ended!)
# shut down the experiment  
disp.close() # 1st command outside the for loop (after FOR loop has ended!)
                    