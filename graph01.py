import matplotlib.pyplot as plt
import networkx as nx

# 1. Dados simulados (Isso viria da sua extração de texto com LLM)
# Estrutura: (Sujeito, Ação, Objeto)
triplets = [
    ("Dragonborn", "mata", "Dragão"),
    ("Dragonborn", "usa", "Tu'um"),
    ("Dragão", "cospe", "Fogo"),
    ("Whiterun", "tem", "Jarl"),
    ("Dragonborn", "visita", "Whiterun"),
    ("Jarl", "pede_ajuda", "Dragonborn")
]

# 2. Criar o Grafo Direcionado (DiGraph)
G = nx.DiGraph()

for source, relation, target in triplets:
    G.add_edge(source, target, label=relation)

# 3. Plotar com Matplotlib
plt.figure(figsize=(10, 8))

# Define a posição dos nós (layout de mola evita sobreposição)
pos = nx.spring_layout(G, k=0.5, seed=42)

# Desenha nós, arestas e labels
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue",
        font_size=10, font_weight="bold", edge_color="gray", arrows=True)

# Adiciona os textos nas arestas (as ações/verbos)
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.title("Sua PoC: Grafo de Conhecimento (GraphRAG)", fontsize=15)
plt.show()