import logging
from database.db_connection import DBConnection


class AgentDB:
    @staticmethod
    def create_agent(data):
        with DBConnection.get_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO agents (name, specialty, agent_rank) VALUES (%s, %s, %s)
                """
                values = list(data.values())
                cursor.execute(sql, values)
                
                conn.commit()
                new_id = cursor.lastrowid
                logging.info(f"agent id {new_id} added.")

                agent = AgentDB.get_agent_by_id(new_id)
                return agent
            
    @staticmethod
    def get_all_agents():
        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT * FROM agents"""
                cursor.execute(sql)

                agents = cursor.fetchall()
                return agents
            
    @staticmethod
    def get_agent_by_id(id):
        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT * FROM agents WHERE id = %s"""
                cursor.execute(sql, (id,))

                agent = cursor.fetchone()
                return agent
            
    @staticmethod
    def update_agent(id, data):
        with DBConnection.get_connection() as conn:
            with conn.cursor() as cursor:
                cause_list = [f"{key}=%s" for key in data.keys()]
                cause_txt = ", ".join(cause_list)

                sql = f"UPDATE agents SET {cause_txt} WHERE id = %s"
                values = list(data.values()) + [id]

                cursor.execute(sql, values)
                conn.commit()

                updated = cursor.rowcount > 0
                return updated

    
    @staticmethod
    def deactivate_agent(id):
        with DBConnection.get_connection() as conn:
            with conn.cursor() as cursor:
                sql = """UPDATE agents SET is_active = FALSE WHERE id =%s"""
                cursor.execute(sql, (id,))

                conn.commit()
                changed = cursor.rowcount > 0
                return changed

    @staticmethod
    def increment_completed(id):
        with DBConnection.get_connection() as conn:
            with conn.cursor() as cursor:
                sql = """UPDATE agents SET completed_missions = completed_missions + 1 WHERE id =%s"""
                cursor.execute(sql, (id,))

                conn.commit()
                changed = cursor.rowcount > 0

                if changed:
                    return {"msg": f"id {id} increment_completed successfully."}
                return {"msg": f" failed. id {id} NOT increment_completed successfully."}
            
    @staticmethod
    def increment_failed(id):
        with DBConnection.get_connection() as conn:
            with conn.cursor() as cursor:
                sql = """UPDATE agents SET failed_missions = failed_missions + 1 WHERE id =%s"""
                cursor.execute(sql, (id,))

                conn.commit()
                changed = cursor.rowcount > 0

                if changed:
                    return {"msg": f"id {id} increment_failed successfully."}
                return {"msg": f" failed. id {id} NOT increment_failed successfully."}
            
    @staticmethod
    def get_agent_performance(id):
        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT completed_missions AS completed, failed_missions AS failed FROM agents WHERE id = %s"""
                cursor.execute(sql, (id,))

                report_dict = cursor.fetchone()
                total = report_dict["completed"] + report_dict["failed"]
                if total <= 0:
                    success_rate = 0
                else:
                    total = report_dict["completed"] + report_dict["failed"]

                
                success_rate = (report_dict["completed"] / total) * 100

                report_dict["total"] = total
                report_dict["success_rate"] = success_rate

                return report_dict

    @staticmethod
    def count_active_agents():
        with DBConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = "SELECT COUNT(*) AS active_agents_count FROM agents WHERE is_active = TRUE"
                cursor.execute(sql)

                result = cursor.fetchone()
                return result
