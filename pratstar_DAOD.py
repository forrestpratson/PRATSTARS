#!/usr/bin/env python

'''
PRATSTAR command line code.
Program used to quickly visualize events in DAOD files.
'''

#Imports:
import argparse
import numpy as np
import uproot
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from operator import itemgetter

#Close out any previous plot that might be open
plt.close()


#Adds Arguments (view,output directory,event number,DAOD file,Show pictures after creation?,Threshold, Add Labels?)
parser = argparse.ArgumentParser(description=".....")
parser.add_argument("-v", "--view", dest="view", type=str, default="Transverse", help="viewing options")
parser.add_argument("-o", "--output", dest="output", type=str, required=True, help="output file")
parser.add_argument("-n", "--event", dest="event_number", type=int, required=True, help="Event Number")
parser.add_argument("-f", "--file", dest="file_name", type=str, required=True, help="DAOD File")
parser.add_argument("-s", "--show", dest="show", type=bool, required=False, default=False, help="Open File after Creation")
parser.add_argument("-c", "--thresh", dest="thresh", type=float, required=False, default=0, help="Threshold PT that will be shown (in MeV)")
parser.add_argument("-l", "--labels", dest="labels_n", type=int, required=False, default=0, help="Label rank vectors by transverse momentum")
args = parser.parse_args()

#Opens File and save location
file = args.file_name
save_loc = args.output
tree = uproot.open(file)["CollectionTree"]

#Pull all neccesary jagged arrays from file
electron_pts = tree["ElectronsAuxDyn.pt"]
electron_etas = tree["ElectronsAuxDyn.eta"]
electron_phis = tree["ElectronsAuxDyn.phi"]

muon_pts = tree["MuonsAuxDyn.pt"]
muon_etas = tree["MuonsAuxDyn.eta"]
muon_phis = tree["MuonsAuxDyn.phi"]

jet_pts = tree["AntiKt4EMTopoJetsAux.pt"]
jet_etas = tree["AntiKt4EMTopoJetsAux.eta"]
jet_phis = tree["AntiKt4EMTopoJetsAux.phi"]
labels = tree[b"EventInfoAux.eventNumber"].array()
runnos = tree[b"EventInfoAux.runNumber"].array()

#Create dictionary that converts event location in file to the event number, and loads which event we are looking at in this run
key = {}
for i in range(len(labels)):
    key[labels[i]] = i
evt_num = args.event_number
if evt_num not in key.keys():
    print("ERROR: Event number not found in file")
event_number = key[evt_num]

view = args.view #Which views will be saved out (transverse or longitudinal)


#Functions
def organize(num): #Takes all relevant data from file, and organizes it into an array (particle type,pt,eta,phi)
    particles = []
    for i in range(len(electron_pts.lazyarray()[num])):
        particles.append(('b',electron_pts.lazyarray()[num][i],electron_etas.lazyarray()[num][i],electron_phis.lazyarray()[num][i]))
    for i in range(len(muon_pts.lazyarray()[num])):
        particles.append(('g',muon_pts.lazyarray()[num][i],muon_etas.lazyarray()[num][i],muon_phis.lazyarray()[num][i]))
    for i in range(len(jet_pts.lazyarray()[num])):
        particles.append(('r',jet_pts.lazyarray()[num][i],jet_etas.lazyarray()[num][i],jet_phis.lazyarray()[num][i]))
    return(particles)


def phi2xy(phi): #Takes phi, and converts it into cartesian unit vectors
    x = np.cos(phi)
    y = np.sin(phi)
    return(x,y)

def maxpt(particles): #Finds the maximum pt for a specific event
    pts = []
    for evt in particles:
        pts.append(evt[1])
    return(np.max(pts))

def plot_array(particles): #Tranverse View: takes necessary information from "particles" required to plot in the transverse view
    plot_data = []
    for event in particles:
        plot_data.append((event[0],event[3],event[1]))
    return(plot_data)

def pt_sum(particles): #Calculates the missing transverse momentum
    px = 0
    py = 0
    for event in particles:
        x,y = phi2xy(event[3])
        px = px + x*event[1]
        py = py + y*event[1]
    pmx = -1*px
    pmy = -1*py
    return(np.arctan2(pmy,pmx))

def eta2xy(eta): #calculates the cartesian z,y unit vectors from eta
    theta = 2*np.arctan(np.exp(-eta))
    z = np.cos(theta)
    y = np.sin(theta)
    return(z/abs(y),y/abs(y))

def plot_array_l(particles): #Longitudinal View: takes necessary information from "particles" required to plot in the Longitudinal view
    plot_data = []
    for event in particles:
        plot_data.append((event[0],event[2],event[1],np.sign(event[3])))
    return(plot_data)


#Plotting Code!
if view != 'Longitudinal': #If view is 'Transverse' or 'Both'
    relevant_data = organize(event_number)
    relevant_data.sort(key=itemgetter(1) , reverse=True) #Sorts the particles based on decscending pt, so that labels are only appplied to top 5
    plot_data = plot_array(relevant_data)
    m = 16.666667*maxpt(relevant_data) #Normalizes the PT bar graph so that it doesnt extend beyond graph's boundries

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar') #Polar corrdinates
    plt.setp(ax.yaxis.get_ticklabels(), visible=True) #Turn off radian labels
    ax.set_ylim(0,.5)
    ax.grid(alpha=.5, color='black')
    ax.set_xticklabels([]) #Turn off theta ticks and labels
    ax.set_xticks([])
    plt.yticks([.4,.43333333,.466667,.5]) #Grid for pt bar graph
    ax.set_yticklabels([])

    #Creates a background in inner graph to diferentiate between vectors and pt bar graph
    circle_background = plt.Circle((0, 0), 0.4, transform=ax.transData._b, color="black", alpha=.075)
    ax.add_artist(circle_background)
   
    #Calculate the missing PT and plot it
    p_miss = pt_sum(relevant_data)
    plt.plot([0,p_miss],[0,.39],color = '.5',linewidth = 5)
    
    
    #Plot each 4 vector in the transverse view and it's pt bar graph component
    dex=0
    for event in plot_data:
        dex=dex+1
        if event[2]/1000 >= args.thresh:
            plt.plot([0,event[1]],[0,.4],color = event[0],linewidth=.8)
            length = event[2]/m + .42
            plt.plot([event[1],event[1]],[.42,length],linewidth = 10, color = event[0],alpha = .5)
            if dex < 6 and args.labels_n==1:
                plt.text(event[1],length+.033333,str(dex))

    #Add a plot title
    plt.title('\n Event ' + str(evt_num) + '\n Transverse View')

    #Add a legend and save out figure to specified location
    red_patch = mpatches.Patch(color='r', label='Jets')
    green_patch = mpatches.Patch(color='g', label='Muons')
    c_patch = mpatches.Patch(color='b', label='Electrons')
    b_patch = mpatches.Patch(color='.5', label='Missing PT')
    plt.legend(handles=[red_patch,green_patch,c_patch,b_patch],loc=4, prop={'size': 6})
    plt.plot(0,0,'ok')
    plt.rcParams["figure.figsize"] = [9,9]

    plt.savefig(save_loc + '/Run_' +str(runnos[event_number]) +'_Event_'+str(evt_num)+'_Transverse',dpi=200)
    if args.show==True:
        os.system("open " + save_loc + '/Run_' +str(runnos[event_number]) +'_Event_'+str(evt_num)+'_Transverse.png')
    plt.close()

#If view == Longitudinal or Both
if view != 'Transverse':
    corrections = 0 #Wierdly the code plots differently if you plot just longitudinal, so corrections must be made to scale
    if view == 'Longitudinal':
        corrections = .04
    relevant_data = organize(event_number)
    relevant_data.sort(key=itemgetter(1) , reverse=True)
    data = plot_array_l(relevant_data)
    m = maxpt(relevant_data)
    plt.clf() #Close out previous plot (incase you chose "both" view)
    fig = plt.figure()
    ax = fig.add_subplot(111) #Create cartesian plot without scale marks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_yticklabels([])

    #Creates the grid for the pt bar graph and draw z-axis (beam)
    plt.plot([-20,20],[0,0], color = '0', linewidth = 1,linestyle = '--')
    plt.plot([-20,20],[1,1], color = '.5')
    plt.plot([-20,20],[-1,-1], color = '.5')
    plt.plot([-20,20],[-1.25,-1.25], color = '.5',linewidth = .5)
    plt.plot([-20,20],[1.25,1.25], color = '.5',linewidth = .5)
    plt.plot([-20,20],[-1.125,-1.125], color = '.5',linewidth = .5)
    plt.plot([-20,20],[1.125,1.125], color = '.5',linewidth = .5)
    plt.plot([-20,20],[-1.375,-1.375], color = '.5',linewidth = .5)
    plt.plot([-20,20],[1.375,1.375], color = '.5',linewidth = .5)

    #Plot each 4 vector and it's pt bar graph
    dex=0
    for event in data:
        dex=dex+1
        if event[2]/1000 >= args.thresh:
            z,y = eta2xy(event[1])
            length = abs(event[2]/(2.635*m)) + 1.08
            plt.plot([0,z],[0,event[-1]*y],color = event[0],linewidth = 1 - corrections)
            plt.plot([z,z],[event[-1]*(1.045 + corrections),event[-1]*(length)],linewidth = 15,color = event[0],alpha = .5)
            if dex < 6 and args.labels_n==1:
                plt.text(z,event[-1]*(length+.1),str(dex))
    plt.plot(0,0,'ok') #add a black dot at the origin (collision point)

    #Create a legend and title
    red_patch = mpatches.Patch(color='r', label='Jets')
    green_patch = mpatches.Patch(color='g', label='Muons')
    c_patch = mpatches.Patch(color='b', label='Electrons')
    plt.legend(handles=[red_patch,green_patch,c_patch],loc=5, prop={'size': 8})
    plt.title('Event ' + str(evt_num) + ' \n Longitudinal View \n')

    #Set relative axis scale and save out the figure
    ax.set_xlim(-4,4)
    ax.set_ylim(-1.5,1.5)
    plt.rcParams["figure.figsize"] = [9,9]
    plt.savefig(save_loc + '/Run_'+str(runnos[event_number])+'_Event_'+str(evt_num)+'_Longitudinal',dpi=200)
    if args.show==True:
        os.system("open " + save_loc + '/Run_'+str(runnos[event_number])+'_Event_'+str(evt_num)+'_Longitudinal.png')
    plt.close()
