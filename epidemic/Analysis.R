
# Gets the fraction of infected people in the graph
get_infected_nodes_fraction <- function(state){
  infected_nodes <- length(which(state==1))
  return(infected_nodes/length(state))
}

# Counts the number of infected neighbors for each node
count_infected_neighbors <- function(node_neighs, infected_nodes){
  nodes_count = 0
  for (neighbor in node_neighs){
    if (neighbor %in% infected_nodes){
      nodes_count = nodes_count + 1
    }
  }
  return(nodes_count)
}

get_new_infected_nodes <- function(n, beta){
  infection_prob <- 1-(1-beta)**n
  infected = 0
  if (infection_prob >= runif(1,0,1)){
    infected = 1
  }
  return(infected)
}

get_new_state <- function(suspects_ids,suspects_update, state){
  for (i in 1:length(suspects_ids)){
    node_id <- suspects_ids[i]
    node_state <- suspects_update[i]
    state[node_id] <- node_state
  }
  return(state)
}

# Simulates a SI model for the given graph
si_simulation <- function(graph,beta,infected_ini,iters){
  n <- vcount(graph)
  infected_nodes_evol <-  c()
  
  # Initialize infected nodes
  initial_state <- integer(n)
  initial_state[infected_ini] <- 1
  
  # Get proportion of infected people
  infected_nodes_evol <- append(infected_nodes_evol, 
                                get_infected_nodes_fraction(initial_state))
  
  last_state <- initial_state
  
  # Simulate epidemic expansion
  for(i in 2:iters){
    infected <- which(last_state==1)
    suspects <- which(last_state==0)
    neighbors_list <- neighborhood(graph, nodes=suspects) 
    infected_neighbors <- lapply(neighbors_list, count_infected_neighbors,infected_nodes=infected)
    new_suspects_state <- lapply(infected_neighbors, get_new_infected_nodes, beta=beta)
    
    state <- get_new_state(suspects,new_suspects_state,
                           last_state)
    infected_nodes_evol <- append(infected_nodes_evol, 
                                  get_infected_nodes_fraction(state))
    
    last_state <- state
  }
  
  return(infected_nodes_evol)
}

mean_simulation <- function(g, beta, infected_init, tmax, simulations) {
  sapply(1:simulations, function(x) si_simulation(g, beta, infected_init, tmax)) %>%
    apply(1, mean)
}

plot_results <- function(results, legend, file, main, tmax) {
  pdf(paste0("plots/", file, ".pdf"))
  plot(NULL,
       xlim = c(1, tmax), ylim = c(0, 1),
       xlab = "Time", ylab = "Infection rate", main = main
  )
  sapply(1:length(results), function(g) lines(results[[g]], col = g))
  legend("topleft", legend, col = 1:length(results), lwd = 1)
  dev.off()
}
