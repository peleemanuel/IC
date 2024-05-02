import networkx as nx

def average_degree(G: nx.Graph) -> float:
    return sum(G.degree(n) for n in G.nodes) / len(G.nodes)

def clustering_coef(G: nx.Graph, u: int):
    """
    Return the clustering coefficient of node `u` from graph `G`

    Parameters:
    -----------
    G: nx.Graph
        Input graph
    u: int
        Node to calculate the clustering coefficient of.

    Returns:
    --------
    clustering coeff: int

    """
    ei = 0
    for i in G.neighbors(u):  # For each neighbour `i` of `u`
        for j in G.neighbors(u):  # For each neighbour `j` of `u`
            if i != j:  # no self loops
                ei += G.has_edge(i, j)  # Check if it has edge and add it to the total edges
    return ei / (G.degree(u) * (G.degree(u) - 1))  # divide by 2 because we count the edges twice