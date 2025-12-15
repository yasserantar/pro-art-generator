import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# 1. Page Configuration
st.set_page_config(
    page_title="Pro Art Generator",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Main Title & Description
st.title("✨ Pro AI Art Generator")
st.markdown("### Generate High Quality Images using Google Imagen 3")

# 3. API Key Management
# Securely gets the key from Streamlit Secrets or User Input
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    api_key = st.text_input("Enter your Google API Key:", type="password")
    
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        # 4. User Inputs
        prompt_text = st.text_area("Describe your image (English or Arabic):", height=100, placeholder="e.g., A futuristic city in neon lights...")
        
        # Advanced Settings Expander
        with st.expander("⚙️ Advanced Settings"):
            col1, col2 = st.columns(2)
            
            with col1:
                aspect_ratio = st.selectbox(
                    "Aspect Ratio",
                    ["1:1", "16:9", "9:16", "4:3"]
                )
            
            with col2:
                num_images = st.slider("Number of Images", 1, 4, 1)
        
        # 5. Generate Button
        if st.button("🖌️ Generate Image", use_container_width=True):
            if not prompt_text:
                st.warning("Please enter a description first!")
            else:
                with st.spinner("Generating your masterpiece... 🎨"):
                    try:
                        # Call Google Imagen 3 Model
                        response = client.models.generate_images(
                            model='imagen-3.0-generate-001',
                            prompt=prompt_text,
                            config=types.GenerateImagesConfig(
                                number_of_images=num_images,
                                aspect_ratio=aspect_ratio.replace(":", "_"),
                            )
                        )
                        
                        # Display Result
                        st.success("Generation Complete! 🎉")
                        
                        for idx, generated_image in enumerate(response.generated_images):
                            st.image(generated_image.image, caption=f"Generated Image {idx+1}", use_container_width=True)
                        
                        # Tip for saving
                        st.info("💡 Tip: Right-click the image and select 'Save Image As' to download.")
                        
                    except Exception as e:
                        st.error(f"Error generating image: {str(e)}")
                        st.error("Make sure your API Key supports Imagen 3 and you have access.")
    
    except Exception as e:
        st.error(f"Configuration Error: {e}")
else:
    st.info("Please enter your Google API Key to start.")

# Footer
st.markdown("---")
st.caption("Developed by Yasser Antar | Powered by Google Imagen 3")
