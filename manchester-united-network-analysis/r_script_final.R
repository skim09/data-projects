## REPEAT SAME FOR CHELSEA GAME
setwd("/Users/swkim728/Desktop/wesleyan/fall_2018/qac241/final_project")
munnew_firsthalf = read.csv("mufc_nufc_first_half.csv", header = T)
library(igraph)
munnew_firsthalf_passes = munnew_firsthalf[!(munnew_firsthalf$to==0|munnew_firsthalf$to==98),]


mnfh_graph = graph_from_data_frame(munnew_firsthalf_passes, directed = T)
mnfh_adj_matrix = as.matrix(get.adjacency(mnfh_graph))
mnfh_am_graph = graph_from_adjacency_matrix(mnfh_adj_matrix,
                                            mode = "undirected",
                                            weighted = T)
plot(mnfh_am_graph, edge.width = E(mnfh_am_graph)$weight)
E(mnfh_am_graph)$weight

write.graph(graph=mnfh_am_graph, file="mnfh_graph.graphml", format="graphml")

##----secondhalf
munnew_secondhalf = read.csv("mufc_nufc_second_half.csv", header = T)
munnew_secondhalf_passes = munnew_secondhalf[!(munnew_secondhalf$to==0|munnew_secondhalf$to==98|munnew_secondhalf$to==99),]

mnsh_graph = graph_from_data_frame(munnew_secondhalf_passes, directed = F)
mnsh_adj_matrix = as.matrix(get.adjacency(mnsh_graph))
mnsh_am_graph = graph_from_adjacency_matrix(mnsh_adj_matrix,
                                            mode = "undirected",
                                            weighted = T)
plot(mnsh_am_graph, edge.width = E(mnsh_am_graph)$weight)
E(mnsh_am_graph)$weight

write.graph(graph=mnsh_am_graph, file="mnsh_graph.graphml", format="graphml")



##-- node centrality?
fheigen = eigen_centrality(mnfh_am_graph)

sheigen = eigen_centrality(mnsh_am_graph)


##----------TRYING WITH SUBSTITUTES
mvn_ko_raw = read.csv("mn_ko.csv", header = T)
mvn_ko = mvn_ko_raw[!(mvn_ko_raw$to==0|mvn_ko_raw$to==98|mvn_ko_raw$to==99),]
mvn_ko_graph = graph_from_data_frame(mvn_ko, directed = F)
mvn_ko_adj = as.matrix(get.adjacency(mvn_ko_graph))
mvn_ko_adj_g = graph_from_adjacency_matrix(mvn_ko_adj,
                                            mode = "undirected",
                                            weighted = T)
plot(mvn_ko_adj_g, edge.width = E(mvn_ko_adj_g)$weight)
write.graph(graph=mvn_ko_adj_g, file="mvn_ko_cyto.graphml", format="graphml")

## bailly >> mata ----------------------------------------------------------------------------

mvn_mata_raw = read.csv("mn_mata.csv", header = T)
mvn_mata = mvn_mata_raw[!(mvn_mata_raw$to==0|mvn_mata_raw$to==98|mvn_mata_raw$to==99),]
mvn_mata_graph = graph_from_data_frame(mvn_mata, directed = F)
mvn_mata_adj = as.matrix(get.adjacency(mvn_mata_graph))
mvn_mata_adj_g = graph_from_adjacency_matrix(mvn_mata_adj,
                                           mode = "undirected",
                                           weighted = T)
plot(mvn_mata_adj_g, edge.width = E(mvn_mata_adj_g)$weight)
write.graph(graph=mvn_mata_adj_g, file="mvn_mata_cyto.graphml", format="graphml")

## mctominay >> fellaini----------------------------------------------------------------------

mvn_felli_raw = read.csv("mn_fellaini.csv", header = T)
mvn_felli = mvn_felli_raw[!(mvn_felli_raw$to==0|mvn_felli_raw$to==98|mvn_felli_raw$to==99),]
mvn_felli_graph = graph_from_data_frame(mvn_felli, directed = F)
mvn_felli_adj = as.matrix(get.adjacency(mvn_felli_graph))
mvn_felli_adj_g = graph_from_adjacency_matrix(mvn_felli_adj,
                                           mode = "undirected",
                                           weighted = T)
plot(mvn_felli_adj_g, edge.width = E(mvn_felli_adj_g)$weight)
write.graph(graph=mvn_felli_adj_g, file="mvn_felli_cyto.graphml", format="graphml")

## rashford >> alexis ------------------------------------------------------------------------

mvn_alexis_raw = read.csv("mn_alexis.csv", header = T)
mvn_alexis = mvn_alexis_raw[!(mvn_alexis_raw$to==0|mvn_alexis_raw$to==98|mvn_alexis_raw$to==99),]
mvn_alexis_graph = graph_from_data_frame(mvn_alexis, directed = F)
mvn_alexis_adj = as.matrix(get.adjacency(mvn_alexis_graph))
mvn_alexis_adj_g = graph_from_adjacency_matrix(mvn_alexis_adj,
                                           mode = "undirected",
                                           weighted = T)
plot(mvn_alexis_adj_g, edge.width = E(mvn_alexis_adj_g)$weight)
write.graph(graph=mvn_alexis_adj_g, file="mvn_alexis_cyto.graphml", format="graphml")
