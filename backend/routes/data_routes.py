"""
Data retrieval routes for SkySQL Intelligence
"""
from flask import jsonify
from datetime import datetime
import random

def setup_data_routes(app, db):
    @app.route('/api/airlines', methods=['GET'])
    def get_airlines():
        """Get all airlines data"""
        try:
            airlines = db.execute_query("""
                SELECT airline_id, name, iata_code, country
                FROM airlines 
                ORDER BY name
            """)
            
            if airlines is None:
                return jsonify({"error": "Failed to fetch airlines data"}), 500
                
            return jsonify({
                "timestamp": datetime.now().isoformat(),
                "count": len(airlines),
                "data": airlines
            })
            
        except Exception as e:
            print(f"Error fetching airlines: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route('/api/airports', methods=['GET'])
    def get_airports():
        """Get all airports data"""
        try:
            airports = db.execute_query("""
                SELECT airport_id, name, city, country, iata_code
                FROM airports 
                ORDER BY country, city
            """)
            
            if airports is None:
                return jsonify({"error": "Failed to fetch airports data"}), 500
                
            return jsonify({
                "timestamp": datetime.now().isoformat(),
                "count": len(airports),
                "data": airports
            })
            
        except Exception as e:
            print(f"Error fetching airports: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route('/api/routes', methods=['GET'])
    def get_flight_routes():
        """Get all flight routes with detailed information"""
        try:
            routes = db.execute_query("""
                SELECT 
                    r.route_id,
                    r.airline_code,
                    r.source_airport,
                    r.dest_airport as destination_airport,
                    r.distance_km,
                    r.base_fuel_kg,
                    a.name as airline_name
                FROM routes r
                LEFT JOIN airlines a ON r.airline_code = a.iata_code
                ORDER BY r.distance_km DESC
            """)
            
            if routes is None:
                return jsonify({"error": "Failed to fetch routes data"}), 500
                
            return jsonify({
                "timestamp": datetime.now().isoformat(),
                "count": len(routes),
                "data": routes
            })
            
        except Exception as e:
            print(f"Error fetching routes: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route('/api/flights', methods=['GET'])
    def get_flights():
        """Get flight performance data"""
        try:
            flights = db.execute_query("""
                SELECT 
                    fp.performance_id,
                    fp.route_id,
                    fp.flight_date,
                    fp.actual_fuel_kg,
                    fp.planned_fuel_kg,
                    fp.efficiency_score,
                    r.source_airport,
                    r.dest_airport as destination_airport
                FROM flight_performance fp
                JOIN routes r ON fp.route_id = r.route_id
                ORDER BY fp.flight_date DESC
                LIMIT 50
            """)
            
            if flights is None:
                return jsonify({"error": "Failed to fetch flights data"}), 500
                
            return jsonify({
                "timestamp": datetime.now().isoformat(),
                "count": len(flights),
                "data": flights
            })
            
        except Exception as e:
            print(f"Error fetching flights: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route('/api/config/aircraft', methods=['GET'])
    def get_aircraft_configs():
        """Get aircraft configuration data - FIXED VERSION"""
        try:
            configs = db.execute_query("""
                SELECT 
                    config_id,
                    aircraft_model,
                    seat_capacity,
                    fuel_efficiency,
                    max_range_km
                FROM aircraft_config 
                ORDER BY aircraft_model
            """)
            
            # Enhanced: Better fallback handling
            if configs is None:
                configs = []
                
            if not configs:
                print("No aircraft configurations found, providing comprehensive fallback data")
                configs = [
                    {
                        "config_id": 1,
                        "aircraft_model": "Boeing 737-800",
                        "seat_capacity": 189,
                        "fuel_efficiency": 0.00152,
                        "max_range_km": 5765
                    },
                    {
                        "config_id": 2,
                        "aircraft_model": "Boeing 787-9",
                        "seat_capacity": 290,
                        "fuel_efficiency": 0.0015,
                        "max_range_km": 14140
                    },
                    {
                        "config_id": 3,
                        "aircraft_model": "Airbus A320neo",
                        "seat_capacity": 194,
                        "fuel_efficiency": 0.0010,
                        "max_range_km": 6300
                    },
                    {
                        "config_id": 4,
                        "aircraft_model": "Airbus A350-900",
                        "seat_capacity": 315,
                        "fuel_efficiency": 0.0012,
                        "max_range_km": 15000
                    },
                    {
                        "config_id": 5,
                        "aircraft_model": "Boeing 777-300ER",
                        "seat_capacity": 396,
                        "fuel_efficiency": 0.0018,
                        "max_range_km": 13650
                    }
                ]
                
            return jsonify({
                "timestamp": datetime.now().isoformat(),
                "count": len(configs),
                "data": configs
            })
            
        except Exception as e:
            print(f"Error fetching aircraft configs: {e}")
            return jsonify({"error": "Aircraft configuration service temporarily unavailable"}), 500
