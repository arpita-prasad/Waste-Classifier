from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import streamlit as st
import os

st.set_page_config(layout='wide')

@st.cache_resource
def load_my_model():
    return load_model("keras_model.h5", compile=False)

model = load_my_model()

def classify_waste(img):
    np.set_printoptions(suppress=True)

    # loading the labels
    class_names = open("labels.txt", "r").readlines()

    # creating the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = img.convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turning the image into a numpy array
    image_array = np.asarray(image)

    # normalizing the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # loading the image into the array
    data[0] = normalized_image_array

    # prediction
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    return class_name, confidence_score

def carbon_info(label):
    info = {
        "cardboard": (
            "♻️ **Cardboard**\n"
            "\nProducing cardboard emits around **0.94 kg of CO₂ per kilogram**. "
            "However, it's one of the most recyclable materials. Recycling cardboard saves trees, water, and about 75% of the energy needed to produce new cardboard. "
            "When disposed of properly, it has a relatively low environmental impact.\n\n"
            "🌍 **Sustainable Tip:** Always flatten boxes before recycling to save space and improve efficiency."
        ),
        "plastic": (
            "🧴 **Plastic**\n"
            "\nPlastic manufacturing emits roughly **6 kg of CO₂ per kilogram**, making it one of the highest emitters. "
            "What makes plastic worse is its persistence—it doesn’t decompose for hundreds of years. "
            "Recycling helps, but only about **9%** of plastic ever gets recycled globally. "
            "Reducing single-use plastic is the best step you can take!\n\n"
            "🌍 **Sustainable Tip:** Ditch single-use plastics. Switch to cloth bags and steel bottles."
        ),
        "glass": (
            "🍶 **Glass**\n"
            "\nGlass production emits about **0.85 kg of CO₂ per kilogram**. It’s heavy, which increases transport emissions. "
            "But the good news? Glass can be recycled **endlessly** without losing quality. "
            "Just one recycled glass bottle saves enough energy to power a light bulb for four hours!\n\n"
            "🌍 **Sustainable Tip:** Reuse jars and bottles at home."
        ),
        "metal": (
            "🥫 **Metal (e.g., aluminum)**\n"
            "\nProducing aluminum from raw ore emits **11–17 kg of CO₂ per kilogram** — that's extremely high. "
            "However, **recycled metal** reduces energy use and emissions by up to **95%**! "
            "So don't throw it in the trash—metal is worth recycling every time.\n\n"
            "🌍 **Sustainable Tip:** Clean your cans before recycling for better processing."
        ),
        "paper": (
            "📄 **Paper**\n"
            "\nPaper emits about **1 kg of CO₂ per kilogram** during production, mostly due to the pulping and bleaching processes. "
            "It’s biodegradable, but paper waste still contributes to deforestation. "
            "Recycling paper reduces emissions, saves water, and helps preserve forests.\n\n"
            "🌍 **Sustainable Tip:** Reuse and recycle. Prefer digital when possible."
        ),
        "trash": (
            "🗑️ **Trash (Mixed Waste)**\n"
            "\nUnsorted trash typically ends up in **landfills** where it decomposes anaerobically and releases **methane**, a greenhouse gas **25x more potent than CO₂**. "
            "The carbon footprint depends on the material mix, but the environmental cost is always high. "
            "Reducing, sorting, and composting can make a big difference.\n\n"
            "🌍 **Sustainable Tip:** Segregate waste to improve recycling and composting."
        )
    }
    cleaned = label.split(" ")[1].strip().lower()
    return info.get(cleaned, "No carbon emission data available for this item.")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #f1f8e9);
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .app-title {
        text-align: center;
        color: #2E7D32;
        font-size: 60px;
        font-weight: 800;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #388E3C;
        font-size: 26px;
        margin-top: 0;
    }
    </style>

    <h1 class="app-title">EcoSort</h1>
    <p class="subtitle">Classify Waste. Learn Impact. Act Sustainably.</p>
""", unsafe_allow_html=True)

input_img = st.file_uploader("***Enter your image***", type=['jpg', 'png', 'jpeg'])

if input_img is not None:
    if st.button("Classify"):
        
        col1, col2, col3 = st.columns([1,1,1])

        with col1:
            st.info("📸 **Here's what you uploaded**")
            st.image(input_img, use_column_width=True)

        with col2:
            st.info("🧪 **Classification Result**")
            image_file = Image.open(input_img)
            label, confidence_score = classify_waste(image_file)
            col4, col5 = st.columns([1,1])
            if label == "0 cardboard\n":
                st.success("The image is classified as **CARDBOARD**.")                
                with col4:
                    st.image("sdg goals/12.png", use_column_width=True)
                    st.image("sdg goals/13.png", use_column_width=True)
                with col5:
                    st.image("sdg goals/14.png", use_column_width=True)
                    st.image("sdg goals/15.png", use_column_width=True) 
            elif label == "1 plastic\n":
                st.success("The image is classified as **PLASTIC**.")
                with col4:
                    st.image("sdg goals/6.jpg", use_column_width=True)
                    st.image("sdg goals/12.png", use_column_width=True)
                with col5:
                    st.image("sdg goals/14.png", use_column_width=True)
                    st.image("sdg goals/15.png", use_column_width=True) 
            elif label == "2 glass\n":
                st.success("The image is classified as **GLASS**.")
                with col4:
                    st.image("sdg goals/12.png", use_column_width=True)
                with col5:
                    st.image("sdg goals/14.png", use_column_width=True)
            elif label == "3 metal\n":
                st.success("The image is classified as **METAL**.")
                with col4:
                    st.image("sdg goals/3.png", use_column_width=True)
                    st.image("sdg goals/6.jpg", use_column_width=True)
                with col5:
                    st.image("sdg goals/12.png", use_column_width=True)
                    st.image("sdg goals/14.png", use_column_width=True) 
            elif label == "4 paper\n":
                st.success("The image is classified as **PAPER**.")
                with col4:
                    st.image("sdg goals/6.jpg", use_column_width=True)
                    st.image("sdg goals/12.png", use_column_width=True)
                with col5:
                    st.image("sdg goals/14.png", use_column_width=True)
                    st.image("sdg goals/15.png", use_column_width=True)
            elif label == "5 trash\n":
                st.success("The image is classified as **TRASH**")
                with col4:
                    st.image("sdg goals/6.jpg", use_column_width=True)
                    st.image("sdg goals/12.png", use_column_width=True)
                with col5:
                    st.image("sdg goals/14.png", use_column_width=True)
                    st.image("sdg goals/15.png", use_column_width=True) 
            else:
                st.error("The image is not classified as any relevant class.")

        with col3:
            st.info("📊 **Carbon Emission Info**")
            result = carbon_info(label)
            st.success(result)
            
st.markdown("""
<style>
@keyframes wiggle {
  0% { transform: rotate(0deg); }
  25% { transform: rotate(-10deg); }
  50% { transform: rotate(10deg); }
  75% { transform: rotate(-10deg); }
  100% { transform: rotate(0deg); }
}

.leaf {
  display: inline-block;
  animation: wiggle 3s infinite ease-in-out;
  font-size: 24px;
  margin-right: 5px;
}
.footer-quote {
  text-align: center;
  color: #444;
  font-style: italic;
  font-size: 16px;
  margin-top: 40px;
}
</style>

<div class='footer-quote'>
  <span class='leaf'>🍃</span>
  “The greatest threat to our planet is the belief that someone else will save it.”<br>
  <span style='font-size:14px;'>– Robert Swan</span>
</div>
""", unsafe_allow_html=True)
