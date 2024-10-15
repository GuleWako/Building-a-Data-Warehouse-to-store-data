
from fastapi import FastAPI, HTTPException, Depends
from database import connect_to_database
from schemas import DetectedImage, DetectedImageCreate
from crud import create_detected_image, get_detected_images

app = FastAPI()

# Dependency to get the database connection
def get_db():
    conn = connect_to_database()
    try:
        yield conn
    finally:
        conn.close()

@app.post("/detected_images/", response_model=DetectedImage)
def add_detected_image(detected_image: DetectedImageCreate, conn=Depends(get_db)):
    image_id = create_detected_image(conn, detected_image)
    if not image_id:
        raise HTTPException(status_code=400, detail="Image creation failed.")
    return {**detected_image.dict(), "id": image_id}

@app.get("/detected_images/", response_model=list[DetectedImage])
def read_detected_images(conn=Depends(get_db)):
    images = get_detected_images(conn)
    return images
