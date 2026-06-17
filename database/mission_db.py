from database.db_connection import DBConnection

class MissionDB:
    @staticmethod
    def create_mission(data):
        with DBConnection.get_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO missions (title, description, location, difficulty, importance) VALUES (%s, %s, %s, %s, %s)
                """
                values = list(data.values())
                cursor.execute(sql, values)
                
                conn.commit()
                new_id = cursor.lastrowid

                mission = MissionDB.get_agent_by_id(new_id)
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
                sql = """SELECT * FROM missions WHERE assigned_agent_id = %s"""
                cursor.execute(sql, (id,))

                result = cursor.fetchone()
                return result
            
    @staticmethod
    def count_all_missions():
        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT COUNT(*) AS total_missions FROM missions"""
                cursor.execute(sql)

                missions = cursor.fetchall()
                return missions
            
