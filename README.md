# Intelligence Task Manager #  
### Agent and task management system with fast api server.
### The system will manage adding agents or tasks as well as assigning tasks to agents according to certain legalities ###    
##  
# folder structure #  
```intelligence-task-manager/ 
├── database/ 
│   ├── db_connection.py 
│   ├── agent_db.py 
│   └── mission_db.py 
├── README.md 
├── requirements.txt 
└── .gitignore 
```
##
# endpoints #  
## agents endpoints  ##
-   POST   /agents חדש סוכן יצירת 
-   GET   /agents הסוכנים כל 
-   GET   /agents/{id} לפי סוכן ID 
-   PUT   /agents/{id} סוכן עדכון 
-   PUT   /agents/{id}/deactivate סוכן השבתת 
-   GET   /agents/{id}/performance סוכן ביצועי 
##  
## missions endpoints  ##
-   POST   /missions משימה יצירת
-   GET   /missions המשימות כל 
-   GET   /missions/{id} לפי משימה ID 
-   PUT   /missions/{id}/assign/{agent_id} 
-   PUT   /missions/{id}/start משימה התחלת 
-   PUT   /missions/{id}/complete בהצלחה סיום 
-   PUT   /missions/{id}/fail בכישלון סיום 
-   PUT   /missions/{id}/cancel משימה ביטול 
##  
## reports endpoints  ##
-   GET   /reports/summary המערכת של כללי דוח 
-   GET   /reports/missions-by-status סטטוס לפי משימות 
-   GET   /reports/top-agent המצטיין הסוכן  get_top_agent 

##
# system flow #  
- create agent: fastapi request -> routers handler[agents] -> data line[add agent] -> answer: 
- create mission: fastapi request -> routers handler[mission] -> data line[add mission] ->  answer: 
- assign: fastapi request -> routers handler[mission] -> data line -> assign_mission -> checks -> answer:
- start mission: fastapi request -> routers handler[mission] -> update_mission_status -> answer:
- finish mission: fastapi request -> routers handler[mission] -> update_mission_status -> answer:
- report /summary: fastapi request -> routers handler[report] -> count_active_agents, count_all_missions, count_open_missions, count_completed_missions, count_field_missions, count_critical_missions -> answer:
- report /missions-by-status: fastapi request -> routers handler[report] -> count_by_status -> answer:
- report /top-agent: fastapi request -> routers handler[report] -> get_top_agent -> answer:

##
# table structure #  
## agents table ##  
| filed | type | comments |
| :---- | :--------- | :------------- |  
id | PRIMARY KEY, AUTO_INCREMENT |unique identifier  
name | VARCHAR(50) | agent name  
specialty|VARCHAR(50) | Area of ​​expertise  
is_active|BOOLEAN| default TRUE  
completed_missions| int| default 0  
failed_missions | int | default 0   
agent_rank|ENUM|Junior / Senior / Commander|  
##  
## missions table ##  
| filed | type | comments |
| :---- | :--------- | :------------- |  
id | PRIMARY KEY, AUTO_INCREMENT |unique identifier  
title|VARCHAR(255)|The title of the task  
description|text|Detailed description  
location|VARCHAR(255)|location  
difficulty| int | 1–10 only
importance| int | 1–10 only
status| ENUM| CANCELLED, FAILED, COMPLETED, IN_PROGRESS, ASSIGNED, NEW `DEFAULT NEW`  
risk_level |VARCHAR|Automatically calculated - does not come from the user  
assigned_agent_id|int|Until the affiliation-null  
##
# classes and methods #
## DB_connection class ##  
| func | Description |
| :---- | :------------------- |  
get_connection()|Returns an active connection to MySQL  
create_database()|Creates Intelligence_db if it does not exist.  
create_tables()|Creates both tables if they do not exist.  
##
## AgentDB class ##  
| func | Description |
| :---- | :------------------- |  
create_agent(data)|Creates a new agent and returns the agent object.
get_all_agents()|Returns a list of all agents
get_agent_by_id(id)|Returns one agent by ID, or None
update_agent(id, data)|UPDATE for the entire row (cannot change id)
deactivate_agent(id)|Sets agent inactive status
increment_completed(id)|Updates the number of tasks completed.
increment_failed(id)|Updates the number of failed tasks
get_agent_performance(id)| Returns a dictionary with these keys completed, failed, total, success_rate
count_active_agents()|Returns the number of active agents
##
## MissionDB class ##  
| func | Description |
| :---- | :------------------- |  
create_mission(data)|Creates a new task and returns the entire object
get_all_missions()|Returns all tasks
get_mission_by_id(id)|Returns one task by ID, or None
assign_mission(m_id, a_id)|Assigning a task to an agent
update_mission_status(id, status)|Used for any status change
get_open_missions_by_agent(id)|Returns agent ASSIGNED/IN_PROGRESS tasks
count_all_missions()|Total tasks
count_by_status(status)|Counting by a certain status
count_open_missions()|Open task counter
count_critical_missions()|CRITICAL task counter
get_top_agent()|The agent with the highest completed_missions  
##
# system rules #  
1. rank must be Junior / Senior / Commander — any other value throws an error.
2. difficulty and importance must be between 1 and 10 — otherwise an error.
3. risk_level is calculated automatically when creating a task — the user does not submit it.
4. An agent with is_active=False cannot accept tasks.
5. An agent cannot have more than 3 open tasks (ASSIGNED / IN_PROGRESS) at the same time.
6. If risk_level=CRITICAL — only an agent with the Commander rank can accept the task.
7. Only a task with the status NEW can be assigned. After assignment: status=ASSIGNED.
8. Only a task with the status ASSIGNED can be started. After: status=IN_PROGRESS.
9. Only a task with the status IN_PROGRESS can be finished and changed to failed or completed.
10. Only a task with the status NEW or ASSIGNED can be canceled — otherwise an error.  
##  
# running instructions #
1. ```git clone https://github.com/david999meir-png/Intelligence_Task_Manager```  
2. ```docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0```
3. ```cd .\Intelligence_Task_Manager\```
4. ```python -m venv .venv ```  
5. ```.\.venv\Scripts\activate ```  
6. ```pip install -r requirements.txt```
7. ```py main.py```


   
