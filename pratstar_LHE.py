#!/usr/bin/env python

#IMPORTS
import matplotlib.patches as mpatches
import mmap
import matplotlib.pyplot as plt
import operator
import numpy as np
import argparse

parser = argparse.ArgumentParser(description=".....")
parser.add_argument("-f", "--file", dest="file_name", type=str, required=True, help="LHE File")
parser.add_argument("-n", "--event", dest="event_number", type=int, required=True, help="Event Number")
parser.add_argument("-o", "--output", dest="output", type=str, required=True, help="output file")
args = parser.parse_args()
file = args.file_name
evt_num=args.event_number

#Functions
def max_pt(active):
    pt = 0
    for i in active.values():
        if i[2] > pt:
            pt = i[2]
    return(pt)

def styles(num):
    if num in style.keys():
        return(style[num])
    else:
        return(['???','-','yellow'])

def arcs(theta1,theta2,r,l_theta):
    radius = [r,r]*25
    small = min(theta1,theta2)
    big = max(theta1,theta2)
    if l_theta < big and l_theta > small:
        theta = np.linspace(small,big,50)
    else:
        theta = np.linspace(big - 2*np.pi,small,50)
    return(theta,radius)

def find_decays(ref_data,dex):
    dexs=[]
    cnt = 0
    for i in range(len(ref_data)):
        if ref_data[i][1] == dex:
            dexs.append(cnt)
        cnt+=1
    return(dexs)

def plot_active(active,radius,delta):
    count = 0
    for line in list(active.values()):
        keys = list(active.keys())
        theta = line[1]
        ls  = styles(line[0])
        color = ls[2]
        sty = ls[1]
        text = ls[0]
        plt.polar([theta,theta,],[radius,radius+delta],linewidth = 3,color=color,linestyle=sty)
        if text_dict[keys[count]] == 1:
            plt.text(theta, radius,'$%s$'%text,fontsize=18,bbox=dict(boxstyle="circle",fc=(1, 1, 1)), horizontalalignment='center',verticalalignment='center')
            text_dict[keys[count]] = 0
        count += 1

def add_active(active,dexs,data,mark):
    for i in dexs:
        typ  = 0
        theta = np.arctan2(data[i][4],data[i][3])
        text = 1
        if mark == True:
            active[i+1] = (data[i][0],theta,np.linalg.norm([data[i][3],data[i][4]]))
        if mark ==False:
            active[i+1] = (data[i][0],theta,np.linalg.norm([data[i][3],data[i][4]]))
        text_dict[i+1] = 1
    return(active)

def normalizet(theta):
    if theta < 0:
        theta = theta + 2*np.pi
    return(theta)

def data_splitter(data):
    collision = []
    first_prods = []
    by_prods = []
    for line in data:
        if line[1] == 0:
            collision.append(line)
        elif line[1] == 1:
            first_prods.append(line)
        else:
            by_prods.append(line)
    return(collision,first_prods,by_prods)


#STYLES
style = {}

#quarks
style[1] = ['d','-','blue']
style[2] = ['u','-','blue']
style[3] = ['s','-','blue']
style[4] = ['c','-','blue']
style[5] = ['b','-','blue']
style[6] = ['t','-','blue']
style[7] = ['b\prime','-','blue']
style[8] = ['u\prime','-','blue']
style[-1] = ['\overline{d}','--','blue']
style[-2] = ['\overline{u}','--','blue']
style[-3] = ['\overline{s}','--','blue']
style[-4] = ['\overline{c}','--','blue']
style[-5] = ['\overline{b}','--','blue']
style[-6] = ['\overline{t}','--','blue']
style[-7] = ['\overline{b\prime}','--','blue']
style[-8] = ['\overline{u\prime}','--','blue']

#leptons
style[11] = ['e-','-','green']
style[12] = ['V\ _e','-','green']
style[13] = ['\mu^-','-','green']
style[14] = ['V\ _{\mu}','-','green']
style[15] = ['t\ ^{-}','-','green']
style[16] = ['V\ _t','-','green']
style[17] = ['t\ ^{\prime-}','-','green']
style[18] = ['V\ _{t\prime}','-','green']
style[-11] = ['\overline{e-}','--','green']
style[-12] = ['\overline{V\ _e}','--','green']
style[-13] = ['\overline{\mu^-}','--','green']
style[-14] = ['\overline{V\ _{\mu}}','--','green']
style[-15] = ['\overline{t\ ^{-}}','--','green']
style[-16] = ['\overline{V\ _t}','--','green']
style[-17] = ['\overline{t\ ^{\prime-}}','--','green']
style[-18] = ['\overline{V\ _{t\prime}}','--','green']

#Gauge and Bosons
style[21] = ['g','-','red']
style[22] = ['\gamma','-','red']
style[23] = ['Z^0','-','red']
style[24] = ['W^+','-','red']
style[25] = ['H^0_1','-','red']
style[32] = ['Z^0_2','-','red']
style[33] = ['Z^0_3','-','red']
style[34] = ['W^+_2','-','red']
style[35] = ['H^0_2','-','red']
style[36] = ['H^0_3','-','red']
style[37] = ['H^+','-','red']
style[-21] = ['\overline{g}','--','red']
style[-22] = ['\overline{\gamma}','--','red']
style[-23] = ['\overline{Z^0}','--','red']
style[-24] = ['\overline{W^+}','--','red']
style[-25] = ['\overline{H^0_1}','--','red']
style[-32] = ['\overline{Z^0_2}','--','red']
style[-33] = ['\overline{Z^0_3}','--','red']
style[-34] = ['\overline{W^+_2}','--','red']
style[-35] = ['\overline{H^0_2}','--','red']
style[-36] = ['\overline{H^0_3}','--','red']
style[-37] = ['\overline{H^+}','--','red']
style[6000005] = ['X^{5/3}','--','yellow']
style[-6000005] = ['\overline{X^{5/3}}','--','yellow']




#READ FILE
evt_num=args.event_number
f = open(args.file_name)
s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
s.seek(s.find(b'</init>'))
temp_data = s.read(s.find(b'</LesHouchesEvents>')).split(b'<event')
temp_data = str(temp_data[evt_num].split(b'</event>')[:-1][0]).split('\\n')
#temp_data=temp_data[1:-1]

mark=np.zeros(len(temp_data))
dex = int(4)
count = 0
for i in temp_data:
    if len(i.split()) == len(temp_data[dex].split()):
        mark[count]=1
    count+=1
first = np.where(mark==1)[0][0]-1
second = np.where(mark==1)[0][-1]+1
temp_data = temp_data[first:second]


#Data Organization
data1 = []
part_num = 1
for line in temp_data[1:]:
    relevant = line.split()
    data1.append((int(relevant[0]),int(relevant[2]),int(relevant[3]),float(relevant[6]),float(relevant[7]),part_num))
    part_num += 1
data1.sort(key=operator.itemgetter(2))
data1.sort(key=operator.itemgetter(1))
ref_data = sorted(data1, key=operator.itemgetter(5))
data = data1



data1.sort(key=operator.itemgetter(2))
data1.sort(key=operator.itemgetter(1))
ref_data = sorted(data1, key=operator.itemgetter(5))
data = data1


text_dict = {}

plt.rcParams["figure.figsize"] = [20,20]
plt.rcParams["font.family"] = "Arial"
fig = plt.figure();
ax = fig.add_subplot(111, projection='polar');
plt.setp(ax.yaxis.get_ticklabels(), visible=True);
ax.set_ylim(0,.5)
ax.grid(alpha=.5, color='black')
ax.set_xticklabels([])
ax.set_xticks([])
plt.yticks([.4,.425,.45,.475,.5])
ax.set_yticklabels([])


collision,first_prods,by_prods = data_splitter(data)

delta = .5/(len(by_prods)+1)

active = {}
for particle in first_prods:
    ls = styles(particle[0])
    color = ls[2]
    sty = ls[1]
    text = ls[0]
    theta = normalizet(np.arctan2(particle[4],particle[3]))
    plt.polar([theta,theta],[0,2*delta],color=color,linestyle=sty,linewidth = 3)
    add_active(active,[particle[5]-1],ref_data,True)
    if text_dict[particle[-1]] == 1:
        plt.text(theta, .05,'$%s$'%text,fontsize=18,bbox=dict(boxstyle="circle",fc=(1., 1, 1)),horizontalalignment='center',verticalalignment='center')
        text_dict[particle[-1]] = 0

radius = 2*delta
for i in range(int(len(by_prods)/2)):
    line = by_prods[0]
    ls = styles(line[0])
    text = ls[0]
    a = text
    if line[1] in active.keys():
        l_theta = normalizet(active[line[1]][1])
        del active[line[1]]
        dexs = find_decays(ref_data,line[1])
        theta1 = np.arctan2(ref_data[dexs[0]][4],ref_data[dexs[0]][3])
        theta2 = np.arctan2(ref_data[dexs[1]][4],ref_data[dexs[1]][3])
        circ = arcs(normalizet(theta1),normalizet(theta2),radius,l_theta)
        plt.polar(circ[0],circ[1],linestyle='dashed',color='black')
        add_active(active,dexs,ref_data,True)
        plot_active(active,radius,delta)
        by_prods.pop(0)
        by_prods.pop(0)
    radius = radius+delta

red_patch = mpatches.Patch(color='r', label='Gauge Bosons')
green_patch = mpatches.Patch(color='g', label='Leptons')
c_patch = mpatches.Patch(color='b', label='Quarks')
plt.legend(handles=[red_patch,green_patch,c_patch],loc=4, prop={'size': 24})
plt.title('Event ' + str(evt_num) + ' \n Transverse View',fontsize=30)


plot_active(active,radius,.4-radius)
plt.polar([0,0],'ok',markersize=25)
plt.polar([0,0],'ok',markersize=20,color='yellow')

maxp = max_pt(active)
circle = plt.Circle((0, 0), 0.4, transform=ax.transData._b, color=".8", alpha=0.4)
plt.subplot(111, polar=True).add_artist(circle)
for i in active.values():
    length = i[2]/(10.8*maxp)
    theta = i[1]
    ls = style[i[0]]
    color = ls[2]
    plt.polar([theta,theta],[.407,.4+length],color = color,linewidth=15,alpha =.5 )
plt.savefig(args.output+'/Event_'+str(evt_num)+'.png',dpi=100)
plt.close()
















