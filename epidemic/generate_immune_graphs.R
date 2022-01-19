rm(list = ls())
library(dplyr)
library(igraph)
library("poweRlaw")
library("ggplot2")

setwd("C:/Users/bscuser/Documents/MIRI/CSN/FakeNewsNet/code") 

graph.file <- c("graph_politifact15014_fake.txt")
infected.file <- c("infected_politifact15014_fake.txt")

generate.inmune.graphs <- function(file.graph, file.infected) {
  graph <- read.graph(file.graph, format="edgelist", directed=FALSE)
  V(graph)$name <- as.character(V(graph))
  fakenews.infected <- read.table(file=file.infected)$V1 + 1
  
  G.betweenness <- betweenness(graph)
  
  infected.n <- length(fakenews.infected)
  idx.nodes.betweenness <- sort(G.betweenness, decreasing = T)[1:infected.n]
  nodes.betweenness <- which(G.betweenness %in% idx.nodes.betweenness)
  
  nodes.to.remove <- setdiff(nodes.betweenness, fakenews.infected)
  first.graph <- delete.vertices(graph, nodes.to.remove[1:ceiling(length(nodes.to.remove)*1/3)])
  second.graph <- delete.vertices(graph, nodes.to.remove[1:ceiling(length(nodes.to.remove)*2/3)])
  third.graph <- delete.vertices(graph, nodes.to.remove[1:ceiling(length(nodes.to.remove)*3/3)])
  
  name1 <- paste("immune1",file.graph,sep="_")
  write.graph(first.graph, name1, format = "ncol")
  name2 <- paste("immune2",file.graph,sep="_")
  write.graph(second.graph, name2, format = "ncol")
  name3 <- paste("immune3",file.graph,sep="_")
  write.graph(third.graph, name3, format = "ncol")
}

generate.inmune.graphs(graph.file, infected.file)
