import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load trained model
model = load_model("model/skin_model.h5")

classes = [
    "akiec",
    "bcc",
    "bkl",
    "df",
    "mel",
    "nv",
    "vasc"
]

disease_names = {
    "akiec": "Actinic keratosis",
    "bcc": "Basal cell carcinoma",
    "bkl": "Benign keratosis",
    "df": "Dermatofibroma",
    "mel": "Melanoma",
    "nv": "Melanocytic nevus",
    "vasc": "Vascular lesion"
}

CONFIDENCE_THRESHOLD = 30


def predict_image(img_path):

    img = image.load_img(img_path, target_size=(224,224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0

    prediction = model.predict(img)

    confidence = float(np.max(prediction)) * 100

    # Reject low confidence images
    if confidence < CONFIDENCE_THRESHOLD:
        return "Invalid Image", confidence, "None", "Please upload a valid skin lesion image"

    index = np.argmax(prediction)

    if index >= len(classes):
        return "Invalid Image", confidence, "None", "Prediction error"

    code = classes[index]

    disease = disease_names.get(code, "Unknown Disease")

    return disease, confidence, "Detected", "Consult dermatologist if symptoms persist"