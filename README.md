# ♻️ EcoSort: Waste Classifier Sustainability App

Welcome to **EcoSort**, an interactive web app that classifies waste materials from images and educates users about their environmental impact — all powered by a model trained on [Teachable Machine](https://teachablemachine.withgoogle.com/).



## Features

- **Image-Based Waste Classification**  
  Upload an image of waste and get an instant classification (e.g., plastic, cardboard, metal, etc.).

- **Machine Learning Model**  
  Built using **Teachable Machine** and integrated with **TensorFlow/Keras**.

- **Carbon Emission Insights**  
  Get detailed and engaging information about the carbon footprint and recyclability of the material.

- **Sustainable Tips**  
  Each classification comes with a sustainability tip.
---

## Model Training

The model was trained using Google's **Teachable Machine**:
- Multi-class image classification
- Trained to recognize: **cardboard, plastic, glass, metal, paper, trash**
- Exported as a `.h5` model and integrated into the app with `keras` and `PIL`

---

## Tech Stack

| Tool               | Purpose                         |
|--------------------|---------------------------------|
| `Streamlit`        | Web application frontend        |
| `Teachable Machine`| Model training platform         |
| `TensorFlow/Keras` | Model loading + inference       |
| `Pillow (PIL)`     | Image preprocessing             |
| `NumPy`            | Image normalization and handling|

---

## How It Works

1. User uploads an image of a waste item.
2. The model predicts the material type.
3. Based on the result:
   - Carbon emission facts are shown.
   - SDG-related tips are displayed.
