import streamlit as st
from PIL import Image
import numpy as np
import base64

# UI
st.set_page_config(page_title="Smart Farmer AI", layout="wide")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    
#Heading
st.markdown("""
<div style='text-align: center; margin-top: 20px; margin-bottom: 30px;'>
    <h1 style='color: black; font-size: 48px; margin-bottom: 5px;'>🌿 FarmGuard</h1>
    <p style='color: black; font-size: 30px; font-weight: 500;'>
        Detect. Protect. Grow Smarter.
    </p>
</div>
""", unsafe_allow_html=True)

#  Crop selection
crop = st.selectbox("Select Crop 🌾", ["Tomato  ಟೊಮೇಟೊ", "Potato  ಆಲೂಗಡ್ಡೆ", "Brinjal  ಬದನೆಕಾಯಿ", "Rice  ಅಕ್ಕಿ", "Wheat  ಗೋಧಿ"])

#  Upload
uploaded_file = st.file_uploader("Upload Leaf Image 📸", type=["jpg","png","jpeg","webp"])

#  Analysis
def analyze(image):
    img = image.resize((224, 224))
    arr = np.array(img)

    # Normalize
    arr = arr / 255.0

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    # 🌿 HEALTHY GREEN DETECTION
    green_mask = (g > r) & (g > b)

    green_pixels = np.sum(green_mask)
    total_pixels = arr.shape[0] * arr.shape[1]

    green_ratio = green_pixels / total_pixels

    # 🌱 Health is based on real green dominance
    health = int(green_ratio * 100)

    # clamp safely
    health = max(0, min(health, 100))


    if health >= 90:
        disease = "🌿 Healthy Crop"
    elif health >= 75:
        disease = "🌱 Good (Minor Stress)"
    elif health >= 60:
        disease = "🌿 Moderate Damage"
    elif health >= 40:
        disease = "🌾 High Disease Risk"
    elif health >= 20:
        disease = "🚨 Severe Infection"
    else:
        disease = "❌ Critical Crop Failure"

    return disease, health

# 💊 Remedies
def get_remedies(health):
    if health >= 90:
        return [
            "🌿 Neem oil (preventive bio-spray) / ಬೇವಿನ ಎಣ್ಣೆ ಸಿಂಪಡಣೆ",
            "🌰 Neem Seed Kernel Extract (NSKE) / ಬೇವಿನ ಬೀಜ ಕರ್ಣಲ್ ಸಾರ"
            
        ]
    elif health >= 75:
        return [
            "🌿 Neem Oil Spray / ಬೇವಿನ ಎಣ್ಣೆ ಸಿಂಪಡಣೆ",
            "🧫 Bacillus thuringiensis (Bt) / ಬ್ಯಸಿಲ್ಲಸ್ ಥುರಿಂಜಿಯೆನ್ಸಿಸ್ (ಬಿಟಿ ಜೈವ ಕೀಟನಾಶಕ)",
            "🦋 Pheromone Traps / ಫೆರೋಮೋನ್ ಬಲೆಯುಗಳು"
        ]
    elif health >= 60:
        return [
            "🦠 Bt Spray / ಬ್ಯಾಸಿಲ್ಲಸ್ ಥುರಿಂಜಿಯೆನ್ಸಿಸ್ ಸಿಂಪಡಣೆ (ಬ್ಯಾಕ್ಟೀರಿಯಾದ ಮೂಲಕ ಕೀಟ ಲಾರ್ವಾ ನಾಶ)",
            "🐞 Chlorantraniliprole / ಕ್ಲೋರಾಂಟ್ರಾನಿಲಿಪ್ರೋಲ್ (ಕಡ್ಡಿ ಮತ್ತು ಎಲೆ ಬೋರರ್ ಕೀಟ ನಿಯಂತ್ರಣ)",
            "✂️ Remove infected leaves / ರೋಗ ಹರಡುವುದನ್ನು ತಡೆಯಲು ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆಯಿರಿ"
        ]
    elif health >= 50:
        return [
            "🧪 Mancozeb / ಮ್ಯಾಂಕೋಜೆಬ್ (ಎಲೆ ಮಚ್ಚೆ ಫಂಗಸ್ ರೋಗಗಳನ್ನು ತಡೆಯುತ್ತದೆ)",
            "🧪 Copper Fungicide / ಕಾಪರ್ ಫಂಗಿಸೈಡ್ (ಬ್ಯಾಕ್ಟೀರಿಯಾ ಮತ್ತು ಫಂಗಸ್ ಸೋಂಕುಗಳನ್ನು ನಿಯಂತ್ರಿಸುತ್ತದೆ)",
            "✂️ Remove infected leaves / ರೋಗ ಹರಡುವುದನ್ನು ತಡೆಯಲು ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆಯಿರಿ"
        ]
    elif health >= 20:
        return [
            "⚡ Strong insecticide spray (Carbendazim--Reduces Fungal Infection) / ಬಲವಾದ ಕೀಟನಾಶಕ ಸಿಂಪಡಣೆ(ಕಾರ್ಬೆಂಡಾಜಿಮ್--ಶಿಲೀಂಧ್ರ (ಫಂಗಸ್) ನಿಯಂತ್ರಣ) ",
            "🧪 Copper Oxychloride / ಕಾಪರ್ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ (ಫಂಗಸ್ ಮತ್ತು ಬ್ಯಾಕ್ಟೀರಿಯಾ ಸೋಂಕು ತಡೆಯುತ್ತದೆ)",
            "🧫 Bio-fungicide / ಜೈವಿಕ ಫಂಗಿಸೈಡ್ (ಮಣ್ಣು ಮತ್ತು ಸಸ್ಯ ಫಂಗಸ್ ರೋಗ ನಿಯಂತ್ರಣ)",
            "🚜 Field sanitation / ಹೊಲದ ಸ್ವಚ್ಛತೆ (ಸೋಂಕಿತ ಎಲೆ ಮತ್ತು ಗಿಡಗಳನ್ನು ತೆಗೆದುಹಾಕುವುದು)"
        ]
    else:
        return [
            "🚜 Remove infected crop / ರೋಗಗ್ರಸ್ತ ಬೆಳೆಗಳನ್ನು ತೆಗೆಯುವುದು (ರೋಗ ಹರಡುವುದನ್ನು ತಡೆಯುತ್ತದೆ)",
            "🧪 Soil sterilization / ಮಣ್ಣು ಶುದ್ಧೀಕರಣ (ಹಾನಿಕಾರಕ ರೋಗಾಣುಗಳನ್ನು ನಾಶ ಮಾಡುತ್ತದೆ)",
            "🧫 Bio-fungicide recovery / ಜೈವಿಕ ಫಂಗಿಸೈಡ್ ಪುನಶ್ಚೇತನ (ಉಪಯುಕ್ತ ಸೂಕ್ಷ್ಮಜೀವಿಗಳನ್ನು ಪುನಃ ಸ್ಥಾಪಿಸುತ್ತದೆ)",
            "⚡ Emergency pesticide / ತುರ್ತು ಕೀಟನಾಶಕ (ತೀವ್ರ ಕೀಟ ದಾಳಿಯನ್ನು ತಕ್ಷಣ ನಿಯಂತ್ರಿಸುತ್ತದೆ)",
            "🌾 Stop irrigation / ನೀರಾವರಿ ನಿಲ್ಲಿಸುವುದು (ರೋಗ ಹರಡುವುದನ್ನು ಕಡಿಮೆ ಮಾಡುತ್ತದೆ)",
            "🌱 Crop rotation / ಬೆಳೆ ಪರಿವರ್ತನೆ (ಮಣ್ಣಿನ ಪೋಷಕಾಂಶ ಸಮತೋಲನ ಕಾಯುತ್ತದೆ)",
        ]

# 🚀 MAIN
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Leaf", width='stretch')

    if st.button("🔍 Detect Disease"):
        disease, health = analyze(image)

        st.success(f"🌾 Crop: {crop}")
        st.success(f"🦠 Condition: {disease}")

        disease = 100 - health

        st.info(f"💚 Health: {health}%")
        st.info(f"❤️ Disease: {disease}%")
        st.progress(health)

        st.subheader("💊 Recommended Remedies")

        for r in get_remedies(health):
            st.info(r)

            #------------Organic and inorganic fertilizers based on specific crop type-----------

def get_crop_specific_remedies(crop):

    if crop == "Tomato  ಟೊಮೇಟೊ":
        return {
            "organic": [
                "🌿 Neem oil spray (natural pest control) / ಬೇವಿನ ಎಣ್ಣೆ (ಪ್ರಾಕೃತಿಕವಾಗಿ ಕೀಟಗಳನ್ನು ನಿಯಂತ್ರಿಸುತ್ತದೆ) ",
                "🌱 Vermicompost (improves soil fertility) / ಎರೆಹುಳು ಗೊಬ್ಬರ (ಮಣ್ಣಿನ ಫಲವತ್ತತೆ ಹೆಚ್ಚಿಸುತ್ತದೆ) ",
                "🐄 Farmyard Manure (Improves soil fertility naturally) / ಹಸು ಗೊಬ್ಬರ (ಸ್ವಾಭಾವಿಕ ಪೋಷಕಾಂಶ ಒದಗಿಸುತ್ತದೆ)",
                "🧫 Trichoderma (Controls soil fungal diseases) / ಟ್ರೈಕೋಡರ್ಮಾ (ಶಿಲೀಂಧ್ರ (ಫಂಗಸ್) ನಿಯಂತ್ರಣ)",
                "♻️ Compost (Improves soil structure and nutrients) / ಸಾವಯವ ಗೊಬ್ಬರ (ಮಣ್ಣಿನ ರಚನೆ ಮತ್ತು ಪೋಷಕಾಂಶಗಳನ್ನು ಸುಧಾರಿಸುತ್ತದೆ)",
                "🌱 Jeevamrutha (Boost Plant Immunity) / (ಸಸ್ಯದ ರೋಗ ನಿರೋಧಕ ಶಕ್ತಿಯನ್ನು ಹೆಚ್ಚಿಸುತ್ತದೆ)"
            ],
            "chemical": [
                "🧪 NPK (19:19:19 ratio, balanced plant growth support) / ಎನ್‌ಪಿಕೆ (19:19:19) (1–2 ಗ್ರಾಂ / ಲೀಟರ್) (40–50 ಕೆಜಿ / ಏಕರೆ)",
                "🧪 Urea (46% Nitrogen, promotes leafy growth fast) / ಯೂರಿಯಾ (46%) (5 ಗ್ರಾಂ / ಲೀಟರ್) (70-80 ಕೆಜಿ / ಏಕರೆ)",
                "🧪 DAP (18:46:0 ratio, supports root and flowering) / ಡಿಎಪಿ (18:46:0) (2 ಗ್ರಾಂ / ಲೀಟರ್) (25–35 ಕೆಜಿ / ಏಕರೆ)",
                "🧪 MOP (0:0:60 ratio, improves fruit size quality) / ಎಂಒಪಿ (0:0:60) (1–2 ಗ್ರಾಂ / ಲೀಟರ್) (75–100 ಕೆಜಿ / ಏಕರೆ)",
                "🦠 Imidacloprid (Controls sucking insect pests) / ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ (0.3–0.5 ಮಿ.ಲಿ / ಲೀಟರ್)",
                "🦠 Mancozeb (Prevents fungal leaf diseases) / ಮ್ಯಾಂಕೋಜೆಬ್ (2–2.5 ಗ್ರಾಂ / ಲೀಟರ್)",
                "🦠 Carbendazim (Controls root fungal infections) / ಕಾರ್ಬೆಂಡಜಿಂ (1 ಗ್ರಾಂ / ಲೀಟರ್)",
                "🦠 Chlorpyrifos (Controls soil insect larvae) / ಕ್ಲೋರ್ಪೈರಿಫಾಸ್ (2 ಮಿ.ಲಿ / ಲೀಟರ್)"
            ]
        }
    

    elif crop == "Potato  ಆಲೂಗಡ್ಡೆ":
        return {
            "organic": [
                "🌿 Neem oil spray (natural pest control) / ಬೇವಿನ ಎಣ್ಣೆ (ಪ್ರಾಕೃತಿಕವಾಗಿ ಕೀಟಗಳನ್ನು ನಿಯಂತ್ರಿಸುತ್ತದೆ) ",
                "🌱 Vermicompost (improves soil fertility) / ಎರೆಹುಳು ಗೊಬ್ಬರ (ಮಣ್ಣಿನ ಫಲವತ್ತತೆ ಹೆಚ್ಚಿಸುತ್ತದೆ) ",
                "🐄 Farmyard Manure (Improves soil fertility naturally) / ಹಸು ಗೊಬ್ಬರ (ಸ್ವಾಭಾವಿಕ ಪೋಷಕಾಂಶ ಒದಗಿಸುತ್ತದೆ)",
                "🧫 Trichoderma (Controls soil fungal diseases) / ಟ್ರೈಕೋಡರ್ಮಾ (ಶಿಲೀಂಧ್ರ (ಫಂಗಸ್) ನಿಯಂತ್ರಣ)",
                "♻️ Compost (Improves soil structure and nutrients) / ಸಾವಯವ ಗೊಬ್ಬರ (ಮಣ್ಣಿನ ರಚನೆ ಮತ್ತು ಪೋಷಕಾಂಶಗಳನ್ನು ಸುಧಾರಿಸುತ್ತದೆ)",
                "🌱 Jeevamrutha (Boost Plant Immunity) / (ಸಸ್ಯದ ರೋಗ ನಿರೋಧಕ ಶಕ್ತಿಯನ್ನು ಹೆಚ್ಚಿಸುತ್ತದೆ)"
                
                
            ],
            "chemical": [
                "🧪 NPK (12:32:16 ratio, tuber development focused) / ಎನ್‌ಪಿಕೆ (12:32:16) (1–2 ಗ್ರಾಂ / ಲೀಟರ್)(40–50 ಕೆಜಿ / ಏಕರೆ)",
                "🧪 Urea (46% Nitrogen, controlled vegetative growth) / ಯೂರಿಯಾ (5 ಗ್ರಾಂ / ಲೀಟರ್) (70-80 ಕೆಜಿ / ಏಕರೆ)",
                "🧪 DAP (18:46:0 ratio, supports early tuber formation) / ಡಿಎಪಿ (2 ಗ್ರಾಂ / ಲೀಟರ್) 20–30 ಕೆಜಿ / ಏಕರೆ)",
                "🧪 MOP (0:0:60 ratio, improves tuber size and quality) / ಎಂಒಪಿ (1–2 ಗ್ರಾಂ / ಲೀಟರ್)",
                "🦠 Imidacloprid (Controls sucking insect pests) / ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ (0.3–0.5 ಮಿ.ಲಿ / ಲೀಟರ್)",
                "🦠 Mancozeb (Prevents fungal leaf diseases) / ಮ್ಯಾಂಕೋಜೆಬ್ (2–2.5 ಗ್ರಾಂ / ಲೀಟರ್)",
                "🦠 Carbendazim (Controls root fungal infections) / ಕಾರ್ಬೆಂಡಜಿಂ (1 ಗ್ರಾಂ / ಲೀಟರ್)",
                            
                        ]
        }


    elif crop == "Brinjal  ಬದನೆಕಾಯಿ":
        return {
            "organic": [
                "🌿 Neem oil spray (natural pest control) / ಬೇವಿನ ಎಣ್ಣೆ (ಪ್ರಾಕೃತಿಕವಾಗಿ ಕೀಟಗಳನ್ನು ನಿಯಂತ್ರಿಸುತ್ತದೆ) ",
                "🌱 Vermicompost (improves soil fertility) / ಎರೆಹುಳು ಗೊಬ್ಬರ (ಮಣ್ಣಿನ ಫಲವತ್ತತೆ ಹೆಚ್ಚಿಸುತ್ತದೆ) ",
                "🐄 Farmyard Manure (Improves soil fertility naturally) / ಹಸು ಗೊಬ್ಬರ (ಸ್ವಾಭಾವಿಕ ಪೋಷಕಾಂಶ ಒದಗಿಸುತ್ತದೆ)",
                "🧫 Trichoderma (Controls soil fungal diseases) / ಟ್ರೈಕೋಡರ್ಮಾ (ಶಿಲೀಂಧ್ರ (ಫಂಗಸ್) ನಿಯಂತ್ರಣ)",
                "♻️ Compost (Improves soil structure and nutrients) / ಸಾವಯವ ಗೊಬ್ಬರ (ಮಣ್ಣಿನ ರಚನೆ ಮತ್ತು ಪೋಷಕಾಂಶಗಳನ್ನು ಸುಧಾರಿಸುತ್ತದೆ)",
                "🌱 Jeevamrutha (Boost Plant Immunity) / (ಸಸ್ಯದ ರೋಗ ನಿರೋಧಕ ಶಕ್ತಿಯನ್ನು ಹೆಚ್ಚಿಸುತ್ತದೆ)"
                
            ],
            "chemical": [
               "🧪 Urea (46% Nitrogen, promotes leafy growth) / ಯೂರಿಯಾ (5 ಗ್ರಾಂ / ಲೀಟರ್) (70-80 ಕೆಜಿ / ಏಕರೆ)",
                "🧪 DAP (18:46:0 ratio, supports root and flowering) / ಡಿಎಪಿ (2 ಗ್ರಾಂ / ಲೀಟರ್) 25–35 ಕೆಜಿ / ಏಕರೆ)",
                "🧪 NPK (15:15:15 ratio, balanced crop growth) / ಎನ್‌ಪಿಕೆ (1–2 ಗ್ರಾಂ / ಲೀಟರ್) (40–50 ಕೆಜಿ / ಏಕರೆ)",
                "🧪 MOP (0:0:60 ratio, improves fruit quality) / ಎಂಒಪಿ (1–2 ಗ್ರಾಂ / ಲೀಟರ್)",
                "🦠 Imidacloprid (Controls sucking insect pests) / ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ (0.3–0.5 ಮಿ.ಲಿ / ಲೀಟರ್)",
                "🦠 Mancozeb (Prevents fungal leaf diseases) / ಮ್ಯಾಂಕೋಜೆಬ್ (2–2.5 ಗ್ರಾಂ / ಲೀಟರ್)",
                "🦠 Carbendazim (Controls root fungal infections) / ಕಾರ್ಬೆಂಡಜಿಂ (1 ಗ್ರಾಂ / ಲೀಟರ್)",
               
            ]
        }
    

    elif crop == "Rice  ಅಕ್ಕಿ":
        return {
            "organic": [
                "🌿 Neem oil spray (natural pest control) / ಬೇವಿನ ಎಣ್ಣೆ (ಪ್ರಾಕೃತಿಕವಾಗಿ ಕೀಟಗಳನ್ನು ನಿಯಂತ್ರಿಸುತ್ತದೆ) ",
                "🌱 Vermicompost (improves soil fertility) / ಎರೆಹುಳು ಗೊಬ್ಬರ (ಮಣ್ಣಿನ ಫಲವತ್ತತೆ ಹೆಚ್ಚಿಸುತ್ತದೆ) ",
                "🐄 Farmyard Manure (Improves soil fertility naturally) / ಹಸು ಗೊಬ್ಬರ (ಸ್ವಾಭಾವಿಕ ಪೋಷಕಾಂಶ ಒದಗಿಸುತ್ತದೆ)",
                "🧫 Trichoderma (Controls soil fungal diseases) / ಟ್ರೈಕೋಡರ್ಮಾ (ಶಿಲೀಂಧ್ರ (ಫಂಗಸ್) ನಿಯಂತ್ರಣ)",
                "♻️ Compost (Improves soil structure and nutrients) / ಸಾವಯವ ಗೊಬ್ಬರ (ಮಣ್ಣಿನ ರಚನೆ ಮತ್ತು ಪೋಷಕಾಂಶಗಳನ್ನು ಸುಧಾರಿಸುತ್ತದೆ)",
                "🌱 Jeevamrutha (Boost Plant Immunity) / (ಸಸ್ಯದ ರೋಗ ನಿರೋಧಕ ಶಕ್ತಿಯನ್ನು ಹೆಚ್ಚಿಸುತ್ತದೆ)"
                
            ],
            "chemical": [
                "Require High Nitrogen Content Fertilizers",
                "🧪 NPK (16:20:0 or 10:26:26 ratio, paddy growth support) / ಎನ್‌ಪಿಕೆ (1–2 ಗ್ರಾಂ / ಲೀಟರ್) (40–50 ಕೆಜಿ / ಏಕರೆ)",
                "🧪 Urea (46% Nitrogen, boosts leafy tiller growth) / ಯೂರಿಯಾ (5 ಗ್ರಾಂ / ಲೀಟರ್) (70-80 ಕೆಜಿ / ಏಕರೆ)",
                "🧪 Magnesium Sulphate (Improves photosynthesis and leaf health) / ಮ್ಯಾಗ್ನೀಷಿಯಂ ಸಲ್ಫೇಟ್ (2–5 ಗ್ರಾಂ / ಲೀಟರ್)",
                "🧪 Zinc Sulphate (Prevents yellowing and stunted growth) / ಜಿಂಕ್ ಸಲ್ಫೇಟ್ (0.5–1 ಗ್ರಾಂ / ಲೀಟರ್)",
                "🦠 Propiconazole (Controls blast and leaf spot diseases) / ಪ್ರೊಪಿಕೊನಾಜೋಲ್ (1 ಮಿ.ಲಿ / ಲೀಟರ್)",
                "🦠 Emamectin Benzoate (Kills leaf eating insect larvae) / ಎಮಾಮೆಕ್ಟಿನ್ ಬೆಂಜೋಯೇಟ್ (0.4 ಗ್ರಾಂ / ಲೀಟರ್)",
                "🦠 Spinosad (Controls caterpillars and fruit borer insects) / ಸ್ಪಿನೋಸಾಡ್ (0.3–0.5 ಮಿ.ಲಿ / ಲೀಟರ್)"
                ]
        }


    elif crop == "Wheat  ಗೋಧಿ":
        return {
            "organic": [
                 "🌿 Neem oil spray (natural pest control) / ಬೇವಿನ ಎಣ್ಣೆ (ಪ್ರಾಕೃತಿಕವಾಗಿ ಕೀಟಗಳನ್ನು ನಿಯಂತ್ರಿಸುತ್ತದೆ) (40–50 ಕೆಜಿ / ಏಕರೆ)",
                "🌱 Vermicompost (improves soil fertility) / ಎರೆಹುಳು ಗೊಬ್ಬರ (ಮಣ್ಣಿನ ಫಲವತ್ತತೆ ಹೆಚ್ಚಿಸುತ್ತದೆ) ",
                "🐄 Farmyard Manure (Improves soil fertility naturally) / ಹಸು ಗೊಬ್ಬರ (ಸ್ವಾಭಾವಿಕ ಪೋಷಕಾಂಶ ಒದಗಿಸುತ್ತದೆ)",
                "🧫 Trichoderma (Controls soil fungal diseases) / ಟ್ರೈಕೋಡರ್ಮಾ (ಶಿಲೀಂಧ್ರ (ಫಂಗಸ್) ನಿಯಂತ್ರಣ)",
                "♻️ Compost (Improves soil structure and nutrients) / ಸಾವಯವ ಗೊಬ್ಬರ (ಮಣ್ಣಿನ ರಚನೆ ಮತ್ತು ಪೋಷಕಾಂಶಗಳನ್ನು ಸುಧಾರಿಸುತ್ತದೆ)",
                "🌱 Jeevamrutha (Boost Plant Immunity) / (ಸಸ್ಯದ ರೋಗ ನಿರೋಧಕ ಶಕ್ತಿಯನ್ನು ಹೆಚ್ಚಿಸುತ್ತದೆ)"
               
            ],
            "chemical": [
                "🧪 NPK (20:20:0 or 19:19:19 ratio, balanced crop growth) / ಎನ್‌ಪಿಕೆ (1–2 ಗ್ರಾಂ / ಲೀಟರ್) (40–50 ಕೆಜಿ / ಏಕರೆ)", 
                "🧪 Zinc Sulphate (Prevents leaf yellowing and stunted growth) / ಜಿಂಕ್ ಸಲ್ಫೇಟ್ (0.5–1 ಗ್ರಾಂ / ಲೀಟರ್)",
                "🧪 Urea (46% Nitrogen, supports strong leaf growth) / ಯೂರಿಯಾ (5 ಗ್ರಾಂ / ಲೀಟರ್) (70-80 ಕೆಜಿ / ಏಕರೆ)",
                "🧪 SSP (Single Super Phosphate, supports root and plant strength) / ಸಿಂಗಲ್ ಸೂಪರ್ ಫಾಸ್ಫೇಟ್ (ಮಣ್ಣಿಗೆ 50–100 ಕೆಜಿ / ಏಕರೆ)",
                "🧪 Magnesium Sulphate (Improves chlorophyll and leaf greening) / ಮ್ಯಾಗ್ನೀಷಿಯಂ ಸಲ್ಫೇಟ್ (2–5 ಗ್ರಾಂ / ಲೀಟರ್)",
                "🦠 Propiconazole (Controls leaf rust and fungal spots) / ಪ್ರೊಪಿಕೊನಾಜೋಲ್ (1 ಮಿ.ಲಿ / ಲೀಟರ್)",
                "🦠 Spinosad (Bio insecticide for leaf eating pests) / ಸ್ಪಿನೋಸಾಡ್ (0.3–0.5 ಮಿ.ಲಿ / ಲೀಟರ್)",
                "🦠 Copper Oxychloride (Prevents bacterial and fungal leaf diseases) / ಕಾಪರ್ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ (2.5–3 ಗ್ರಾಂ / ಲೀಟರ್)",
                "🦠 Imidacloprid (Controls aphids and leaf hoppers) / ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ (0.3–0.5 ಮಿ.ಲಿ / ಲೀಟರ್)",
                "🦠 Lambda Cyhalothrin (Controls chewing and sucking pests) / ಲ್ಯಾಂಬ್ಡಾ ಸೈಹಾಲೋಥ್ರಿನ್ (0.5 ಮಿ.ಲಿ / ಲೀಟರ್)"
            ]
        }
  
  


try:
    if uploaded_file and 'health' in locals():

        data = get_crop_specific_remedies(crop)

        st.subheader("🌾 Crop-Specific Advanced Recommendations")

        st.markdown("### 🌿 Organic Solutions / ಸಾವಯವ ಗೊಬ್ಬರಗಳು")
        for item in data["organic"]:
            st.success(item)

        st.markdown("### ⚗️ Chemical Fertilizers & Pesticides / ರಾಸಾಯನಿಕ ರಸಗೊಬ್ಬರಗಳು ಮತ್ತು ಕೀಟನಾಶಕಗಳು")
        for item in data["chemical"]:
            st.warning(item)


except:
    pass