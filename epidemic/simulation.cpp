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


vector <float> si_model(vector < set <int> > adjacency_list, float beta, vector <int> infected_init, int iters) {
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
        // Simulation
    }

    return(infected_ratio_evol);

}

int main() {
    ifstream params;
    ofstream SI_infection_rate;

    vector < set <int> > adjacency_list;
    vector < int > infected_init;
    vector <float> infected_ratio_evol;

    int n;
    int iters=100;
    float beta=0.05;


    SI_infection_rate.open("results/SI_infection_rate.csv");
    params.open("params.txt");
    params >> n;

    // Initialize network as adjacency list
    adjacency_list = build_graph("graph.txt", n);

    // Get initially infected nodes
    infected_init = get_initial_infected("infected.txt");

    default_random_engine generator;
    for (int experiment = 0; experiment < 1; experiment++){
      // Run SI model and write results to file
      infected_ratio_evol = si_model(adjacency_list,beta,infected_init,iters);
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
}
