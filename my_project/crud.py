from database import connect_to_database

def create_detected_image(conn, detected_image):
    query = """
    INSERT INTO detected_image (image, class, x_center, y_center, width, height, confidence)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (
            detected_image.image, detected_image.class_, detected_image.x_center,
            detected_image.y_center, detected_image.width, detected_image.height,
            detected_image.confidence
        ))
        conn.commit()
        return cursor.fetchone()[0]

def get_detected_images(conn):
    query = "SELECT * FROM detected_image;"
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()
