from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image, UnidentifiedImageError
import io
import numpy as np
from tensorflow.keras.models import load_model
import logging

app = FastAPI()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Loading the model
try:
    model = load_model('./models/fire_detection_model.h5')
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load the model: {str(e)}")
    raise HTTPException(status_code=500, detail="Failed to load the model.")

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename} with content type {file.content_type}")
    
    if file.content_type not in ["image/jpeg", "image/png"]:
        logger.error(f"Unsupported file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Unsupported file type. Only JPEG and PNG are supported.")

    try:
        # Reading the file content
        file_data = await file.read()
        logger.info(f"File size: {len(file_data)} bytes")

        if len(file_data) == 0:
            logger.error("Empty file received.")
            raise HTTPException(status_code=400, detail="Empty file received.")

        # Writing file for verification
        with open("uploaded_file_check.jpg", "wb") as f:
            f.write(file_data)

        # Opening the image with PIL
        image = Image.open(io.BytesIO(file_data))
        image = image.convert("RGB")
        image = image.resize((150, 150))  # Resizing the image

    except UnidentifiedImageError as e:
        logger.error(f"Unidentified image error: {str(e)}")
        raise HTTPException(status_code=400, detail="Cannot identify the image file.")
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    # Converting the image to a numpy array
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    try:
        # Get prediction
        prediction = model.predict(img_array)[0][0]
        result = "Fire" if prediction > 0.5 else "No fire"
        logger.info(f"Prediction: {result} with confidence {prediction * 100:.2f}%")
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    return {"prediction": result, "confidence": f"{prediction * 100:.2f}%"}
