import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal


router = APIRouter()

@router.get("/summary")
def get_summary():
    return {"msg": "ssss"}