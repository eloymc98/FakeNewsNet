#include <fstream>
#include <random>
#include <set>
#include <vector>
using namespace std;

vector < set <int> > build_graph(string path, int n) {
    std::ifstream edgelist(path);
    vector < set <int> > adjacency_list(n, set <int> ());
    int u, v;
    while (edgelist >> u >> v){
        adjacency_list[u].insert(v);
        adjacency_list[v].insert(u);
    }
    return adjacency_list;
}

vector < int > get_initial_infected(string path) {
    std::ifstream inputfile(path);
    vector < int > infected_init;
    int a;
    while (inputfile >> a){
        infected_init.push_back(a);
    }
    return infected_init;
}

vector < int > get_initial_infected_random(float p0, int n, default_random_engine generator) {
    vector < int > infected_init;
    uniform_int_distribution <int> random_distribution(0, 100);
    for (int i=0;i<n;i++){
        int p = random_distribution(generator);
        float random_prob = 1.0*p/100;
        if (p0>=random_prob){
          infected_init.push_back(i);
        }

    }
    return infected_init;
}

float get_infected_nodes_fraction(vector<int> state, int n) {
    vector<int>::iterator it;
    int infected=0;
    for (it = state.begin(); it != state.end(); ++it){
        if (*it == 1){
          infected++;
        }
    }
    return 1.0*infected/n;
}

int count_infected_neighbors(set <int> neighbors, vector <int> state) {
  set<int>::iterator it;
  int count = 0;
  for (it = neighbors.begin(); it != neighbors.end(); ++it){
      if(state[*it]==1)
          count++;
  }
  return count;
}

vector<int> get_new_state(vector <int> state, int n, vector < set <int> > adjacency_list, float beta, default_random_engine generator) {
    vector<int> new_state;
    new_state.assign(state.begin(), state.end());

    // Iterate over suspect nodes to get new infected nodes
    uniform_int_distribution <int> random_distribution(0, 100);
    vector<int>::iterator id;
    int infected_count;
    float infection_prob;
    for (int i = 0; i<n; i++){
        if (state[i] == 0){
          // Count number of infected nodes
          set <int> neighbors = adjacency_list[i];
          infected_count = count_infected_neighbors(neighbors,state);
          // Compute infection probability
          infection_prob = 1.0 - pow((1.0-beta),infected_count);

          // Decide if node gets infected
          int p = random_distribution(generator);
          float random_prob = 1.0*p/100;
          if (infection_prob>=random_prob){
              new_state[i] = 1;
          }
        }
    }
    return new_state;
}

vector <float> si_model(vector < set <int> > adjacency_list, float beta, vector <int> infected_init, int iters, default_random_engine generator) {
    int n = adjacency_list.size();
    vector <float> infected_ratio_evol;
    vector <int> current_state(n,0);
    vector <int> last_state;
    float infected_ratio;

    // Initialize current_state with infected nodes
    vector<int>::iterator it;
    for (it = infected_init.begin(); it != infected_init.end(); ++it){
        current_state[*it] = 1;
    }

    // Get proportion of infected people
    infected_ratio = get_infected_nodes_fraction(current_state, n);
    infected_ratio_evol.push_back(infected_ratio);

    // Copy state
    last_state.assign(current_state.begin(), current_state.end());

    for(int t=1; t<iters; t++){
        printf("Iteration %d of %d\n", t, iters);
        // Simulation
        current_state = get_new_state(last_state, n, adjacency_list, beta, generator);
        infected_ratio = get_infected_nodes_fraction(current_state, n);
        infected_ratio_evol.push_back(infected_ratio);
        last_state.assign(current_state.begin(), current_state.end());
    }

    return(infected_ratio_evol);

}

int main(int argc, char** argv) {
    ifstream params;
    ofstream SI_infection_rate;
    default_random_engine generator;

    vector < set <int> > adjacency_list;
    vector < int > infected_init;
    vector <float> infected_ratio_evol;

    int n;
    int iters;
    float beta;
    string graph_path, infected_path, params_path, results_path;

    time_t start = time(&start);

    if(argc<6||argc>7){
      return 0;
    }

    graph_path = argv[1];
    params_path = argv[2];
    results_path = argv[3];
    beta = std::stof(argv[4]);
    iters = std::stoi(argv[5]);

    SI_infection_rate.open(results_path);
    params.open(params_path);
    params >> n;

    // Initialize network as adjacency list
    adjacency_list = build_graph(graph_path, n);

    if (argc == 6){
      // Get initially infected nodes
      infected_init = get_initial_infected_random(0.05, n, generator);
    } else if (argc==7){
      infected_path = argv[6];

      // Get initially infected nodes
      infected_init = get_initial_infected(infected_path);
    } else{
      return 0;
    }


    for (int experiment = 0; experiment < 1; experiment++){
      // Run SI model and write results to file
      infected_ratio_evol = si_model(adjacency_list,beta,infected_init,iters,generator);
      vector<float>::iterator it;
      int i=0;
      for (it = infected_ratio_evol.begin(); it != infected_ratio_evol.end(); ++it){
        if (i > 0)
            SI_infection_rate << ',';
        SI_infection_rate << *it;
        i++;
      }
      SI_infection_rate << endl;
    }
    SI_infection_rate.close();
    params.close();

    time_t end = time(&end);
    printf("Simulation in %ld seconds\n", end-start);
}
