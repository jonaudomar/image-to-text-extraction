import streamlit as st
from PIL import Image
import pytesseract
import time
import random

st.set_page_config(
    page_title="OCR ludique",
    page_icon="📸",
    layout="centered"
)

st.title("Text extraction app")
st.write("Upload an image and see the text extraction")

# Upload de l'image
uploaded_file = st.file_uploader(
    "Choose an image (png, jpg, jpeg)",
    type=["png", "jpg", "jpeg"]
)

def preprocess_image(image):
    gray = image.convert("L")
    # bw = gray.point(lambda x: 0 if x < 140 else 255, "1")
    return gray #bw

def typewriter_streamlit(text, base_delay=0.03):
    placeholder = st.empty()
    displayed_text = ""

    for char in text:
        displayed_text += char
        placeholder.markdown(
            f"<pre>{displayed_text}</pre>",
            unsafe_allow_html=True
        )

        if char in ".!?":
            time.sleep(base_delay * 6)
        elif char in ",;:":
            time.sleep(base_delay * 3)
        elif char == "\n":
            time.sleep(base_delay * 4)
        else:
            time.sleep(base_delay + random.uniform(-0.01, 0.01))

if uploaded_file:
    image = Image.open(uploaded_file)

    st.subheader("🖼️ Image source")
    st.image(image, use_column_width=True)

    if st.button("🔍 Run OCR"):
        with st.spinner("Analyse de l’image..."):
            processed = preprocess_image(image)
            text = pytesseract.image_to_string(
                processed,
                lang="fra",
                config="--psm 6"
            )

        st.subheader("📝 Texte détecté")
        typewriter_streamlit(text)
