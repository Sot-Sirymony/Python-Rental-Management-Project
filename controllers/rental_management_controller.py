# File: controllers/rental_management_controller.py
from sqlite3 import connect

def set_rental_price_and_terms(room_id, rental_price, payment_frequency, security_deposit, grace_period):
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        UPDATE Room
        SET rental_price = ?,
            payment_frequency = ?,
            security_deposit = ?,
            grace_period = ?
        WHERE id = ?
        """, (rental_price, payment_frequency, security_deposit, grace_period, room_id))
        connection.commit()
    except Exception as e:
        print(f"Error setting rental terms: {e}")
    finally:
        connection.close()
        
def update_tenant_for_room(room_id, tenant_id):
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        UPDATE Room
        SET tenant_id = ?
        WHERE id = ?
        """, (tenant_id, room_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating tenant for room: {e}")
        raise
    finally:
        connection.close()          

def update_occupancy_status(room_id, status):
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        UPDATE Room
        SET occupancy_status = ?
        WHERE id = ?
        """, (status, room_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating occupancy status: {e}")
    finally:
        connection.close()
def fetch_room_details():
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        # Query to fetch room details along with tenant information
        cursor.execute("""
        SELECT 
            Room.id, 
            Room.name, 
            Room.type, 
            Room.rental_price, 
            Room.payment_frequency,
            Room.security_deposit, 
            Room.grace_period, 
            Room.occupancy_status,
            COALESCE(Tenant.first_name || ' ' || Tenant.last_name, 'No Tenant') AS tenant_name
        FROM Room
        LEFT JOIN Tenant ON Room.tenant_id = Tenant.id
        """)
        # Fetch and return all rows
        return cursor.fetchall()
    except Exception as e:
        # Print error details for debugging
        print(f"Error fetching room details: {e}")
        return []
    finally:
        # Ensure the database connection is closed
        connection.close()
       
def fetch_room_details_with_booking():
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT
            r.id, r.name, r.type, r.rental_price, r.payment_frequency, 
            r.security_deposit, r.grace_period, r.occupancy_status, 
            t.first_name || ' ' || t.last_name AS tenant_name,
            CASE
                WHEN b.status IS NULL THEN r.occupancy_status
                ELSE b.status
            END AS dynamic_status -- Dynamic status based on bookings
        FROM Room r
        LEFT JOIN Tenant t ON r.tenant_id = t.id
        LEFT JOIN (
            SELECT room_id, status
            FROM Booking
            WHERE status IN ('Pending', 'Active') -- Only consider relevant booking statuses
        ) b ON r.id = b.room_id;
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching room details with booking info: {e}")
        return []
    finally:
        connection.close() 
        
def fetch_room_details_with_booking_and_payment():
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT
            r.id AS room_id,
            r.name AS room_name,
            r.type AS room_type,
            r.rental_price,
            r.payment_frequency,
            r.security_deposit,
            r.grace_period,
            r.occupancy_status,
            COALESCE(t.first_name || ' ' || t.last_name, 'No Tenant') AS tenant_name,
            CASE
                WHEN b.status IS NULL THEN r.occupancy_status
                ELSE b.status
            END AS dynamic_status, -- Dynamic status based on bookings
            COALESCE(SUM(p.amount), 0) AS total_payments, -- Total payment amount
            MAX(p.date) AS last_payment_date -- Last payment date
        FROM Room r
        LEFT JOIN Tenant t ON r.tenant_id = t.id
        LEFT JOIN (
            SELECT room_id, status
            FROM Booking
            WHERE status IN ('Pending', 'Active') -- Only consider relevant booking statuses
        ) b ON r.id = b.room_id
        LEFT JOIN Payment p ON r.id = p.room_id -- Join with Payment table
        GROUP BY r.id, r.name, r.type, r.rental_price, r.payment_frequency,
                 r.security_deposit, r.grace_period, r.occupancy_status,
                 t.first_name, t.last_name, b.status
        ORDER BY r.id; -- Order by Room ID
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching room details with booking and payment info: {e}")
        return []
    finally:
        connection.close()
        
        
def create_lease(room_id, tenant_id, start_date, end_date):
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        # Insert the lease
        cursor.execute("""
        INSERT INTO Lease (room_id, tenant_id, start_date, end_date)
        VALUES (?, ?, ?, ?)
        """, (room_id, tenant_id, start_date, end_date))
        
        # Update the room's occupancy status
        cursor.execute("""
        UPDATE Room
        SET occupancy_status = 'Rented', tenant_id = ?
        WHERE id = ?
        """, (tenant_id, room_id))
        
        connection.commit()
    except Exception as e:
        print(f"Error creating lease: {e}")
        raise
    finally:
        connection.close()
def fetch_leases(room_id=None, tenant_id=None):
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        query = """
        SELECT l.id, r.name AS room_name, t.first_name || ' ' || t.last_name AS tenant_name,
               l.start_date, l.end_date, l.status
        FROM Lease l
        JOIN Room r ON l.room_id = r.id
        JOIN Tenant t ON l.tenant_id = t.id
        WHERE 1=1
        """
        params = []
        if room_id:
            query += " AND l.room_id = ?"
            params.append(room_id)
        if tenant_id:
            query += " AND l.tenant_id = ?"
            params.append(tenant_id)
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching leases: {e}")
        return []
    finally:
        connection.close()
        
def update_lease(lease_id, start_date, end_date, status):
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        UPDATE Lease
        SET start_date = ?, end_date = ?, status = ?
        WHERE id = ?
        """, (start_date, end_date, status, lease_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating lease: {e}")
        raise
    finally:
        connection.close()
       
        
        
     
