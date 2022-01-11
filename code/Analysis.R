library(dplyr)
library(igraph)


fakenews.graph <- read.graph("graph.txt", format="edgelist")
fakenews.infected <- read.table(file="infected.txt")$V1


tmax <- 20
simulations <- 1

graphs <- list(FakeNews = fakenews.graph)

si_simulation <- function(g, beta, initial) {
  n <- length(V(g))
  r <- numeric(tmax)
  infected <- integer(n)
  infected[initial] <- 1
  r[1] <- sum(infected)
  print(infected)
  for (i in 2:tmax) {
    infected_neighbors <- (as_adj(g) %*% infected)[, 1]
    infection_probability <- 1 - (1 - beta)^infected_neighbors
    new_infected  <- rbinom(n, 1, infection_probability)
    infected <- infected + (1 - infected) * new_infected
    r[i] <- sum(infected)
  }
  r/n
  return(r)
}
 
rr <- si_simulation(fakenews.graph, 0.2, fakenews.infected)

mean_simulation <- function(g, beta, initial) {
  sapply(1:simulations, function(x) si_simulation(g, beta, initial)) %>%
    apply(1, mean)
}

plot_results <- function(results, legend, file, main) {
  pdf(paste0("plots/", file, ".pdf"))
  plot(NULL,
       xlim = c(1, tmax), ylim = c(0, 1),
       xlab = "Time", ylab = "Infection rate", main = main
  )
  sapply(1:length(results), function(g) lines(results[[g]], col = g))
  legend("topleft", legend, col = 1:length(results), lwd = 1)
  dev.off()
}


# Task 1

beta <- 0.3
gamma <- 0.3

graphs %>%
  lapply(mean_simulation, beta, fakenews.infected) %>%
  plot_results(names(graphs), "1",
               expression("Simulation with " ~ beta ~ " = " ~ 1)
  )

