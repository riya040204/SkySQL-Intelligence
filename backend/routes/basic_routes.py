"""
Basic API routes for SkySQL Intelligence
"""
from flask import jsonify
from datetime import datetime

def setup_basic_routes(app, db, ensure_operational_metrics_func):
    @app.route('/')
    def api_root():
        return jsonify({
            "api": "SkySQL Intelligence",
            "version": "1.0.0",
            "description": "Professional Airline Operational Efficiency Analytics Platform",
            "database": "MariaDB",
            "timestamp": datetime.now().isoformat(),
            "status": "operational"
        })

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Comprehensive health check endpoint"""
        try:
            # Test database connection
            test_query = db.execute_query("SELECT 1 as status")
            
            if test_query:
                # Ensure operational metrics data exists
                metrics_ready = ensure_operational_metrics_func()
                
                # Get basic database stats
                stats = db.execute_query("""
                    SELECT 
                        (SELECT COUNT(*) FROM airlines) as airline_count,
                        (SELECT COUNT(*) FROM airports) as airport_count,
                        (SELECT COUNT(*) FROM routes) as route_count,
                        (SELECT COUNT(*) FROM flight_performance) as flight_count,
                        (SELECT COUNT(*) FROM operational_metrics) as metrics_count
                """)
                
                health_status = {
                    "status": "healthy",
                    "database": "connected",
                    "operational_metrics": "ready" if metrics_ready else "generating",
                    "timestamp": datetime.now().isoformat(),
                    "statistics": stats[0] if stats else {},
                    "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                return jsonify(health_status)
            else:
                return jsonify({
                    "status": "unhealthy",
                    "database": "disconnected",
                    "timestamp": datetime.now().isoformat(),
                    "error": "Database connection test failed"
                }), 503
                
        except Exception as e:
            print(f"Health check failed: {e}")
            return jsonify({
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }), 500

    @app.route('/api/debug/tables', methods=['GET'])
    def debug_tables():
        """Debug endpoint to check table structure"""
        try:
            tables = db.execute_query("""
                SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = 'skysql_intelligence'
                ORDER BY TABLE_NAME, ORDINAL_POSITION
            """)
            
            return jsonify({
                "database": "skysql_intelligence",
                "tables": tables or [],
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            "error": "Endpoint not found",
            "timestamp": datetime.now().isoformat(),
            "documentation": "See / for available endpoints"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        print(f"Internal server error: {error}")
        return jsonify({
            "error": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }), 500
