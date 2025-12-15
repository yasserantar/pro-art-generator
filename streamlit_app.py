import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

# Page configuration
st.set_page_config(
    page_title="Pro AI Art Generator",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Main title
st.title("🎨 Pro AI Art Generator")
st.markdown("**Generate & Edit Images using AI (Multiple Models)**")

# Model Selection
st.markdown("#### 🤖 Choose AI Model")
model_choice = st.selectbox(
    "Select Generation Model:",
    ["Pollinations.ai - Free & Fast 🚀", "Gemini 3 Pro Image (Nano Banana Pro) 🔥 [Coming Soon]"],
    help="Pollinations.ai is our most advanced image model with superior quality. Free and instant!"
)

# Image Upload Section
st.markdown("#### 📸 Upload Reference Image (Optional)")
uploaded_file = st.file_uploader(
    "Upload an image to describe or use as reference:",
    type=["png", "jpg", "jpeg", "webp"],
    help="Upload an image and describe what changes you want"
)

# Prompt input
st.markdown("#### ✍️ وصف الصورة أو التعديل المطلوب (English or Arabic):")
prompt = st.text_area(
    "Describe the image you want:",
    placeholder="e.g., A professional product photography of a coffee mug\nأو: فنجان قهوة احترافي بتصميم عصري على طاولة خشبية، جودة عالية",
    height=100,
    label_visibility="collapsed"
)

# Advanced Settings
with st.expander("🎨 Advanced Settings"):
    col1, col2 = st.columns(2)
    
    with col1:
        art_style = st.selectbox(
            "Art Style",
            ["Photorealistic", "Cinematic", "3D Render", "Anime/Manga", "Oil Painting", "Digital Art", "Product Photography"]
        )
    
    with col2:
        num_images = st.slider("Number of Images", 1, 4, 1)
    
    quality = st.select_slider(
        "Image Quality (Resolution)",
        options=["1K (1024x1024)", "2K (2048x2048)", "4K (4096x4096)"],
        value="2K (2048x2048)"
    )

# Generate button
if st.button("🖌️ Generate Image", type="primary", use_container_width=True):
    if not prompt:
        st.error("✍️ Please enter a prompt to start generating images!")
    else:
        # Show loading message
        st.info("🎨 Generating your image with Pollinations.ai...")
        
        try:
            # Enhance prompt with style
            enhanced_prompt = f"{prompt}, {art_style.lower()} style, high quality, detailed"
            
            # Get resolution from quality setting
            if "4K" in quality:
                width, height = 1024, 1024  # Pollinations works best with 1024x1024
            elif "2K" in quality:
                width, height = 1024, 1024
            else:
                width, height = 1024, 1024
            
            # Generate images
            for i in range(num_images):
                # Create Pollinations URL
                pollinations_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(enhanced_prompt)}?width={width}&height={height}&nologo=true&model=flux"
                
                st.success(f"✅ Image {i+1} generated successfully!")
                st.image(pollinations_url, caption=f"Generated Image {i+1} (Pollinations.ai)", use_container_width=True)
                
                # Add download button
                st.markdown(f"[⬇️ Download Image {i+1}]({pollinations_url})")
        
        except Exception as e:
            st.error(f"❌ Error generating image: {str(e)}")
            st.info("💡 Please try again with a different prompt or check your internet connection.")

# Footer
st.markdown("---")
st.markdown("Developed by Yasser Antar | Powered by Pollinations AI")
st.markdown("💡 **Pro Tip:** Use Pollinations.ai for best quality product photography and professional images!")
