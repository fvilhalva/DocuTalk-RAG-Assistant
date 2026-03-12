import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.cluster import KMeans

print("🚀 Iniciando Teste de Stack Completa...")

# 1. NUMPY: Gerar dados sintéticos (2 clusters de dados)
print("🔢 Gerando dados com Numpy...")
X = np.random.rand(20, 2)  # 20 pontos em 2D
y_true = np.random.randint(0, 2, size=20)  # Classes reais (0 ou 1)

# 2. SCIKIT-LEARN: Clusterização (K-Means)
print("🤖 Rodando Scikit-Learn (K-Means)...")
kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(X)
y_pred = kmeans.labels_  # O que a IA "achou"

# 3. PANDAS: Organizar
print("📊 Organizando com Pandas...")
df = pd.DataFrame({"x": X[:, 0], "y": X[:, 1], "Real": y_true, "Previsto": y_pred})
print(df.head(3))

# 4. MATPLOTLIB + SKLEARN: Matriz de Confusão
print("🎨 Plotando Matriz de Confusão...")
cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm, display_labels=["Grupo A", "Grupo B"]
)

plt.figure(figsize=(10, 5))

# Subplot 1: A Matriz
plt.subplot(1, 2, 1)
plt.title("Matriz de Confusão (Sklearn)")
disp.plot(ax=plt.gca(), cmap="Blues")

# 5. NETWORKX: Grafo de Similaridade
print("🕸️ Gerando Grafo com NetworkX...")
# Criar grafo onde nós são conectados se forem do mesmo cluster previsto
G = nx.Graph()
for i in range(len(y_pred)):
    G.add_node(i, cluster=y_pred[i])
    # Conecta com o anterior se for do mesmo cluster (lógica simples de teste)
    if i > 0 and y_pred[i] == y_pred[i - 1]:
        G.add_edge(i, i - 1)

# Subplot 2: O Grafo
plt.subplot(1, 2, 2)
plt.title("Grafo de Clusters (NetworkX)")
pos = nx.spring_layout(G)
nx.draw(
    G, pos, with_labels=True, node_color=y_pred, cmap=plt.cm.coolwarm, node_size=300
)

plt.tight_layout()
plt.savefig("teste_completo.png")
print("\n✅ Sucesso! Verifique a imagem 'teste_completo.png'.")
