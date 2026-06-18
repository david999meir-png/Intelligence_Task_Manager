from fastapi import FastAPI
import uvicorn
from logs.setup_log import setup_logger
from database.db_connection import DBConnection
from database.agent_db import AgentDB
from database.mission_db import MissionDB


app = FastAPI()

agent = [
    {"name": "david" , "specialty": "aaa" , "agent_rank": "Junior"},
    {"name": "dan", "specialty": "ccc" , "agent_rank": "Senior"},
    {"name": "moshe" , "specialty": "qqq" , "agent_rank": "Junior"},
    {"name": "tal", "specialty": "ooo" , "agent_rank": "Commander"}
]

mission = [
    {"title": "1" ,"description": "ssssss" ,"location": "aa" ,"difficulty": 1 ,"importance":3 },
    {"title": "2" ,"description": "ssssss" ,"location": "aa" ,"difficulty": 1 ,"importance":5 },
    {"title": "3" ,"description": "ssssss" ,"location": "aa" ,"difficulty": 1 ,"importance":9 },
    {"title": "4" ,"description": "ssssss" ,"location": "aa" ,"difficulty": 1 ,"importance":10 },
    {"title": "5" ,"description": "ssssss" ,"location": "aa" ,"difficulty": 8 ,"importance":10 }
]


if __name__ == "__main__":
    setup_logger()

    DBConnection.create_database()
    DBConnection.create_tables()

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



    # print(f'{MissionDB.get_mission_by_id(8)=}')
    # print(f'{MissionDB.count_open_missions()=}')
    # print(f'{MissionDB.count_all_missions()=}')
    # print(f'{MissionDB.count_by_status("NEW")=}')


    # print(f'{MissionDB.count_critical_missions()=}')
    
    # print(f'{MissionDB.create_mission({"title": "5" ,"description": "ssssss" ,"location": "aa" ,"difficulty": 8 ,"importance":10 })=}')
    # print(f'{MissionDB.assign_mission(1,10)=}')
    # print(f'{MissionDB.assign_mission(2,10)=}')
    # print(f'{MissionDB.assign_mission(3,10)=}')
    # print(f'{MissionDB.assign_mission(4,10)=}')

    # print(f'{MissionDB.update_mission_status(1, "IN_PROGRESS")=}')
    # print(f'{MissionDB.update_mission_status(8, "CANCELLED")=}')
    # print(f'{MissionDB.update_mission_status(1, "ASSIGNED")=}')
    # print(f'{MissionDB=}')
    # print(f'{MissionDB=}')


    # print(AgentDB.increment_completed(1))
    # print(AgentDB.increment_failed(1))
    # print(AgentDB.get_agent_by_id(8))

    # print(AgentDB.count_active_agents())
    # print(AgentDB.deactivate_agent(2))
    # print(AgentDB.get_agent_by_id(2))

    # print(AgentDB.get_agent_performance(3))

    # for a in agent:
    #     try:
    #         AgentDB.create_agent(a)

    #     except Exception as e:
    #         print(e)

    # for m in mission:
    #     try:
    #         MissionDB().create_mission(m)

    #     except Exception as e:
    #         print(e)
