import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from database.agent_db import AgentDB

logger = logging.getLogger(__name__)


class Agent(BaseModel):
    name: str = Field(max_length=50)
    specialty: str = Field(max_length=50)
    agent_rank: Literal['Junior', 'Senior', 'Commander']


class AgentUP(BaseModel):
    name: str | None = Field(max_length=50, default=None)
    specialty: str | None = Field(max_length=50, default=None)
    agent_rank: None | Literal['Junior', 'Senior', 'Commander'] = None


router = APIRouter()


@router.post("", status_code=201)
def add_agent(data: Agent):
    try:
        logging.info("post agent/ call")
        new_agent = AgentDB.create_agent(data.model_dump())

        logging.info("post agent/ finish")
        return new_agent
    
    except ValueError as e:
        logging.error(str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def get_all_agents():
    logging.info("get agent/ call")

    agents =  AgentDB.get_all_agents()
    if not agents:
        logging.warning('empty list')

    logging.info("get agent/ finish")
    return agents


@router.get("/{id}")
def get_agent_by_id(id: int):
    logging.info("get agent/id call")
    found = AgentDB.get_agent_by_id(id)

    if not found:
        logging.error(f"agent id {id} not found")
        raise HTTPException(status_code=404, detail=f"agent id {id} not found.")
    
    logging.info("get agent/ finish")
    return found
    

@router.put("/{id}")
def update_agent(id: int, agent: AgentUP):
    logging.info("put agent/ call")

    if agent is None:
        logger.error(f"try to update an agent with empty data: {id}")
        raise HTTPException(status_code=400, detail=f"try to update an agent with empty data: {id}")

    found = AgentDB.get_agent_by_id(id)
    if not found:
        logging.error(f"agent id {id} not found")
        raise HTTPException(status_code=404, detail=f"agent id {id} not found.")
    
    updated = AgentDB.update_agent(id, agent.model_dump(exclude_none=True))
    if not updated:
        logging.error(f"update field: {id}")
        raise HTTPException(status_code=400, detail=f"update field: {id}")
    
    logging.info("put agent/ finish")
    return {"msg": f"id {id} updated."}


@router.put("/{id}/deactivate")
def deactive_agent(id: int):
    logging.info("put agent/ call (deactive)")

    found = AgentDB.get_agent_by_id(id)
    if not found:
        logging.error(f"agent id {id} not found")
        raise HTTPException(status_code=404, detail=f"agent id {id} not found.")
    
    changed = AgentDB.deactivate_agent(id)
    if not changed:
        logging.error(f"deactive field: {id}")
        raise HTTPException(status_code=400, detail=f"diactive field: {id} alrady deactive")
    
    logging.info("put agent/ finish (deactive)")
    return {"msg": f"id {id} become deactive."}


@router.get("/{id}/performance")
def get_agent_performance(id: int):
    logging.info(f"get /{id}/performance call")

    found = AgentDB.get_agent_by_id(id)
    if not found:
        logging.error(f"agent id {id} not found")
        raise HTTPException(status_code=404, detail=f"agent id {id} not found.")
    
    data = AgentDB.get_agent_performance(id)
    logging.info(f"get /{id}/performance finish")
    return data

