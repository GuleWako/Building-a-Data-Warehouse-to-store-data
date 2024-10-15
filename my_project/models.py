
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS detected_image (
    id serial PRIMARY KEY,
    image VARCHAR,
    class FLOAT,
    x_center FLOAT,
    y_center FLOAT,
    width FLOAT,
    height FLOAT,
    confidence FLOAT
);
"""

def create_detected_image_table(conn):
    with conn.cursor() as cursor:
        cursor.execute(CREATE_TABLE_QUERY)
        conn.commit()
