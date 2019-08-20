## Loading necessary packages
library(igraph)
library(dplyr)

## Setting working directory, importing data files
setwd("/Users/swkim728/Desktop/wesleyan/fall_2018/qac241/final_project/chelsea_data")
##-----
first_half = read.csv("first_half_data.csv", header = T) %>% filter(!to %in% c(0,98,99))
second_half = read.csv("second_half_data.csv", header = T) %>% filter(!to %in% c(0,98,99))

##creating adjacency matrix
adj_matrix1 = first_half %>% 
  graph_from_data_frame(directed = T) %>%
  get.adjacency() %>%
  as.matrix()
g1 = graph_from_adjacency_matrix(adj_matrix1, mode = "directed", weighted = T)
for (i in 1:nrow(adj_matrix1)) {
  for (j in 1:ncol(adj_matrix1)) {
    max_value = max(adj_matrix1[i,])
    min_value = sort(adj_matrix1, decreasing = T)[10]
    if (adj_matrix1[i,j] < min_value) {
      adj_matrix1[i,j] = 0
    }
  }
}
vg1 = graph_from_adjacency_matrix(adj_matrix1, mode = "directed", weighted = T)
##write.graph(graph=vg1, file="firsthalf.graphml", format="graphml")

adj_matrix1A = first_half %>% 
  graph_from_data_frame(directed = F) %>%
  get.adjacency() %>%
  as.matrix()
g1A = graph_from_adjacency_matrix(adj_matrix1A, mode = "undirected", weighted = T)
##write.graph(graph=g1A, file="firsthalfA.graphml", format="graphml")


##for second half
adj_matrix2 = second_half %>% 
  graph_from_data_frame(directed = T) %>%
  get.adjacency() %>%
  as.matrix()
adj_matrix2[c("8","11","10"),] = adj_matrix2[c("8","11","10"),] + adj_matrix2[c("21","7","15"),]
adj_matrix2[,c("8","11","10")] = adj_matrix2[,c("8","11","10")] + adj_matrix2[,c("21","7","15")]
adj_matrix2 = adj_matrix2[-(12:14),-(12:14)]
g2 = graph_from_adjacency_matrix(adj_matrix2, mode = "directed", weighted = T)
for (i in 1:nrow(adj_matrix2)) {
  for (j in 1:ncol(adj_matrix2)) {
    max_value = max(adj_matrix2[i,])
    min_value = sort(adj_matrix2, decreasing = T)[10]
    if (adj_matrix2[i,j] < min_value) {
      adj_matrix2[i,j] = 0
    }
  }
}
vg2 = graph_from_adjacency_matrix(adj_matrix2, mode = "directed", weighted = T)
##write.graph(graph=vg2, file="secondhalf.graphml", format="graphml")

adj_matrix2a = second_half %>% 
  graph_from_data_frame(directed = F) %>%
  get.adjacency() %>%
  as.matrix()
adj_matrix2a[c("8","11","10"),] = adj_matrix2a[c("8","11","10"),] + adj_matrix2a[c("21","7","15"),]
adj_matrix2a[,c("8","11","10")] = adj_matrix2a[,c("8","11","10")] + adj_matrix2a[,c("21","7","15")]
adj_matrix2a = adj_matrix2a[-(12:14),-(12:14)]
g2a = graph_from_adjacency_matrix(adj_matrix2a, mode = "undirected", weighted = T)
##write.graph(graph=g2a, file="secondhalfcombineda.graphml", format="graphml")

adj_matrixf = first_half %>% 
  graph_from_data_frame(directed = T) %>%
  get.adjacency() %>%
  as.matrix()
gf = graph_from_adjacency_matrix(adj_matrixf, mode = "directed", weighted = T)



firsthalf_eigen = eigen_centrality(g1a, directed = T)
secondhalf_eigen = eigen_centrality(g2a, directed = T)
firsthalf_eigen = eigen_centrality(g1a, directed = F)
sort(firsthalf_eigen$vector, decreasing = T)
secondhalf_eigen = eigen_centrality(g2a, directed = F)
sort(secondhalf_eigen$vector, decreasing = T)


firsthalf_btwn = closeness(g1, directed = TRUE)
sort(firsthalf_btwn, decreasing = T)
