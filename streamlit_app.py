import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Page Configuration
st.set_page_config(
    page_title="Pro AI Art Generator",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Main title
st.title("🎨 Pro AI Art Generator")
st.markdown("### Generate Images using AI (via external API)")

# User Input
prompt_text = st.text_area(
    "وصف الصورة (English or Arabic):",
    height=100,
    placeholder="e.g., A futuristic city in neon lights..."
)

# Advanced Settings
with st.expander("🎨 Advanced Settings"):
    col1, col2 = st.columns(2)
    
    with col1:
        style_mode = st.selectbox(
            "Art Style",
            ["Photorealistic", "Cinematic", "3D Render", "Anime/Manga", "Oil Painting", "Digital Art"]
        )
    
    with col2:
        num_images = st.slider("Number of Images", 1, 4, 1)

# Generate button
if st.button("🖌️ Generate Image", use_container_width=True):
    if not prompt_text:
        st.warning("Please enter a description first!")
    else:
        with st.spinner("Generating your masterpiece... 🎨"):
            try:
                # Use Pollinations.ai API (Free text-to-image)
                style_modifiers = {
                    "Photorealistic": "photorealistic, 4k, highly detailed, sharp focus, realistic textures",
                    "Cinematic": "cinematic lighting, dramatic atmosphere, movie scene, 4k",
                    "3D Render": "3d render, unreal engine 5, octane render, isometric",
                    "Anime/Manga": "anime style, studio ghibli, vibrant colors",
                    "Oil Painting": "oil painting, artistic, impressionist style",
                    "Digital Art": "digital art, concept art, trending on artstation"
                }
                
                full_prompt = f"{prompt_text}, {style_modifiers[style_mode]}"
                
                # Generate images
                st.success("Generation Complete! 🎉")
                
                for idx in range(num_images):
                    # Using Pollinations.ai free API
                    image_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(full_prompt)}?width=1024&height=1024&seed={idx}"
                    
                    try:
                        response = requests.get(image_url, timeout=30)
                        if response.status_code == 200:
                            img = Image.open(BytesIO(response.content))
                            st.image(img, caption=f"Generated Image {idx+1}", use_container_width=True)
                        else:
                            st.error(f"Failed to generate image {idx+1}")
                    except Exception as e:
                        st.error(f"Error loading image {idx+1}: {str(e)}")
                
                # Tip for saving
                st.info("💡 Tip: Right-click the image and select 'Save Image As' to download.")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
else:
    st.info("Please enter your API key to start.")

# Footer
st.markdown("---")
st.caption("Developed by Yasser Antar | Powered by AI")
