"""
SkySQL Intelligence Database Setup


"""

import mysql.connector
from mysql.connector import Error
import sys
import time
import random
from datetime import datetime, timedelta

class DatabaseSetup:
    """Professional database setup class for SkySQL Intelligence"""
    
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'port': 3306
        }
        self.db_name = 'skysql_intelligence'
    
    def create_connection(self):
        """Create connection to MariaDB server"""
        try:
            conn = mysql.connector.connect(**self.config)
            print("Connected to MariaDB server successfully")
            return conn
        except Error as err:
            print(f"Connection failed: {err}")
            return None

    def setup_database(self):
        """Main database setup method"""
        print("SkySQL Intelligence Database Setup")
        print("XAMPP MariaDB Configuration")
        print("=" * 50)
        
        conn = self.create_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        try:
            # Create database
            print("1. Creating database...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            cursor.execute(f"USE {self.db_name}")
            print("   Database 'skysql_intelligence' created")
            
            # Drop existing tables to avoid conflicts
            print("2. Dropping existing tables...")
            tables_to_drop = [
                'operational_metrics', 'flight_performance', 'aircraft_config', 
                'routes', 'airports', 'airlines'
            ]
            
            for table in tables_to_drop:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table}")
                except Error:
                    pass  # Table might not exist
            
            # Create tables with CORRECTED structure
            print("3. Creating tables...")
            
            tables_sql = [
                """
                CREATE TABLE IF NOT EXISTS airlines (
                    airline_id INT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    iata_code VARCHAR(3),
                    country VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB
                """,
                
                """
                CREATE TABLE IF NOT EXISTS airports (
                    airport_id INT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    city VARCHAR(50),
                    country VARCHAR(50),
                    iata_code VARCHAR(3),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB
                """,
                
                """
                CREATE TABLE IF NOT EXISTS routes (
                    route_id INT AUTO_INCREMENT PRIMARY KEY,
                    airline_code VARCHAR(3) NOT NULL,
                    source_airport VARCHAR(3) NOT NULL,
                    dest_airport VARCHAR(3) NOT NULL,
                    distance_km INT NOT NULL,
                    base_fuel_kg INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB
                """,
                
                """
                CREATE TABLE IF NOT EXISTS flight_performance (
                    performance_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    route_id INT,
                    flight_date DATE,
                    actual_fuel_kg DECIMAL(10, 2),
                    planned_fuel_kg DECIMAL(10, 2),
                    passengers_count INT,
                    efficiency_score DECIMAL(4, 3),
                    fuel_savings_kg DECIMAL(10, 2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (route_id) REFERENCES routes(route_id)
                ) ENGINE=InnoDB
                """,
                
                """
                CREATE TABLE IF NOT EXISTS aircraft_config (
                    config_id INT AUTO_INCREMENT PRIMARY KEY,
                    aircraft_model VARCHAR(50) NOT NULL,
                    fuel_efficiency DECIMAL(8, 4),  -- CORRECTED COLUMN NAME
                    seat_capacity INT,
                    max_range_km INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB
                """,
                
                """
                CREATE TABLE IF NOT EXISTS operational_metrics (
                    metric_id INT AUTO_INCREMENT PRIMARY KEY,
                    metric_date DATE NOT NULL,
                    total_flights INT,
                    avg_efficiency DECIMAL(4, 3),
                    total_fuel_used_kg DECIMAL(12, 2),
                    total_fuel_saved_kg DECIMAL(12, 2),
                    avg_passenger_load DECIMAL(5, 2),
                    on_time_performance DECIMAL(5, 2),
                    route_id INT,
                    airline_code VARCHAR(3),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB
                """
            ]
            
            table_names = ['airlines', 'airports', 'routes', 'flight_performance', 
                          'aircraft_config', 'operational_metrics']
            
            for i, sql in enumerate(tables_sql):
                cursor.execute(sql)
                print(f"   {table_names[i]} table created")
            
            # Insert sample data
            print("4. Inserting sample data...")
            self.insert_sample_data(cursor)
            
            conn.commit()
            print("Database setup completed successfully!")
            return True
            
        except Error as err:
            print(f"Setup error: {err}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def insert_sample_data(self, cursor):
        """Insert sample data with CORRECTED column names"""
        try:
            # Airlines data
            airlines_data = [
                (1, 'Qantas Airways', 'QF', 'Australia'),
                (2, 'Cathay Pacific', 'CX', 'Hong Kong'),
                (3, 'Singapore Airlines', 'SQ', 'Singapore'),
                (4, 'Lufthansa', 'LH', 'Germany'),
                (5, 'Emirates', 'EK', 'UAE'),
                (6, 'British Airways', 'BA', 'United Kingdom'),
                (7, 'Air France', 'AF', 'France'),
                (8, 'American Airlines', 'AA', 'United States'),
                (9, 'Delta Air Lines', 'DL', 'United States'),
                (10, 'United Airlines', 'UA', 'United States'),
                (11, 'Qatar Airways', 'QR', 'Qatar'),
                (12, 'Air New Zealand', 'NZ', 'New Zealand')
            ]
            
            cursor.executemany(
                "INSERT IGNORE INTO airlines (airline_id, name, iata_code, country) VALUES (%s, %s, %s, %s)",
                airlines_data
            )
            print("   Airlines data inserted")
            
            # Airports data
            airports_data = [
                (1, 'Sydney Kingsford Smith Airport', 'Sydney', 'Australia', 'SYD'),
                (2, 'Los Angeles International Airport', 'Los Angeles', 'United States', 'LAX'),
                (3, 'Hong Kong International Airport', 'Hong Kong', 'China', 'HKG'),
                (4, 'Heathrow Airport', 'London', 'United Kingdom', 'LHR'),
                (5, 'Changi Airport', 'Singapore', 'Singapore', 'SIN'),
                (6, 'Frankfurt Airport', 'Frankfurt', 'Germany', 'FRA'),
                (7, 'John F Kennedy International Airport', 'New York', 'United States', 'JFK'),
                (8, 'Dubai International Airport', 'Dubai', 'United Arab Emirates', 'DXB'),
                (9, 'Charles de Gaulle Airport', 'Paris', 'France', 'CDG'),
                (10, 'Tokyo Haneda Airport', 'Tokyo', 'Japan', 'HND')
            ]
            
            cursor.executemany(
                "INSERT IGNORE INTO airports (airport_id, name, city, country, iata_code) VALUES (%s, %s, %s, %s, %s)",
                airports_data
            )
            print("   Airports data inserted")
            
            # Routes data - matching the frontend display exactly
            routes_data = [
                # SYD to LAX - Qantas (multiple entries for different airlines)
                ('QF', 'SYD', 'LAX', 12051, 144000),
                ('QF', 'SYD', 'LAX', 12051, 144000),
                ('QF', 'SYD', 'LAX', 12051, 144000),
                # HKG to LHR - Cathay Pacific
                ('CX', 'HKG', 'LHR', 9625, 115000),
                ('CX', 'HKG', 'LHR', 9625, 115000),
                # SIN to SYD - Singapore Airlines
                ('SQ', 'SIN', 'SYD', 6302, 75500),
                ('SQ', 'SIN', 'SYD', 6302, 75500),
                ('SQ', 'SIN', 'SYD', 6302, 75500),
                # FRA to JFK - Lufthansa
                ('LH', 'FRA', 'JFK', 6200, 74500),
                ('LH', 'FRA', 'JFK', 6200, 74500),
                ('LH', 'FRA', 'JFK', 6200, 74500),
                # Additional routes for analytics
                ('EK', 'DXB', 'LHR', 5500, 82000),
                ('BA', 'LHR', 'JFK', 5536, 78500),
                ('AA', 'JFK', 'LAX', 3983, 48500),
                ('DL', 'JFK', 'LAX', 3983, 48200),
                ('UA', 'ORD', 'LAX', 2806, 34500),
                ('NZ', 'AKL', 'SYD', 2157, 28500),
                ('AF', 'CDG', 'JFK', 5834, 69800),
                ('QR', 'DOH', 'LHR', 5213, 76500)
            ]
            
            cursor.executemany(
                "INSERT INTO routes (airline_code, source_airport, dest_airport, distance_km, base_fuel_kg) VALUES (%s, %s, %s, %s, %s)",
                routes_data
            )
            print("   Flight routes inserted")
            
            # Aircraft configurations - CORRECTED column name: fuel_efficiency
            config_data = [
                ('Boeing 787-9', 0.0015, 290, 14140),
                ('Airbus A350-900', 0.0012, 315, 15000),
                ('Boeing 777-300ER', 0.0018, 396, 13650),
                ('Airbus A380', 0.0021, 853, 15200),
                ('Boeing 737 MAX', 0.0011, 204, 6570)
            ]
            
            cursor.executemany(
                "INSERT INTO aircraft_config (aircraft_model, fuel_efficiency, seat_capacity, max_range_km) VALUES (%s, %s, %s, %s)",
                config_data
            )
            print("   Aircraft configurations inserted")
            
            # Generate flight performance data with fuel savings
            print("   Generating flight performance data...")
            self.generate_performance_data(cursor)
            
            # Generate operational metrics with enhanced fields
            print("   Generating operational metrics...")
            self.generate_operational_metrics(cursor)
            
            return True
            
        except Error as e:
            print(f"Error inserting sample data: {e}")
            return False

    def generate_performance_data(self, cursor):
        """Generate realistic flight performance data with fuel savings"""
        cursor.execute("SELECT route_id, base_fuel_kg FROM routes")
        routes = cursor.fetchall()
        
        start_date = datetime.now() - timedelta(days=90)
        
        performance_data = []
        
        for route in routes:
            route_id, base_fuel = route
            num_flights = random.randint(2, 6)  # Fewer flights to avoid duplicates
            
            for i in range(num_flights):
                flight_date = start_date + timedelta(days=random.randint(0, 89), 
                                                   hours=random.randint(0, 23))
                actual_fuel = base_fuel * random.uniform(0.82, 1.08)
                efficiency = random.uniform(0.75, 0.98)
                fuel_savings = base_fuel - actual_fuel if actual_fuel < base_fuel else 0
                
                performance_data.append((
                    route_id,
                    flight_date.date(),
                    round(actual_fuel, 2),
                    base_fuel,
                    random.randint(180, 350),
                    round(efficiency, 3),
                    round(fuel_savings, 2)
                ))
        
        # Insert all performance data
        cursor.executemany("""
            INSERT INTO flight_performance 
            (route_id, flight_date, actual_fuel_kg, planned_fuel_kg, passengers_count, efficiency_score, fuel_savings_kg)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, performance_data)
        
        print(f"   Generated {len(performance_data)} flight performance records")

    def generate_operational_metrics(self, cursor):
        """Generate operational metrics data with enhanced fields"""
        cursor.execute("SELECT route_id, airline_code FROM routes LIMIT 5")
        routes = cursor.fetchall()
        
        operational_data = []
        
        for i in range(6):  # Last 6 days of metrics
            metric_date = datetime.now() - timedelta(days=(5 - i))
            
            for route in routes:
                route_id, airline_code = route
                
                operational_data.append((
                    metric_date.date(),
                    random.randint(2, 8),
                    round(random.uniform(0.75, 0.95), 3),
                    round(random.uniform(800000, 1200000), 2),
                    round(random.uniform(5000, 25000), 2),
                    round(random.uniform(0.75, 0.92), 2),
                    round(random.uniform(0.82, 0.96), 2),
                    route_id,
                    airline_code
                ))
        
        # Insert all operational metrics
        cursor.executemany("""
            INSERT INTO operational_metrics 
            (metric_date, total_flights, avg_efficiency, total_fuel_used_kg, total_fuel_saved_kg, 
             avg_passenger_load, on_time_performance, route_id, airline_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, operational_data)
        
        print(f"   Generated {len(operational_data)} operational metric records")

    def verify_setup(self):
        """Verify the database setup with CORRECTED column names"""
        conn = self.create_connection()
        if not conn:
            return False
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(f"USE {self.db_name}")
            
            print("\nDATABASE VERIFICATION")
            print("=" * 50)
            
            # Table counts
            tables = ['airlines', 'airports', 'routes', 'flight_performance', 
                     'aircraft_config', 'operational_metrics']
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                count = cursor.fetchone()['count']
                print(f"  {table:20} : {count:6} records")
            
            # Sample data verification
            print("\nSAMPLE DATA VERIFICATION:")
            print("-" * 30)
            
            # Check routes match frontend
            cursor.execute("""
                SELECT r.route_id, r.airline_code, r.source_airport, r.dest_airport, 
                       r.distance_km, r.base_fuel_kg, a.name as airline_name
                FROM routes r
                LEFT JOIN airlines a ON r.airline_code = a.iata_code
                ORDER BY r.distance_km DESC
                LIMIT 5
            """)
            routes = cursor.fetchall()
            
            print("Top Routes:")
            for route in routes:
                print(f"  {route['source_airport']} to {route['dest_airport']} "
                      f"({route['airline_code']}) - {route['distance_km']}km")
            
            # Check aircraft config - CORRECTED column name
            cursor.execute("SELECT aircraft_model, fuel_efficiency FROM aircraft_config LIMIT 3")
            aircraft = cursor.fetchall()
            
            print("\nAircraft Configurations:")
            for ac in aircraft:
                print(f"  {ac['aircraft_model']}: {ac['fuel_efficiency']}")
            
            # Check performance data
            cursor.execute("""
                SELECT AVG(efficiency_score) as avg_efficiency, 
                       COUNT(*) as total_flights 
                FROM flight_performance
            """)
            perf = cursor.fetchone()
            print(f"\nPerformance Stats: {perf['total_flights']} flights, "
                  f"avg efficiency: {perf['avg_efficiency']:.3f}")
            
            print("\nDatabase setup verified successfully!")
            return True
            
        except Error as e:
            print(f"Verification failed: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

def main():
    """Main execution function"""
    start_time = time.time()
    
    setup = DatabaseSetup()
    success = setup.setup_database()
    
    if success:
        setup.verify_setup()
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"\nSetup time: {elapsed:.2f} seconds")
    
    if success:
        print("\n🎉 SkySQL Intelligence is ready!")
        print("\nNext steps:")
        print("1. Start backend: python app1.py")
        print("2. Start frontend: python -m http.server 3000 (in frontend directory)")
        print("3. Access dashboard: http://localhost:3000/dashboard.html")
        print("\nBackend API endpoints available:")
        print("  - http://localhost:8000/api/health")
        print("  - http://localhost:8000/api/routes") 
        print("  - http://localhost:8000/api/analyze/route/1")
        print("  - http://localhost:8000/api/metrics")
    else:
        print("Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()