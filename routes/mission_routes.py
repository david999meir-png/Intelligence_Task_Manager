import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from database.mission_db import MissionDB
from database.agent_db import AgentDB


logger = logging.getLogger(__name__)


class Mission(BaseModel):
    title: str = Field(max_length=255)
    description: str
    location: str = Field(max_length=255)
    difficulty: int = Field(ge=1, le=10)
    importance: int = Field(ge=1, le=10)
    

router = APIRouter()


@router.post("", status_code=201)
def add_mission(data: Mission):
    try:
        logging.info("post missions/ call")
        new_mission = MissionDB.create_mission(data.model_dump())

        logging.info("post missions/ finish")
        return new_mission
    
    except ValueError as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def get_all_missions():
    logging.info("get missions/ call")
    
    missions =  MissionDB.get_all_missions()
    if not missions:
        logging.warning('empty list')

    logging.info("get missions/ finish")
    return missions


@router.get("/{id}")
def get_mission_by_id(id: int):
    logging.info("get missions/id call")
    found = MissionDB.get_mission_by_id(id)

    if not found:
        logging.error(f"mission id {id} not found")
        raise HTTPException(status_code=404, detail=f"mission id {id} not found.")
    
    logging.info("get missions/ finish")
    return found


@router.put("/{id}/assign/{agent_id}")
def assign_mission_to_agent(id: int, agent_id: int):
    logging.info(f"get missions//{id}/assign/{agent_id} call")

    mission_found = MissionDB.get_mission_by_id(id)
    if not mission_found:
        logging.error(f"mission id {id} not found")
        raise HTTPException(status_code=404, detail=f"mission not found: {id}")
    
    agent_found = AgentDB.get_agent_by_id(agent_id)
    if not agent_found:
        logging.error(f"Agent id {agent_id} not found")
        raise HTTPException(status_code=404, detail=f"Agent not found: {agent_id}")
    
    status_mission = mission_found["status"]
    if status_mission != "NEW":
        logging.error(f"Mission not available")
        raise HTTPException(status_code=400, detail=f"Mission not available: {id}")
    
    agent_active = agent_found["is_active"]
    if not agent_active:
        logging.error(f"Agent is not active")
        raise HTTPException(status_code=400, detail=f"Agent is not active: {agent_id}")

    open_missions = len(MissionDB.get_open_missions_by_agent(agent_id))
    if open_missions >= 3:
        logging.error(f"Agent has reached maximum missions")
        raise HTTPException(status_code=400, detail=f"Agent has reached maximum missions: id ={agent_id} open missions={open_missions}")
    
    risk_level = mission_found["risk_level"]
    if risk_level == "CRITICAL":
        if agent_found["agent_rank"] != "Commander":
            logging.error(f"Only Commander can handle critical missions")
            raise HTTPException(status_code=400, detail=f"Only Commander can handle critical missions")
        
    assigned = MissionDB.assign_mission(id, agent_id)
    if not assigned:
        logging.error(f"mission id {id} not assign to agen id {agent_id}")
        raise HTTPException(status_code=400, detail=f"mission id {id} not assign to agen id {agent_id}")
    return {"msg": f"mission id {id} assign to agen id {agent_id} successfully"}  


@router.put("/{id}/start")
def start_mission(id: int):
    logging.info(f"get missions/{id}/start call")

    found = MissionDB.get_mission_by_id(id)
    if not found:
        logging.error(f"mission id {id} not found")
        raise HTTPException(status_code=404, detail=f"mission id {id} not found.")
    
    try:
        updated = MissionDB.update_mission_status(id, "IN_PROGRESS")
        if not updated:
            logging.error(f"mission alrady IN_PROGRESS: {id}")
            raise ValueError("this mission alrady IN_PROGRESS")
        
        logging.info(f"get missions/{id}/start finish")
        return {"msg": f"mission id {id} update_mission_status to IN_PROGRESS successfully."}


    except ValueError as e:
        logging.error(f"mission start fiald: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}/complete")
def Successful_completion_of_a_task(id: int):
    logging.info(f"get missions/{id}/complete call")

    found = MissionDB.get_mission_by_id(id)
    if not found:
        logging.error(f"mission id {id} not found")
        raise HTTPException(status_code=404, detail=f"mission id {id} not found.")
    
    try:
        updated = MissionDB.update_mission_status(id, "COMPLETED")
        if not updated:
            logging.error(f"mission id {id} not updated")
            raise ValueError("this mission alrady COMPLETED")
        
        agent_id = found["assigned_agent_id"]
        AgentDB.increment_completed(agent_id)
        
        logging.info(f"get missions/{id}/complete finish")
        return {"msg": f"mission id {id} update_mission_status to COMPLETED successfully."}


    except ValueError as e:
        logging.error(f"mission complete fiald: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}/fail")
def field_completion_of_a_task(id: int):
    logging.info(f"get missions/{id}/fail call")

    found = MissionDB.get_mission_by_id(id)
    if not found:
        logging.error(f"mission id {id} not found")
        raise HTTPException(status_code=404, detail=f"mission id {id} not found.")
    
    try:
        updated = MissionDB.update_mission_status(id, "FAILED")
        if not updated:
            logging.error(f"mission id {id} not updated")
            raise ValueError("this mission alrady FAILED")
        
        agent_id = found["assigned_agent_id"]
        AgentDB.increment_failed(agent_id)
        
        logging.info(f"get missions/{id}/fail finish")
        return {"msg": f"mission id {id} update_mission_status to FAILED successfully."}

    except ValueError as e:
        logging.error(f"mission FAILED fiald: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put("/{id}/cancel")
def Canceling_task(id: int):
    logging.info(f"get missions/{id}/cancel call")

    found = MissionDB.get_mission_by_id(id)
    if not found:
        logging.error(f"mission id {id} not found")
        raise HTTPException(status_code=404, detail=f"mission id {id} not found.")
    
    try:
        updated = MissionDB.update_mission_status(id, "CANCELLED")
        if not updated:
            raise ValueError("this mission alrady CANCELLED")
                
        logging.info(f"get missions/{id}/cancel finish")
        return {"msg": f"mission id {id} update_mission_status to CANCELLED successfully."}

    except ValueError as e:
        logging.error(f"mission FAILED fiald: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))