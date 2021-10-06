"""
Tutorial Machine Learning Aire
Diciembre 2020.

El guión es como sigue:

1. El origen de los datos está en las centrales de monitoreo del sistema de monitoreo de calidad del aire
    IMG_01
    IMG_02
2. Los datos se recolectan en tablas ordenadas, identificanfo estacion, contaminante, marcas de tiempo
    IMG_03
3. Estos datos puden representarse en una proyección sobre un plano bidimensional, combinando los valores de dos contaminantes (XY, YZ, XZ) 
    ahi se observa que las muestras proóximas forman algunos grupos 'naturales'
    CODE: A imports
    CODE: B scrap data
    CODE: B.1 load data
    CODE: C show data
    CODE: C.1 plot
    IMG_04
4. Con el algoritmo KMEANS aprovechamos este 'agrupamiento natural' y asignamos etiquetas a cada grupo
    luego cada nuevo dato es 'categorizado' en uno de estos patrones y el sistema notifica que está en cierto estado
    CODE: D train and classify data
    CODE: D.1 plot
    IMG_05
5. Este proceso ya se ve en la interfaz normal de aire: a cada muestra se asigna una categoria segun sus valores.
    IMG_06



"""

# A: imports
import time
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# B: scrapping data
db = {}
stations = []
timestamps = []
def load_data_csv(fn='EXTRACT_20201125.06.csv'):
    """create an initial database from csv file"""
    # get 
    ls = [l.strip() for l in open(fn, 'r+').readlines()]
    #create dictionary db[estacion][fecha]=[contams]
    db = {}
    ee = []
    ff = []
    act_contams = {}
    past_sta = ''
    sta = ''
    for i,l in enumerate(ls[1:]):
        ttg, sta, o3, no2, pm25 = l.split(',')
        if (sta != past_sta):
            #append dict to db and create new one
            if (past_sta != ''):
                db[past_sta] = act_contams
                act_contams = {}
            past_sta = sta
            print ('[csv]: \t' + past_sta)
        act_contams[ttg] = [db, stations, timestamps = load_data_csv()
t' + sta)
    # end loop
    ee = list(db.keys())
    ff = list(db[ee[0]].keys())
    print ('[csv]: '+ fn)
    return db, ee, ff
# B.1: load
db, stations, timestamps = load_data_csv()



# C: read and plot data
def read_show():
    db, ee, ff = json.load(open('db_aire.json','r+'))
    datapoints_xy = np.array([np.array([db[ee[0]][f][0], db[ee[0]][f][1]]) for f in ff])
    datapoints_yz = np.array([np.array([db[ee[0]][f][1], db[ee[0]][f][2]]) for f in ff])
    datapoints_xz = np.array([np.array([db[ee[0]][f][0], db[ee[0]][f][2]]) for f in ff])
    # create figure
    fig = plt.figure(figsize=(12, 4))
    fig.subplots_adjust(left=0.04, right=0.98, bottom=0.1, top=0.9)
    colors = ['#4EACC5', '#FF9C34', '#4E9A06']
    # XY
    ax = fig.add_subplot(1, 3, 1)
    ax.plot(datapoints_xy[:,0],datapoints_xy[:,1], 'w', markerfacecolor=colors[0], marker='.')
    ax.set_title('NO2 / O3')
    # YZ
    ax = fig.add_subplot(1, 3, 2)
    ax.plot(datapoints_yz[:,0],datapoints_yz[:,1], 'w', markerfacecolor=colors[1], marker='.')
    ax.set_title('PM25 / NO2')
    # XZ
    ax = fig.add_subplot(1, 3, 3)
    ax.plot(datapoints_xz[:,0],datapoints_xz[:,1], 'w', markerfacecolor=colors[2], marker='.')
    ax.set_title('PM25 / O3')
    plt.show()
# C.1 read
read_show()


# D: classify data
def classify_show():
    db, ee, ff = json.load(open('db_aire.json','r+'))
    datapoints = np.array([np.array([db[ee[0]][f][0], db[ee[0]][f][1], db[ee[0]][f][2]]) for f in ff])
    datapoints_xy = np.array([np.array([db[ee[0]][f][0], db[ee[0]][f][1]]) for f in ff])
    datapoints_yz = np.array([np.array([db[ee[0]][f][1], db[ee[0]][f][2]]) for f in ff])
    datapoints_xz = np.array([np.array([db[ee[0]][f][0], db[ee[0]][f][2]]) for f in ff])
    # classifier
    n_clusts = 5
    k_means = KMeans(init='k-means++', n_clusters=n_clusts, n_init=10)
    k_means.fit(datapoints)
    centers = k_means.cluster_centers_
    labels = k_means.labels_
    # prepare the figure
    fig = plt.figure(figsize=(12, 4))
    fig.subplots_adjust(left=0.04, right=0.98, bottom=0.1, top=0.9)
    colors = ['#1159FF', '#00FF38', '#FFEA12', '#FF7AA0', '#FF2812']
    # color and plot
    ax = fig.add_subplot(1, 3, 1)
    for k, col in zip(range(n_clusts), colors):
        my_members = labels == k
        cluster_center = centers[k]
        ax.plot(datapoints_xy[my_members, 0], datapoints_xy[my_members, 1], 'w', markerfacecolor=col, marker='.')
        ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)
    ax.set_title('NO2 / O3')
    ax = fig.add_subplot(1, 3, 2)
    for k, col in zip(range(n_clusts), colors):
        my_members = labels == k
        cluster_center = centers[k]
        ax.plot(datapoints_yz[my_members, 0], datapoints_yz[my_members, 1], 'w', markerfacecolor=col, marker='.')
        ax.plot(cluster_center[1], cluster_center[2], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)
    ax.set_title('PM25 / NO2')
    ax = fig.add_subplot(1, 3, 3)
    for k, col in zip(range(n_clusts), colors):
        my_members = labels == k
        cluster_center = centers[k]
        ax.plot(datapoints_xz[my_members, 0], datapoints_xz[my_members, 1], 'w', markerfacecolor=col, marker='.')
        ax.plot(cluster_center[0], cluster_center[2], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)
    ax.set_title('PM25 / O3')
    plt.show()
# D.1
classify_show()

