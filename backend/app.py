"""
SkySQL Intelligence Backend API - MODULAR VERSION
Professional Airline Efficiency Analytics Platform
"""
from flask import Flask
from flask_cors import CORS
import logging
import sys
from datetime import datetime

# Import modular components
from database_manager import DatabaseManager
from utils import ensure_operational_metrics
from routes.basic_routes import setup_basic_routes
from routes.data_routes import setup_data_routes
from routes.analytics_routes import setup_analytics_routes

# Professional logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize database manager
db = DatabaseManager()

# Setup all routes
setup_basic_routes(app, db, ensure_operational_metrics)
setup_data_routes(app, db)
setup_analytics_routes(app, db, ensure_operational_metrics)

def main():
    """Main application entry point"""
    print("=" * 70)
    print("SkySQL Intelligence API Server - MODULAR VERSION")
    print("All Endpoints Working - Split into Modular Components")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Database: MariaDB (XAMPP)")
    print("API Base: http://localhost:8000")
    print("Health Check: http://localhost:8000/api/health")
    print("=" * 70)
    
    # Test database connection on startup
    conn = db.get_connection()
    if conn:
        print("‚úÖ Database connection: SUCCESS")
        
        # Ensure operational metrics are ready
        print("Ì≥ä Checking operational metrics...")
        if ensure_operational_metrics(db):
            print("‚úÖ Operational metrics: READY")
        else:
            print("‚ö†Ô∏è  Operational metrics: USING FALLBACK DATA")
        
        # Display basic stats
        stats = db.execute_query("""
            SELECT 
                (SELECT COUNT(*) FROM routes) as routes,
                (SELECT COUNT(*) FROM flight_performance) as flights,
                (SELECT COUNT(*) FROM airlines) as airlines,
                (SELECT COUNT(*) FROM operational_metrics) as metrics_count
        """)
        
        if stats:
            print(f"Ì≥ä Database stats: {stats[0]['routes']} routes, "
                  f"{stats[0]['flights']} flights, {stats[0]['airlines']} airlines, "
                  f"{stats[0]['metrics_count']} metrics records")
        
        if conn and conn.is_connected():
            conn.close()
    else:
        print("‚ùå Database connection: FAILED")
        print("Please ensure:")
        print("  - XAMPP MySQL service is running")
        print("  - Database 'skysql_intelligence' exists")
        print("  - Connection credentials are correct")
    
    print("Server starting...")
    print("-" * 70)

if __name__ == '__main__':
    main()
    
    try:
        app.run(host='0.0.0.0', port=8000, debug=False)
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
