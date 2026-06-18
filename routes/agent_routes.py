import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from database.agent_db import AgentDB


router = APIRouter()

@router.get("")
def get_all_agents():
    return AgentDB.get_all_agents()