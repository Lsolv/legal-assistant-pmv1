from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..services.chatbot_service import LegalChatbot
from ..models.legal_query import LegalQuery
from ..schemas.legal_query import LegalQueryCreate, LegalQueryResponse
from ..utils.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()
chatbot = LegalChatbot()

@router.post("/query", response_model=LegalQueryResponse)
async def ask_legal_question(query: LegalQueryCreate, db: Session = Depends(get_db)):
    try:
        # Obtener respuesta del chatbot
        response = chatbot.answer_legal_question(query.question)
        
        # Guardar en base de datos (si hay usuario autenticado)
        if query.user_id:
            db_query = LegalQuery(
                question=query.question,
                response=response["answer"],
                user_id=query.user_id
            )
            db.add(db_query)
            db.commit()
            db.refresh(db_query)
            response["query_id"] = db_query.id
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/suggested-questions", response_model=List[str])
async def get_suggested_questions():
    return chatbot.get_suggested_questions()