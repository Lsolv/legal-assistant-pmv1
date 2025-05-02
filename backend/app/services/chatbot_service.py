from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import torch
from typing import List, Dict
import json
import os

class LegalChatbot:
    def __init__(self):
        # Cargar modelo de preguntas y respuestas en español
        self.qa_model = pipeline(
            "question-answering",
            model="mrm8488/distillbert-base-spanish-wwm-cased-finetuned-spa-squad2-es"
        )
        
        # Modelo para embeddings semánticos
        self.semantic_model = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')
        
        # Cargar base de conocimiento legal
        self.load_legal_knowledge()
    
    def load_legal_knowledge(self):
        # Esto debería cargarse desde una base de datos en producción
        legal_data_path = os.path.join(os.path.dirname(__file__), "../../ml/data/legal_knowledge.json")
        with open(legal_data_path, "r", encoding="utf-8") as f:
            self.legal_knowledge = json.load(f)
        
        # Precomputar embeddings para búsqueda semántica
        self.legal_contexts = [item["context"] for item in self.legal_knowledge]
        self.legal_embeddings = self.semantic_model.encode(self.legal_contexts, convert_to_tensor=True)
    
    def find_most_relevant_context(self, question: str) -> str:
        # Codificar la pregunta
        question_embedding = self.semantic_model.encode(question, convert_to_tensor=True)
        
        # Calcular similitud coseno
        cos_scores = util.pytorch_cos_sim(question_embedding, self.legal_embeddings)[0]
        
        # Obtener el contexto más relevante
        most_relevant_idx = torch.argmax(cos_scores).item()
        return self.legal_contexts[most_relevant_idx]
    
    def answer_legal_question(self, question: str) -> Dict:
        # Encontrar el contexto más relevante
        context = self.find_most_relevant_context(question)
        
        # Obtener respuesta del modelo QA
        result = self.qa_model(question=question, context=context)
        
        return {
            "question": question,
            "answer": result["answer"],
            "confidence": float(result["score"]),
            "context": context
        }
    
    def get_suggested_questions(self) -> List[str]:
        return [item["sample_question"] for item in self.legal_knowledge[:5]]