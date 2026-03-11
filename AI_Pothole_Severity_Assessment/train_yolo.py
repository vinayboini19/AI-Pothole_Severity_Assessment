from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov11n.pt")

# Train the model
model.train(
    data="data.yaml",
    epochs=50,
    imgsz=640
)
model.val()
# Run prediction
model.predict(source="test/images", save=True)