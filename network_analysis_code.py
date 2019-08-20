# Final Paper
# Sangwon Kim

import networkx as nx
from geopy import distance
import matplotlib.pyplot as plt
import numpy as np
import operator
import statistics

#####################################################################################################################################################################################
#####################################################################################################################################################################################
#####################################################################################################################################################################################
## Reading in data

G = nx.MultiGraph()

airlines = {}
fh = open('EUAirTransportation_layers.txt')
for line in fh:
    num = int(line.split(" ")[0])
    airline = line.split(" ")[1]
    airline = airline[:-1]
    airlines[num] = airline
fh.close()

airports = {}
center_long = 0
center_lat = 0
fh = open('EUAirTransportation_nodes.txt')
for line in fh:
    num = int(line.split(" ")[0])
    airport = line.split(" ")[1]
    long = float(line.split(" ")[2])
    center_long += long
    lat = float(line.split(" ")[3])
    center_lat += lat
    airports[num] = [airport, long, lat]
fh.close()
center_long = center_long/len(airports)
center_lat = center_lat/len(airports)
center = (center_long, center_lat)
# 94405 Landau an der Isar, Germany

fh = open('EUAirTransportation_multiplex.edges')
for line in fh:
    i = int(line.split(" ")[1])
    j = int(line.split(" ")[2])
    airlinenum = int(line.split(" ")[0])
    G.add_edge(i,j, airline = airlinenum)
fh.close()

## Removing nodes with no data
G.remove_node(259)
G.remove_node(399)

#####################################################################################################################################################################################
#####################################################################################################################################################################################
#####################################################################################################################################################################################
## Looking at the data by layer (airline)

airline_networks = {}

deg_slopes = {}
btwn_slopes = {}
close_slopes = {}

center_city_per_airline = {}

big_airport_distances = []
top_degrees = []

deg_cent_total = nx.degree_centrality(G)
btwn_cent_total = nx.betweenness_centrality(G)
close_cent_total = nx.closeness_centrality(G)

# Going through each airline, calculating the various centralities and distances for each one
# Also finding the airport with the highest centralities in each layer, and then seeing how far they are from the center of europe
# Storing each network and its centralities and distances in a dictionary
for i in range(1, len(airlines)+1):
    SG = nx.Graph( [ (u,v,d) for u,v,d in G.edges(data=True) if d['airline'] == i] )
    deg_cent = nx.degree_centrality(SG)
    btwn_cent = nx.betweenness_centrality(SG)
    close_cent = nx.closeness_centrality(SG)
    distances = {}
    #What is the most central airport?
    total_central_airport_num = list(dict(sorted(iter(deg_cent_total.items()), key=operator.itemgetter(1), reverse=True)[:1]).keys())

    for node in SG.nodes():
        airport_coord = ( airports[int(node)][1], airports[int(node)][2])
        total_central_coord = ( airports[total_central_airport_num[0]][1], airports[total_central_airport_num[0]][2] )
        distances[int(node)] = distance.distance(airport_coord, total_central_coord).km


    x, y = list(distances.values()), list(deg_cent.values())
    plt.scatter(x, y)
    plt.xlabel('Distance')
    plt.ylabel('Degree Centrality')
    plt.title(airlines[i])
    texttosave = airlines[i] + '_degree_v_distance_from_center.pdf'
    save_results_to = '/Users/swkim728/Desktop/wesleyan/spring_2019/COMP360/FINALPAPER/FIGURES/layers/'
    plt.savefig(save_results_to + texttosave)
    plt.clf()

    x, y = list(distances.values()), list(deg_cent.values())
    deg_slopes[airlines[i]] = float(np.polyfit(x, y, 1)[0])

    x, y = list(distances.values()), list(btwn_cent.values())
    btwn_slopes[airlines[i]] = float(np.polyfit(x, y, 1)[0])

    x, y = list(distances.values()), list(close_cent.values())
    close_slopes[airlines[i]] = float(np.polyfit(x, y, 1)[0])

    city_max_deg = list(dict(sorted(iter(deg_cent.items()), key=operator.itemgetter(1), reverse=True)[:1]).keys())
    city_max_btwn = list(dict(sorted(iter(btwn_cent.items()), key=operator.itemgetter(1), reverse=True)[:1]).keys())
    city_max_close = list(dict(sorted(iter(close_cent.items()), key=operator.itemgetter(1), reverse=True)[:1]).keys())
    print(airlines[i])
    print("City with highest degree centrality:", airports[city_max_deg[0]])
    print("City with highest betweenness centrality:", airports[city_max_btwn[0]])
    print("City with highest closeness centrality:", airports[city_max_close[0]])
    print("Distance of (degree) city from center:", distances[city_max_deg[0]], "\n")
    most_central_airport = city_max_deg[0]
    center_city_per_airline[airlines[i]] = most_central_airport
    big_airport_distances.append(distances[most_central_airport])
    top_degrees.append(deg_cent[most_central_airport])

    airline_networks[i] = [SG, deg_cent, btwn_cent, close_cent, distances]


#####################################################################################################################################################################################
## Calculated slope of distance v. centrality, what are the top 3 positive and top 3 negative ones?
save_results_to = '/Users/swkim728/Desktop/wesleyan/spring_2019/COMP360/FINALPAPER/FIGURES/slopes/'

print("\nThe top 3 highest/lowest airlines for distance vs. degree")
top3_deg_airlines =list(dict(sorted(iter(deg_slopes.items()), key=operator.itemgetter(1), reverse=True)[:3]).keys())
bot3_deg_airlines = list(dict(sorted(iter(deg_slopes.items()), key=operator.itemgetter(1), reverse=False)[:3]).keys())
print(top3_deg_airlines, "\n", bot3_deg_airlines, "\n\n")

plt.bar(list(airlines.values()), height = list(deg_slopes.values()))
plt.ylabel('Slope of Distance v. Degree Centrality')
plt.xticks(rotation=45, ha='right')
plt.tick_params(labelsize=6)
plt.subplots_adjust(left=0.12, right=0.95, bottom=0.22, top=0.97, wspace = 0.2, hspace = 0.2)
#plt.show
plt.savefig(save_results_to + 'airlines_degree_slope.pdf')
plt.clf()


print("\nThe top 3 highest/lowest airlines for distance vs. betweenness")
top3_btwn_airlines = list(dict(sorted(iter(btwn_slopes.items()), key=operator.itemgetter(1), reverse=True)[:3]).keys())
bot3_btwn_airlines = list(dict(sorted(iter(btwn_slopes.items()), key=operator.itemgetter(1), reverse=False)[:3]).keys())
print(top3_btwn_airlines, "\n", bot3_btwn_airlines, "\n\n")

plt.bar(list(airlines.values()), height = list(btwn_slopes.values()))
plt.xlabel('Airlines')
plt.ylabel('Slope of Distance v. Betweenness Centrality')
plt.xticks(rotation=45, ha='right')
plt.tick_params(labelsize=6)
plt.subplots_adjust(left=0.12, right=0.95, bottom=0.22, top=0.97, wspace = 0.2, hspace = 0.2)
plt.savefig(save_results_to + 'airlines_betweenness_slope.pdf')
plt.clf()


print("\nThe top 3 highest/lowest airlines for distance vs. closeness")
top3_close_airlines = list(dict(sorted(iter(close_slopes.items()), key=operator.itemgetter(1), reverse=True)[:3]).keys())
bot3_close_airlines = list(dict(sorted(iter(close_slopes.items()), key=operator.itemgetter(1), reverse=False)[:3]).keys())
print(top3_btwn_airlines, "\n", bot3_btwn_airlines, "\n\n")

plt.bar(list(airlines.values()), height = list(close_slopes.values()))
plt.xlabel('Airlines')
plt.ylabel('Slope of Distance v. Closeness Centrality')
plt.xticks(rotation=45, ha='right')
plt.tick_params(labelsize=6)
plt.subplots_adjust(left=0.12, right=0.95, bottom=0.22, top=0.97, wspace = 0.2, hspace = 0.2)
plt.savefig(save_results_to + 'airlines_closeness_slope.pdf')
plt.clf()


## What are the most extreme cities for each airline?
## DEGREE CENTRALITY
top_airline_num = [k for k, v in airlines.items() if v == top3_deg_airlines[0]]
deg_cent = airline_networks[top_airline_num[0]][1]
distances = airline_networks[top_airline_num[0]][4]
top_airport_num = list(dict(sorted(iter(deg_cent.items()), key=operator.itemgetter(1), reverse=True)[:1]).keys())
print("Highest degree centrality:", airports[top_airport_num[0]], "Degree centrality =", deg_cent[top_airport_num[0]], "Distance =", distances[top_airport_num[0]] )


## BETWEENNESS CENTRALITY
top_airline_num = [k for k, v in airlines.items() if v == top3_btwn_airlines[0]]
btwn_cent = airline_networks[top_airline_num[0]][2]
distances = airline_networks[top_airline_num[0]][4]
top_airport_num = list(dict(sorted(iter(btwn_cent.items()), key=operator.itemgetter(1), reverse=True)[:1]).keys())
print("Highest betweenness centrality:", airports[top_airport_num[0]], "Betweenness centrality =", btwn_cent[top_airport_num[0]], "Distance =", distances[top_airport_num[0]] )


## CLOSENESS CENTRALITY
top_airline_num = [k for k, v in airlines.items() if v == top3_close_airlines[0]]
close_cent = airline_networks[top_airline_num[0]][3]
distances = airline_networks[top_airline_num[0]][4]
top_airport_num = list(dict(sorted(iter(close_cent.items()), key=operator.itemgetter(1), reverse=True)[:1]).keys())
print("Highest closeness centrality:", airports[top_airport_num[0]], "Closeness centrality =", close_cent[top_airport_num[0]], "Distance =", distances[top_airport_num[0]]  )


#####################################################################################################################################################################################
#####################################################################################################################################################################################
#####################################################################################################################################################################################



## Now, what about the total graph?


deg_cent = nx.degree_centrality(G)
btwn_cent = nx.betweenness_centrality(G)
close_cent = nx.closeness_centrality(G)

total_central_airport_num = list(dict(sorted(iter(deg_cent.items()), key=operator.itemgetter(1), reverse=True)[:1]).keys())

distances = {}

for node in G.nodes():
    airport_coord = ( airports[int(node)][1], airports[int(node)][2])
    total_central_coord = ( airports[total_central_airport_num[0]][1], airports[total_central_airport_num[0]][2] )
    distances[int(node)] = distance.distance(airport_coord, total_central_coord).km

x, y = list(distances.values()), list(deg_cent.values())
total_deg_slope = float(np.polyfit(x, y, 1)[0])

x, y = list(distances.values()), list(btwn_cent.values())
total_btwn_slope = float(np.polyfit(x, y, 1)[0])

x, y = list(distances.values()), list(close_cent.values())
total_close_slope = float(np.polyfit(x, y, 1)[0])

# Graphing the same bar charts, but this time with the slope for ALL airlines at the end
# Degree
save_results_to = '/Users/swkim728/Desktop/wesleyan/spring_2019/COMP360/FINALPAPER/FIGURES/slopes/'

x, y = list(airlines.values()), list(deg_slopes.values())
x.append('All_Airlines')
y.append(total_deg_slope)
plt.bar(x, height = y)
plt.ylabel('Slope of Distance v. Degree Centrality')
plt.xticks(rotation=45, ha='right')
plt.tick_params(labelsize=6)
plt.savefig(save_results_to + 'airlines_degree_slope+all.pdf')
plt.clf()

#Betweenness
x, y = list(airlines.values()), list(btwn_slopes.values())
x.append('All_Airlines')
y.append(total_btwn_slope)
plt.bar(x, height = y)
plt.ylabel('Slope of Distance v. Betweenness Centrality')
plt.xticks(rotation=45, ha='right')
plt.tick_params(labelsize=6)
plt.savefig(save_results_to + 'airlines_betweenness_slope+all.pdf')
plt.clf()

#Closeness
x, y = list(airlines.values()), list(close_slopes.values())
x.append('All_Airlines')
y.append(total_close_slope)
plt.bar(x, height = y)
plt.ylabel('Slope of Distance v. Closeness Centrality')
plt.xticks(rotation=45, ha='right')
plt.tick_params(labelsize=6)
plt.savefig(save_results_to + 'airlines_closeness_slope+all.pdf')
plt.clf()

save_results_to = '/Users/swkim728/Desktop/wesleyan/spring_2019/COMP360/FINALPAPER/FIGURES/all/'
for centrality in [deg_cent, btwn_cent, close_cent]:
    x, y = list(distances.values()), list(centrality.values())
    plt.scatter(x, y)
    plt.xlabel('Distance from geographic center (km)')
    if centrality == deg_cent:
        plt.ylabel('Degree Centrality')
        plt.savefig(save_results_to + 'all_airlines_degree.pdf')
    if centrality == btwn_cent:
        plt.ylabel('Betweenness Centrality')
        plt.savefig(save_results_to + 'all_airlines_betweenness.pdf')
    if centrality == close_cent:
        plt.ylabel('Closeness Centrality')
        plt.savefig(save_results_to + 'all_airlines_closeness.pdf')
    plt.clf()


## DOING IT FOR NOT CENTER OF GEOGRAPHY BUT HIGHEST DEGREE CENTRALITY
total_central_airport_num = list(dict(sorted(iter(deg_cent.items()), key=operator.itemgetter(1), reverse=True)[:1]).keys())
distances = {}
for node in G.nodes():
    airport_coord = ( airports[int(node)][1], airports[int(node)][2])
    total_central_coord = ( airports[total_central_airport_num[0]][1], airports[total_central_airport_num[0]][2] )
    distances[int(node)] = distance.distance(airport_coord, total_central_coord).km
for centrality in [deg_cent, btwn_cent, close_cent]:
    x, y = list(distances.values()), list(centrality.values())
    plt.scatter(x, y)
    plt.xlabel('Distance from overall most central node (km)')
    if centrality == deg_cent:
        plt.ylabel('Degree Centrality')
        plt.savefig(save_results_to + 'central_airlines_degree.pdf')
    if centrality == btwn_cent:
        plt.ylabel('Betweenness Centrality')
        plt.savefig(save_results_to + 'central_airlines_betweenness.pdf')
    if centrality == close_cent:
        plt.ylabel('Closeness Centrality')
        plt.savefig(save_results_to + 'central_airlines_closeness.pdf')
    plt.clf()



topdistances = list(dict(sorted(iter(distances.items()), key=operator.itemgetter(1), reverse=True)[:3]).keys())



# DEGREE CENTRALITY
top_airport_num = list(dict(sorted(iter(deg_cent.items()), key=operator.itemgetter(1), reverse=True)[:3]).keys())
print("Highest Degree Centrality for total:", airports[top_airport_num[0]], "Degree centrality =", deg_cent[top_airport_num[0]], "Distance =", distances[top_airport_num[0]] )
print("Highest Degree Centrality for total:", airports[top_airport_num[1]], "Degree centrality =", deg_cent[top_airport_num[1]], "Distance =", distances[top_airport_num[1]] )
print("Highest Degree Centrality for total:", airports[top_airport_num[2]], "Degree centrality =", deg_cent[top_airport_num[2]], "Distance =", distances[top_airport_num[2]] )

## BETWEENNESS CENTRALITY
top_airport_num = list(dict(sorted(iter(btwn_cent.items()), key=operator.itemgetter(1), reverse=True)[:3]).keys())
print("Highest Betweenness Centrality for total:", airports[top_airport_num[0]], "Betweenness centrality =", btwn_cent[top_airport_num[0]], "Distance =", distances[top_airport_num[0]])
print("Highest Betweenness Centrality for total:", airports[top_airport_num[1]], "Betweenness centrality =", btwn_cent[top_airport_num[1]], "Distance =", distances[top_airport_num[1]])
print("Highest Betweenness Centrality for total:", airports[top_airport_num[2]], "Betweenness centrality =", btwn_cent[top_airport_num[2]], "Distance =", distances[top_airport_num[2]])

## CLOSENESS CENTRALITY
top_airport_num = list(dict(sorted(iter(close_cent.items()), key=operator.itemgetter(1), reverse=True)[:3]).keys())
print("Highest Closeness Centrality for total:", airports[top_airport_num[0]], "Closeness centrality =", close_cent[top_airport_num[0]], "Distance =", distances[top_airport_num[0]] )
print("Highest Closeness Centrality for total:", airports[top_airport_num[1]], "Closeness centrality =", close_cent[top_airport_num[1]], "Distance =", distances[top_airport_num[1]] )
print("Highest Closeness Centrality for total:", airports[top_airport_num[2]], "Closeness centrality =", close_cent[top_airport_num[2]], "Distance =", distances[top_airport_num[2]] )




#####################################################################################################################################################################################
#####################################################################################################################################################################################
#####################################################################################################################################################################################


## Let's try that again for each layer, but this time compare centrality with the most central node, not the center of all nodes

deg_slopes = {}
btwn_slopes = {}
close_slopes = {}

x_deg = []
y_deg = []
x_btwn = []
y_btwn = []
x_close = []
y_close = []
# Going through each airline, calculating the various centralities and distances for each one
# Also finding the airport with the highest centralities in each layer, and then seeing how far they are from the center of europe
# Storing each network and its centralities and distances in a dictionary
save_results_to = '/Users/swkim728/Desktop/wesleyan/spring_2019/COMP360/FINALPAPER/FIGURES/layers/'
for i in range(1, len(airlines)+1):
    SG = nx.Graph( [ (u,v,d) for u,v,d in G.edges(data=True) if d['airline'] == i] )
    deg_cent = nx.degree_centrality(SG)
    btwn_cent = nx.betweenness_centrality(SG)
    close_cent = nx.closeness_centrality(SG)
    distances = {}
    central_node_num = list(dict(sorted(iter(deg_cent.items()), key=operator.itemgetter(1), reverse=True)[:1]).keys())
    for node in SG.nodes():
        airport_coord = ( airports[int(node)][1], airports[int(node)][2])
        center_coord = ( airports[center_city_per_airline[airlines[i]]][1], airports[center_city_per_airline[airlines[i]]][2])
        top_coord = ( airports[central_node_num[0]][1], airports[central_node_num[0]][2])
        distances[int(node)] = distance.distance(airport_coord, center_coord).km


    x, y = list(distances.values()), list(deg_cent.values())
    deg_slopes[airlines[i]] = float(np.polyfit(x, y, 1)[0])

    x, y = list(distances.values()), list(btwn_cent.values())
    btwn_slopes[airlines[i]] = float(np.polyfit(x, y, 1)[0])

    x, y = list(distances.values()), list(close_cent.values())
    close_slopes[airlines[i]] = float(np.polyfit(x, y, 1)[0])

    x, y = list(distances.values()), list(deg_cent.values())
    plt.scatter(x, y)
    plt.xlabel('Distance')
    plt.ylabel('Degree Centrality')
    plt.title(airlines[i])
    texttosave = airlines[i] + '_degree_v_distance_from_central_node.pdf'
    plt.savefig(save_results_to + texttosave)
    plt.clf()



## TESTTESTTESTTESTTESTTESTTEST
    x, y = list(distances.values()), list(deg_cent.values())
    x_deg = x_deg + x
    y_deg = y_deg + y

    x, y = list(distances.values()), list(btwn_cent.values())
    x_btwn = x_btwn + x
    y_btwn = y_btwn + y

    x, y = list(distances.values()), list(close_cent.values())
    x_close = x_close + x
    y_close = y_close + y


save_results_to = '/Users/swkim728/Desktop/wesleyan/spring_2019/COMP360/FINALPAPER/FIGURES/all/'
plt.scatter(x_deg, y_deg)
plt.xlabel('Distance from airline-respective most central node (km)')
plt.ylabel('Degree Centrality')
plt.savefig(save_results_to + 'combo_airlines_degree')
plt.clf()

plt.scatter(x_btwn, y_btwn)
plt.xlabel('Distance from airline-respective most central node (km)')
plt.ylabel('Between Centrality')
plt.savefig(save_results_to + 'combo_airlines_between')
plt.clf()

plt.scatter(x_close, y_close)
plt.xlabel('Distance from airline-respective most central node (km)')
plt.ylabel('Closeness Centrality')
plt.savefig(save_results_to + 'combo_airlines_close')
plt.clf()






save_results_to = '/Users/swkim728/Desktop/wesleyan/spring_2019/COMP360/FINALPAPER/FIGURES/slopes/'

plt.bar(list(airlines.values()), height = list(deg_slopes.values()))
plt.ylabel('Slope of Distance v. Degree Centrality')
plt.xticks(rotation=45, ha='right')
plt.tick_params(labelsize=6)
plt.savefig(save_results_to + 'airlines_degree_slope_nodecenter.pdf')
plt.clf()


plt.bar(list(airlines.values()), height = list(btwn_slopes.values()))
plt.ylabel('Slope of Distance v. Betweenness Centrality')
plt.xticks(rotation=45, ha='right')
plt.tick_params(labelsize=6)
plt.savefig(save_results_to + 'airlines_betweenness_slope_nodecenter.pdf')
plt.clf()


plt.bar(list(airlines.values()), height = list(close_slopes.values()))
plt.ylabel('Slope of Distance v. Closeness Centrality')
plt.xticks(rotation=45, ha='right')
plt.tick_params(labelsize=6)
plt.savefig(save_results_to + 'airlines_closeness_slope_nodecenter.pdf')
plt.clf()
