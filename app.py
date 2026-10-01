import streamlit as st
import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO

st.set_page_config(page_title="Pothole Detection System", layout="wide")

st.title("Pothole Detection and Classification")

model = YOLO("best.pt")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    results = model(image)
    result = results[0]

    annotated_image = result.plot()
    st.image(annotated_image, channels="BGR", use_column_width=True)

    data = []

    if result.masks is not None:
        masks = result.masks.data.cpu().numpy()

        for i, mask in enumerate(masks):
            area = np.sum(mask)

            if area < 5000:
                size = "Small"
            elif area < 15000:
                size = "Medium"
            else:
                size = "Large"

            data.append({
                "Pothole ID": i + 1,
                "Detection Result": "Pothole",
                "Area (pixels)": int(area),
                "Size Classification": size
            })

    df = pd.DataFrame(data)
    st.subheader("Detection Results")
    st.dataframe(df)