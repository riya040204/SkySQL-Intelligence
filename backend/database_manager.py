"""
Database Manager for SkySQL Intelligence
Handles all MariaDB connections and queries
"""
import mysql.connector
from mysql.connector import Error
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Professional MariaDB database management
    Enhanced error handling and connection management
    """
    
    def __init__(self):
        # XAMPP MariaDB configuration
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "skysql_intelligence",
            "port": 3306,
            "charset": 'utf8mb4',
            "autocommit": True
        }
    
    def get_connection(self):
        """Establish database connection with robust error handling"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            logger.info("Database connection established successfully")
            return conn
        except Error as e:
            logger.error(f"Database connection failed: {e}")
            return None
    
    def execute_query(self, query, params=None, fetch=True):
        """
        Execute database queries with professional error handling
        Returns results or None on error
        """
        conn = self.get_connection()
        if not conn:
            return None
            
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                logger.debug(f"Query executed successfully: {len(result)} rows returned")
            else:
                conn.commit()
                result = cursor.lastrowid or True
                
            return result
            
        except Error as e:
            logger.error(f"Query execution error: {e}")
            if conn.is_connected():
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
