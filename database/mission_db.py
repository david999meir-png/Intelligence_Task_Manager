from database.db_connection import DBConnection
from database.agent_db import AgentDB

class MissionDB:
    @staticmethod
    def create_mission(data):
        with DBConnection.get_connection() as conn:
            with conn.cursor() as cursor:
                risk_value = data["difficulty"] * 2 + data["importance"]
                risk_level = None

                if 0 <= risk_value <= 9:
                    risk_level = "LOW"
                elif 10 <= risk_value <= 17:
                    risk_level = "MEDIUM"
                elif 18 <= risk_value <= 24:
                    risk_level = "HIGH"
                elif risk_value <= 25:
                    risk_level = "CRITICAL"
                else:
                    raise ValueError(f"invalid value in difficulty or importance")

                sql = """
                INSERT INTO missions (title, description, location, difficulty, importance, risk_level) VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = list(data.values()) + [risk_level]
                cursor.execute(sql, values)
                
                conn.commit()
                new_id = cursor.lastrowid

                mission = MissionDB.get_mission_by_id(new_id)
                return mission
            
    @staticmethod
    def get_all_missions():
        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT * FROM missions"""
                cursor.execute(sql)

                missions = cursor.fetchall()
                return missions
            
    @staticmethod
    def get_mission_by_id(id):
        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT * FROM missions WHERE id = %s"""
                cursor.execute(sql, (id,))

                mission = cursor.fetchone()
                return mission
    
    @staticmethod
    def assign_mission(m_id, a_id):
        with DBConnection.get_connection() as conn:
            agent = AgentDB.get_agent_by_id(a_id)

            is_active = agent["is_active"]
            if not is_active:
                raise ValueError(f"agent id {a_id} not active.")
            
            open_mission = MissionDB.get_open_missions_by_agent(a_id)
            if len(open_mission) >= 3:
                raise ValueError(f'agent id: {a_id} alrady has the max open missions')
            
            mission = MissionDB.get_mission_by_id(m_id)
            if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander":
                raise ValueError(f"the mission level is critical, you need agent with rank Commander fro this")
            
            status_mission = mission["status"]
            if status_mission is not "NEW":
                raise ValueError(f"field, you can't assign mission with other status, only NEW")
                
            with conn.cursor(dictionary=True) as cursor:
                sql = """UPDATE missions SET assigned_agent_id = %s WHERE id = %s"""
                cursor.execute(sql, (a_id, m_id))

                conn.commit()
                assigned = cursor.rowcount > 0

                if assigned:
                    return {"msg": f"mission id {m_id} assign_mission successfully."}
                return {"msg": f" failed. mission id {m_id} NOT assign_mission successfully."}

    @staticmethod
    def update_mission_status(id, status):
        mission = MissionDB.get_mission_by_id(id)
        current_status = mission["status"]

        if status == "ASSIGNED":
            if current_status != "NEW":
                raise ValueError(F"It is not possible to associate a task with a status other than New")
        
        if status == "IN_PROGRESS":
            if  current_status != "ASSIGNED":
                raise ValueError("You cannot start a task with a status other than ASSIGNED.")
            
        if status == "CANCELLED":
            if current_status != "NEW" or current_status != "ASSIGNED":
                raise ValueError("You can only cancel a task if the status is NEW or ASSIGNED .")

        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """UPDATE missions SET status = %s WHERE id = %s"""
                cursor.execute(sql, (status, id))

                conn.commit()
                status_apdated = cursor.rowcount > 0

                if status_apdated:
                    return {"msg": f"mission id {id} update_mission_status successfully."}
                return {"msg": f" failed. mission id {id} NOT update_mission_status successfully."}
            
    @staticmethod
    def get_open_missions_by_agent(id):
        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT * FROM missions WHERE assigned_agent_id = %s AND status in('IN_PROGRESS', 'ASSIGNED')"""
                cursor.execute(sql, (id,))

                result = cursor.fetchall()
                return result
            
    @staticmethod
    def count_all_missions():
        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT COUNT(*) AS total_missions FROM missions"""
                cursor.execute(sql)

                missions = cursor.fetchone()
                return missions
            
    @staticmethod
    def count_by_status(status):
        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT COUNT(*) AS total_by_status FROM missions WHERE status = %s"""
                cursor.execute(sql, (status,))

                result = cursor.fetchone()
                return result
            
    @staticmethod
    def count_open_missions():
        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT COUNT(*) AS open_missions FROM missions WHERE status in('IN_PROGRESS', 'ASSIGNED')"""
                cursor.execute(sql)

                result = cursor.fetchone()
                return result
            
    @staticmethod
    def count_critical_missions():
        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT COUNT(*) AS CRITICAL_missions FROM missions WHERE status = 'CRITICAL' """
                cursor.execute(sql)

                result = cursor.fetchone()
                return result
            
    @staticmethod
    def get_top_agent():
        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:     
                sql = """SELECT * FROM missions 
                ORDER BY completed_missions DESC
                 LIMIT 1 """   
                
                cursor.execute(sql)

                top_agen = cursor.fetchone()
                return top_agen