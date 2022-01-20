
##### GENERAL PURPOSE FUNCTIONS

# Gets the maximum eigenvalue of the graph adjacency matrix
get_max_eigenvalue <- function(graph){
  adjacency_matrix <- as_adjacency_matrix(graph)
  eigenvalues <- eigen(adjacency_matrix)
  return(max(abs(eigenvalues$values)))
}

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

get_new_suspect_nodes <- function(n, gamma){
  infected = 1
  if (gamma >= runif(1,0,1)){
    infected = 0
  }
  return(infected)
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

##### SI SIMULATION FUNCTIONS

SI_get_new_state <- function(suspects_ids,suspects_update, state){
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
    
    state <- SI_get_new_state(suspects,new_suspects_state,
                           last_state)
    infected_nodes_evol <- append(infected_nodes_evol, 
                                  get_infected_nodes_fraction(state))
    
    last_state <- state
  }
  
  return(infected_nodes_evol)
}

SI_mean_simulation <- function(g, beta, infected_init, tmax, simulations) {
  sapply(1:simulations, function(x) si_simulation(g, beta, infected_init, tmax)) %>%
    apply(1, mean)
}


##### SIS SIMULATION FUNCTIONS


SIS_get_new_state <- function(infected_ids,infected_update,suspects_ids,suspects_update, state){
  for (i in 1:length(infected_ids)){
    node_id <- infected_ids[i]
    node_state <- infected_update[i]
    state[node_id] <- node_state
  }
  for (i in 1:length(suspects_ids)){
    node_id <- suspects_ids[i]
    node_state <- suspects_update[i]
    state[node_id] <- node_state
  }
  return(state)
}

# Simulates a SIS model for the given graph
SIS_simulation_initial_infected <- function(graph,beta,gamma,infected_ini,iters){
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
    new_infected_state <- lapply(infected, get_new_suspect_nodes, gamma=gamma)
    
    state <- SIS_get_new_state(infected,new_infected_state,suspects,new_suspects_state,
                           last_state)
    infected_nodes_evol <- append(infected_nodes_evol, 
                                  get_infected_nodes_fraction(state))
    
    last_state <- state
  }
  
  return(infected_nodes_evol)
}

SIS_simulation <- function(graph,beta,gamma,p0,iters){
  n <- vcount(graph)
  infected_nodes_evol <-  c()
  
  # Initialize infected nodes
  initial_state <- sample(c(0,1), replace=TRUE, size=n, 
                          prob=c(1-p0,p0))
  
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
    new_infected_state <- lapply(infected, get_new_suspect_nodes, gamma=gamma)
    
    state <- SIS_get_new_state(infected,new_infected_state,suspects,new_suspects_state,
                               last_state)
    infected_nodes_evol <- append(infected_nodes_evol, 
                                  get_infected_nodes_fraction(state))
    
    last_state <- state
  }
  
  return(infected_nodes_evol)
}

threshold_evalutation_initial_infected<- function(graphs,names,gamma,infected_ini,iters){
  i <- 1
  for (g in graphs){
    graph_res <- data.frame()
    lambda <- get_max_eigenvalue(g)
    beta <- gamma/lambda
    beta_low <- max(0,beta*0.9)
    beta_high <- min(1, beta*1.1)
    print(paste0("Algo.: ", names[[i]], " Thresh: ", 1/lambda, 
                 " beta/gamma below: ", beta_low/gamma,
                 " beta/gamma above: ", beta_high/gamma))
    sim <- SIS_simulation_initial_infected(g,beta_low,gamma,infected_ini[[i]],iters)
    graph_res <- rbind(graph_res, cbind(as.data.frame(sim),
                                        group=paste0(names[[i]],' below thr.'),
                                        time=seq.int(iters),
                                        inv_lambda=round(1/lambda, 5),
                                        beta_gama=round(beta_low/gamma, 5))
    )
    
    sim <- SIS_simulation_initial_infected(g,beta_high,gamma,infected_ini[[i]],iters)
    graph_res <- rbind(graph_res, cbind(as.data.frame(sim),
                                        group=paste0(names[[i]],' above thr.'),
                                        time=seq.int(iters),
                                        inv_lambda=round(1/lambda, 5),
                                        beta_gama=round(beta_high/gamma, 5)))
    
    ggplot(data=graph_res, aes(x=time, y=sim, group=group, color=as.factor(group))) +
      geom_line() +
      xlab("Time") +
      ylab("Infected nodes (%)") +
      ggtitle(paste0("Algo.: ", names[[i]]))
    
    
    i <- i+1
  }
  
}

threshold_evalutation<- function(graphs,names,gamma,p0,iters){
  i <- 1
  graph_res <- data.frame()
  for (g in graphs){
    lambda <- get_max_eigenvalue(g)
    beta <- gamma/lambda
    beta_low <- max(0,beta*0.9)
    beta_high <- min(1, beta*1.1)
    print(paste0("Algo.: ", names[[i]], " Thresh: ", 1/lambda, 
                 " beta/gamma below: ", beta_low/gamma,
                 " beta/gamma above: ", beta_high/gamma))
    sim <- SIS_simulation(g,beta_low,gamma,p0,iters)
    graph_res <- rbind(graph_res, cbind(as.data.frame(sim),
                                        group=paste0(names[[i]],' below thr.'),
                                        time=seq.int(iters),
                                        inv_lambda=round(1/lambda, 5),
                                        beta_gama=round(beta_low/gamma, 5))
    )
    
    sim <- SIS_simulation(g,beta_high,gamma,p0,iters)
    graph_res <- rbind(graph_res, cbind(as.data.frame(sim),
                                        group=paste0(names[[i]],' above thr.'),
                                        time=seq.int(iters),
                                        inv_lambda=round(1/lambda, 5),
                                        beta_gama=round(beta_high/gamma, 5)))
    
    i <- i+1
  }
  graph_res
}
