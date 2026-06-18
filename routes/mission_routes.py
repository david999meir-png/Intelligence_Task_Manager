import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from database.mission_db import MissionDB


router = APIRouter()

@router.get("")
def get_all_missions():
    return MissionDB.get_all_missions()