from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
preguntas = [line.strip() for line in open('data/preguntas_aborto.txt', 'r')]
embeddings = model.encode(preguntas)
np.save('embeddings/embeddings_aborto.npy', embeddings)