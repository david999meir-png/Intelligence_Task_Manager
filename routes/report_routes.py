import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from database.agent_db import AgentDB
from database.mission_db import MissionDB

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/summary")
def get_summary():
    logging.info("get reports/summary/ call")

    active_agents_count = AgentDB.count_active_agents()
    total_missions = MissionDB.count_all_missions()
    open_missions = MissionDB.count_open_missions()
    completed_missions = MissionDB.count_completed_missions()
    failed_missions = MissionDB.count_field_missions()
    critical_missions = MissionDB.count_critical_missions()

    logging.info("get reports/summary/ finish")
    return {**active_agents_count, **total_missions, **open_missions,\
             **completed_missions, **failed_missions, **critical_missions}


@router.get("/missions-by-status")
def get_mission_by_status():
    logging.info("get reports/missions-by-status call")

    new = MissionDB.count_by_status("NEW")
    assign = MissionDB.count_by_status("ASSIGNED")
    in_progress = MissionDB.count_by_status("IN_PROGRESS")
    completed = MissionDB.count_by_status("COMPLETED")
    failed = MissionDB.count_by_status("FAILED")
    cancel = MissionDB.count_by_status("CANCELLED")
    
    logging.info("get reports/missions-by-status finish")
    return {**new, **assign, **in_progress, **completed, **failed, **cancel}


@router.get("/top-agent")
def get_top_agent():
    logging.info("get reports/top-agent call")
    agent = MissionDB.get_top_agent()

    logging.info("get reports/top-agent finish")
    return agent
