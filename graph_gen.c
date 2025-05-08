#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) {
    int nodes = atoi(argv[1]);
    int edges = atoi(argv[2]);
    srand(time(NULL));
    char **edge_exists = malloc((nodes + 1) * sizeof(char *));
    if (!edge_exists) {
        fprintf(stderr, "malloc error\n");
        return 1;
    }
    for (int i = 0; i <= nodes; i++) {
        edge_exists[i] = calloc(nodes + 1, sizeof(char));
        if (!edge_exists[i]) {
            fprintf(stderr, "calloc error\n");
            return 1;
        }
    }
    
    printf("p max %d %d\n", nodes, edges);
    printf("n 1 s\n"); 
    printf("n %d t\n", nodes); 

    int count = 0;
    while (count < edges) {
        int u = rand() % nodes + 1; 
        int v = rand() % nodes + 1; 
        if (u == v) continue;       
        if (edge_exists[u][v]) continue; 
        
        edge_exists[u][v] = 1;
        int capacity = (rand() % 100) + 1; 
        printf("a %d %d %d\n", u, v, capacity);
        count++;
    }
    
    for (int i = 0; i <= nodes; i++) {
        free(edge_exists[i]);
    }
    free(edge_exists);
    
    return 0;
}
