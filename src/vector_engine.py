import time
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Dados simulados (Lore do Skyrim + Ruído para teste)
# Em produção, isso viria do seu banco de dados ou arquivos PDF lidos
DOCUMENTOS = [
    "O Dragonborn (Dovahkiin) possui o sangue de dragão e pode usar o Thu'um.",  # ID 0
    "Whiterun é a capital comercial de Skyrim, governada pelo Jarl Balgruuf.",     # ID 1
    "A Guilda dos Ladrões opera nos esgotos de Riften longe da lei.",              # ID 2
    "O Fus Ro Dah é um grito de força implacável que lança inimigos longe.",       # ID 3
    "Python é uma linguagem de programação interpretada de alto nível.",           # ID 4 (Ruído)
    "O compilador GCC otimiza código C++ para arquitetura x86.",                   # ID 5 (Ruído)
]

def main():
    print("-" * 50)
    print("🚀 INICIANDO VECTOR ENGINE (TCC)")
    print("-" * 50)

    # 1. Carregar Modelo (Transformer)
    # O all-MiniLM-L6-v2 gera vetores de 384 dimensões
    print("📦 [1/4] Carregando modelo 'all-MiniLM-L6-v2'...")
    start_load = time.time()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"   --> Modelo carregado em {time.time() - start_load:.4f}s")

    # 2. Vetorização (Embeddings)
    print(f"🧠 [2/4] Gerando embeddings para {len(DOCUMENTOS)} documentos...")
    start_encode = time.time()
    
    # Gera a matriz densa (Numpy array)
    embeddings = model.encode(DOCUMENTOS)
    
    # IMPORTANTE (Matemática): Normalização L2
    # Para que o Produto Escalar (Inner Product) seja igual à Similaridade de Cosseno,
    # os vetores precisam ter magnitude 1.
    faiss.normalize_L2(embeddings)
    
    print(f"   --> Vetorização concluída em {time.time() - start_encode:.4f}s")
    print(f"   --> Shape dos dados: {embeddings.shape}")

    # 3. Indexação (FAISS - C++)
    print("📚 [3/4] Construindo índice FAISS (IndexFlatIP)...")
    dimension = embeddings.shape[1] # 384
    
    # Usamos IndexFlatIP (Inner Product) porque é mais rápido que calcular L2 distance
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    print(f"   --> Total indexado: {index.ntotal} vetores.")

    # 4. Teste de Busca
    # Note: A query não contém as palavras exatas "Dragonborn" ou "Fus Ro Dah"
    query_text = "guerreiro que grita nos inimigos"
    
    print(f"\n🔍 [4/4] Teste de Busca Semântica: '{query_text}'")
    
    # Vetorizar a query e normalizar
    query_vector = model.encode([query_text])
    faiss.normalize_L2(query_vector)
    
    # Buscar os 3 vizinhos mais próximos (Top-K)
    k = 3
    distances, indices = index.search(query_vector, k)
    
    print("\n🏆 RESULTADOS ENCONTRADOS:")
    for i in range(k):
        idx_doc = indices[0][i]
        score = distances[0][i] # Score de similaridade (próximo de 1 = idêntico)
        
        print(f"   Rank #{i+1} | Score: {score:.4f} | ID: {idx_doc}")
        print(f"   Texto: {DOCUMENTOS[idx_doc]}\n")

if __name__ == "__main__":
    main()