from ultralytics import YOLO


# Load a pretrained YOLO model (recommended for training)
model = YOLO("yolo26s.pt")

# Train the model using the 'coco8.yaml' dataset for 3 epochs
results = model.train(data="vid/data.yaml", epochs=6000,val=False)

# Evaluate the model's performance on the validation set
results = model.val()

# Perform object detection on an image using the model
results = model("https://ultralytics.com/images/bus.jpg")

# Export the model to ONNX format
model.export(format="onnx", dynamic=True)
