import logging
import mysql.connector


class DBConnection:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="1234",
            database="Intelligence_db",
        )

    @staticmethod
    def create_database():
        logging.debug("run the create_database func")
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="1234",
        )
        cursor = conn.cursor()

        sql = "CREATE DATABASE IF NOT EXISTS Intelligence_db"
        cursor.execute(sql)
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def create_tables():
        logging.debug("run the create_tables func")

        with DBConnection.get_connection() as conn:
            with conn.cursor() as cursor:
                sql_agents = """
                CREATE TABLE IF NOT EXISTS agents(
                id INT PRIMARY KEY AUTO_INCREMENT, 
                name VARCHAR(50),
                specialty VARCHAR(50),
                is_active BOOLEAN DEFAULT TRUE,
                completed_missions INT DEFAULT 0,
                failed_missions INT DEFAULT 0,
                agent_rank ENUM('Junior', 'Senior', 'Commander') NOT NULL
                )
                        """

                sql_missions = """
                CREATE TABLE IF NOT EXISTS missions(
                id INT PRIMARY KEY AUTO_INCREMENT, 
                title VARCHAR(255),
                description TEXT,
                location VARCHAR(255),
                difficulty INT,
                importance INT,
                status ENUM('CANCELLED', 'FAILED', 'COMPLETED', 'IN_PROGRESS', 'ASSIGNED', 'NEW') DEFAULT 'NEW',
                risk_level VARCHAR(255),
                assigned_agent_id INT DEFAULT NULL,
                check (difficulty BETWEEN 1 AND 10 AND importance BETWEEN 1 AND 10)
                )
                """
                cursor.execute(sql_agents)
                cursor.execute(sql_missions)

                conn.commit()
