import streamlit as st
import requests

# Title
st.title("Fire Detection Web Application")

# Image upload
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    # Display the uploaded image
    st.image(uploaded_image, caption='Uploaded Image.', use_column_width=True)

    # Read file content
    img_bytes = uploaded_image.read()

    # Check that data is loaded
    st.write(f"File name: {uploaded_image.name}, Size: {len(img_bytes)} bytes")

    if st.button('Predict'):
        try:
            # Send file in request
            files = {'file': (uploaded_image.name, img_bytes, uploaded_image.type)}
            response = requests.post("http://api:8000/predict/", files=files)

            if response.status_code == 200:
                prediction = response.json()
                st.write(f"Prediction: {prediction['prediction']}")
                st.write(f"Confidence: {prediction['confidence']}")
            else:
                st.error(f"Error: Unable to get prediction (status code {response.status_code})")

        except Exception as e:
            st.error(f"Unexpected error: {e}")
