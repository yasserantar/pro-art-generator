import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Setup API
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Page config
st.set_page_config(
    page_title="Pro AI Art Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);}
    .stButton>button {
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
        color: white !important;
        border-radius: 10px;
        padding: 15px 30px;
        font-size: 18px;
        border: none;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'generated_images' not in st.session_state:
    st.session_state['generated_images'] = []

# Sidebar
st.sidebar.title("🎨 AI Studio Tools")
st.sidebar.markdown("---")

tool = st.sidebar.radio(
    "اختر الأداة:",
    ["🖌️ Image Generator", "🎭 Style Transfer", "📸 Product Studio",
     "🔄 Image Blender", "⬆️ Upscaler", "🎨 Background Remover"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 كل الصور بتتحفظ في Gallery!")

# IMAGE GENERATOR
if tool == "🖌️ Image Generator":
    st.title("✨ Pro AI Art Generator")
    st.markdown("### Generate High-Quality Images using Google Imagen 3")
    
    tab1, tab2, tab3 = st.tabs(["🎨 Basic", "⚙️ Advanced", "🖼️ Gallery"])
    
    with tab1:
        prompt = st.text_area(
            "وصف الصورة (English or Arabic):",
            placeholder="e.g., A futuristic city in neon lights...",
            height=120
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            aspect_ratio = st.selectbox("📐 Aspect Ratio", ["1:1", "16:9", "9:16", "4:3"])
        with col2:
            num_images = st.slider("🖼️ Images", 1, 4, 1)
        with col3:
            language = st.selectbox("🌐 Language", ["English", "العربية"])
    
    with tab2:
        negative_prompt = st.text_area(
            "❌ Negative Prompt:",
            placeholder="blurry, low quality, distorted...",
            height=80
        )
        
        col1, col2 = st.columns(2)
        with col1:
            quality = st.select_slider("💎 Quality", ["Standard", "High", "Ultra"], value="High")
            art_style = st.selectbox(
                "🎨 Art Style",
                ["Photorealistic", "Cinematic", "3D Render", "Oil Painting", 
                 "Watercolor", "Digital Art", "Anime", "Minimalist"]
            )
        with col2:
            safety = st.selectbox("🛡️ Safety", ["Strict", "Moderate", "Off"], index=1)
            mood = st.selectbox(
                "🌈 Mood",
                ["Neutral", "Dramatic", "Bright", "Dark", "Warm", "Cold", "Dreamy"]
            )
    
    with tab3:
        st.markdown("#### 🖼️ Your Gallery")
        if st.session_state['generated_images']:
            cols = st.columns(2)
            for idx, img in enumerate(st.session_state['generated_images']):
                with cols[idx % 2]:
                    st.image(img, use_column_width=True)
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button(
                        f"⬇️ Download #{idx+1}",
                        buf.getvalue(),
                        f"ai_art_{idx+1}.png",
                        "image/png",
                        key=f"dl_{idx}"
                    )
        else:
            st.info("لا توجد صور. قم بإنشاء صورة جديدة!")
    
    st.markdown("---")
    if st.button("🎨 Generate Image", use_container_width=True):
        if prompt:
            enhanced_prompt = prompt
            if art_style != "Photorealistic":
                enhanced_prompt += f", {art_style} style"
            if mood != "Neutral":
                enhanced_prompt += f", {mood} mood"
            
            with st.spinner("🎨 Creating masterpiece..."):
                try:
                    model = genai.ImageGenerationModel("imagen-3.0-generate-001")
                    result = model.generate_images(
                        prompt=enhanced_prompt,
                        number_of_images=num_images,
                        safety_filter_level=safety.lower(),
                        aspect_ratio=aspect_ratio,
                        negative_prompt=negative_prompt if negative_prompt else None
                    )
                    
                    st.success("✅ تم بنجاح!")
                    cols = st.columns(num_images)
                    
                    for idx, image in enumerate(result.images):
                        with cols[idx]:
                            st.image(image._pil_image, use_column_width=True)
                            buf = io.BytesIO()
                            image._pil_image.save(buf, format="PNG")
                            st.download_button(
                                f"⬇️ Download",
                                buf.getvalue(),
                                f"generated_{idx+1}.png",
                                "image/png",
                                key=f"gen_{idx}"
                            )
                        st.session_state['generated_images'].append(image._pil_image)
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter description!")

# STYLE TRANSFER
elif tool == "🎭 Style Transfer":
    st.title("🎭 AI Style Transfer")
    st.info("🚧 Coming Soon! Transform images with artistic styles")
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
        if uploaded:
            st.image(uploaded, use_column_width=True)
    with col2:
        style = st.selectbox(
            "Style:",
            ["Van Gogh", "Picasso", "Monet", "Pop Art", "Anime"]
        )

# PRODUCT STUDIO
elif tool == "📸 Product Studio":
    st.title("📸 Product Photography Studio")
    st.info("🚧 Coming Soon! Professional product shots with AI")
    
    col1, col2 = st.columns(2)
    with col1:
        product = st.file_uploader("Upload Product", type=['png', 'jpg'])
        if product:
            st.image(product, use_column_width=True)
    with col2:
        background = st.selectbox(
            "Background:",
            ["White Studio", "Dark Luxury", "Natural Light", "Outdoor"]
        )
        lighting = st.select_slider(
            "Lighting:",
            ["Soft", "Natural", "Studio", "Dramatic"]
        )

# IMAGE BLENDER
elif tool == "🔄 Image Blender":
    st.title("🔄 AI Image Blender")
    st.info("🚧 Coming Soon! Blend multiple images seamlessly")
    
    col1, col2 = st.columns(2)
    with col1:
        img1 = st.file_uploader("Image 1", type=['png', 'jpg'], key="b1")
        if img1:
            st.image(img1, use_column_width=True)
    with col2:
        img2 = st.file_uploader("Image 2", type=['png', 'jpg'], key="b2")
        if img2:
            st.image(img2, use_column_width=True)

# UPSCALER
elif tool == "⬆️ Upscaler":
    st.title("⬆️ AI Image Upscaler")
    st.info("🚧 Coming Soon! Enhance & upscale images")
    
    uploaded = st.file_uploader("Upload Image", type=['png', 'jpg'])
    if uploaded:
        st.image(uploaded, use_column_width=True)
        scale = st.slider("Upscale Factor", 2, 8, 4)

# BACKGROUND REMOVER
else:
    st.title("🎨 Background Remover")
    st.info("🚧 Coming Soon! Remove backgrounds instantly")
    
    uploaded = st.file_uploader("Upload Image", type=['png', 'jpg'])
    if uploaded:
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded, caption="Original", use_column_width=True)
        with col2:
            st.info("Processed image will appear here")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("✨ Developed by Yasser Antar")
st.sidebar.caption("⚡ Powered by Google Imagen 3")
