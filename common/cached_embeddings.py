"""Embeddings with a small on-disk cache, so the help centre is embedded once (by the presenter) and
students only embed their questions. Wraps LangChain's GoogleGenerativeAIEmbeddings.

    emb = CachedEmbeddings("gemini-embedding-001", api_key, "kb/embeddings_cache.npz")
    store = InMemoryVectorStore(emb); store.add_documents(chunks)     # cache hits cost nothing
"""
import hashlib
import os

import numpy as np
from langchain_core.embeddings import Embeddings

from .gemini_helpers import call_gemini


class CachedEmbeddings(Embeddings):
    def __init__(self, model, api_key, cache_path, dimensions=768):
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        self.model, self.dimensions, self.cache_path = model, dimensions, cache_path
        self.live = GoogleGenerativeAIEmbeddings(model=model, google_api_key=api_key)
        self.cache = {}
        self.hits = self.misses = 0
        if os.path.exists(cache_path):
            data = np.load(cache_path)
            self.cache = dict(zip(data["keys"].tolist(), data["vectors"].astype(np.float32)))

    def _key(self, text):
        return hashlib.sha1(f"{self.model}|{self.dimensions}|{text}".encode("utf-8")).hexdigest()

    def save(self):
        keys = sorted(self.cache)
        np.savez_compressed(self.cache_path, keys=np.array(keys), vectors=np.array([self.cache[k] for k in keys], dtype=np.float16))

    def embed_documents(self, texts):
        missing = [t for t in dict.fromkeys(texts) if self._key(t) not in self.cache]
        self.hits += len(texts) - len(missing)
        self.misses += len(missing)
        for i in range(0, len(missing), 50):
            batch = missing[i:i + 50]
            vectors = call_gemini(lambda: self.live.embed_documents(batch, task_type="RETRIEVAL_DOCUMENT",
                                                                    output_dimensionality=self.dimensions), self.model)
            for t, v in zip(batch, vectors):
                self.cache[self._key(t)] = np.asarray(v, dtype=np.float32)
        if missing:
            self.save()
        return [self.cache[self._key(t)].tolist() for t in texts]

    def embed_query(self, text):
        return call_gemini(lambda: self.live.embed_query(text, task_type="RETRIEVAL_QUERY",
                                                         output_dimensionality=self.dimensions), self.model)
