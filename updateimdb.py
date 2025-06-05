import mysql.connector

def get_tracking_report(package_ids):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        placeholders = ', '.join(['%s'] * len(package_ids))

        select_query = f"""
            SELECT
                scans.package_id,
                scans.timestamp,
                scans.action,
                addresses.address
            FROM scans
            JOIN addresses ON scans.address_id = addresses.id
            WHERE scans.drop = 'Drop'
              AND scans.package_id IN ({placeholders})
            ORDER BY scans.package_id, scans.timestamp;
        """

        cursor.execute(select_query, tuple(package_ids))
        records = cursor.fetchall()

        print(" Printing Tracking Report")
        for row in records:
            print("Package ID:", row[0])
            print("Timestamp:", row[1])
            print("Action:", row[2])
            print("Address:", row[3])
            print("_" * 40)

        close_connection(connection)

    except (Exception, mysql.connector.Error) as error:
        print("No data available", error)
        return

print("Example 1: Print Database version")
read_database_version()

print("Example 2: Information about drivers")
get_driver_detail(5)

print("Example 3: Tracking report")
get_tracking_report(1)

