import mysql.connector

class DBConnection:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="127.0.0.1", 
            port=3306,
            user="root",
            password=1234,
            database="Intelligence_db"
        )
    
    @staticmethod
    def create_database():
        with DBConnection.get_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                CREATE DATABASE IF NOT EXISTS Intelligence_db
                  """
                cursor.execute(sql)
                conn.commit()
    
    @staticmethod
    def create_tables():
        with DBConnection.get_connection() as conn:
            with conn.cursor() as cursor:
                sql_agents = """
                CREATE TABLE IF NOT EXISTS agents(
                id PRIMARY KEY AUTO_INCREMENT, 
                name VARCHAR(50),
                specialty VARCHAR(50),
                is_active BOOLEAN DEFAULT TRUE,
                completed_missions INT DEFAULT 0,
                failed_missions INT DEFAULT 0,
                agent_rank ENUM(Junior, Senior, Commander)
                )
                        """
                
                sql_missions = """
                CREATE TABLE IF NOT EXISTS missions(
                id PRIMARY KEY AUTO_INCREMENT, 
                title VARCHAR(255),
                description TEXT,
                location VARCHAR(255),
                difficulty INT,
                importance INT,
                status ENUM(CANCELLED, FAILED, COMPLETED, IN_PROGRESS, ASSIGNED, NEW) DEFAULT NEW,
                risk_level VARCHAR(255),
                assigned_agent_id INT DEFAULT NULL
                )
                """
                cursor.execute(sql_agents)
                cursor.execute(sql_missions)

                conn.commit()
                