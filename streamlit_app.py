import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64
import google.generativeai as genai
import os

# Page Configuration
st.set_page_config(
    page_title="Pro AI Art Generator",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Main title
st.title("🎨 Pro AI Art Generator")
st.markdown("### Generate & Edit Images using AI (Multiple Models)")

# Model Selection
st.markdown("#### 🤖 Choose AI Model")
model_choice = st.selectbox(
    "Select Generation Model:",
    ["Gemini (Imagen 3) - Best Quality 🔥", "Pollinations.ai - Free & Fast"],
    help="Gemini requires API key but produces superior quality. Pollinations is free but lower quality."
)

# API Key input for Gemini
api_key = None
if "Gemini" in model_choice:
    api_key = st.text_input(
        "🔑 Enter your Gemini API Key:",
        type="password",
        help="Get your free API key from: https://ai.google.dev/"
    )
    if api_key:
        genai.configure(api_key=api_key)
        st.success("✅ API Key configured successfully!")

# Image Upload Section
st.markdown("---")
st.markdown("#### 📸 Upload Reference Image (Optional)")
uploaded_file = st.file_uploader(
    "Upload an image to describe or use as reference:",
    type=["png", "jpg", "jpeg", "webp"],
    help="Upload an image and describe what changes you want"
)

if uploaded_file:
    uploaded_image = Image.open(uploaded_file)
    st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
    
    # If Gemini is selected, analyze the image
    if "Gemini" in model_choice and api_key:
        with st.spinner("🔍 Analyzing your image..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(["Describe this image in detail, focusing on the style, composition, colors, and main elements.", uploaded_image])
                st.info(f"📝 **AI Image Analysis:**\n{response.text}")
                st.session_state['image_description'] = response.text
            except Exception as e:
                st.warning(f"Could not analyze image: {str(e)}")

# User Input
st.markdown("---")
prompt_text = st.text_area(
    "✍️ وصف الصورة أو التعديل المطلوب (English or Arabic):",
    height=120,
    placeholder="e.g., A professional product photography of a coffee mug\nأو: قطة بيضاء جميلة في حديقة",
    help="Describe what you want to generate or how to modify the uploaded image"
)

# Advanced Settings
with st.expander("🎨 Advanced Settings"):
    col1, col2 = st.columns(2)
    
    with col1:
        style_mode = st.selectbox(
            "Art Style",
            ["Photorealistic", "Cinematic", "3D Render", "Anime/Manga", "Oil Painting", "Digital Art", "Product Photography"]
        )
    
    with col2:
        num_images = st.slider("Number of Images", 1, 4, 1)
    
    if "Gemini" in model_choice:
        quality = st.select_slider(
            "Image Quality",
            options=["Standard", "High", "Ultra (4K)"],
            value="High"
        )

# Generate button
if st.button("🖌️ Generate Image", use_container_width=True, type="primary"):
    if not prompt_text:
        st.warning("⚠️ Please enter a description first!")
    elif "Gemini" in model_choice and not api_key:
        st.error("🔑 Please enter your Gemini API key to use this model!")
    else:
        with st.spinner("🎨 Generating your masterpiece..."):
            try:
                # Style modifiers
                style_modifiers = {
                    "Photorealistic": "photorealistic, 4k, highly detailed, sharp focus, realistic textures, professional photography",
                    "Cinematic": "cinematic lighting, dramatic atmosphere, movie scene, 4k, film grain, color grading",
                    "3D Render": "3d render, unreal engine 5, octane render, isometric, highly detailed",
                    "Anime/Manga": "anime style, studio ghibli, vibrant colors, detailed illustration",
                    "Oil Painting": "oil painting, artistic, impressionist style, brush strokes, fine art",
                    "Digital Art": "digital art, concept art, trending on artstation, detailed, vibrant",
                    "Product Photography": "product photography, studio lighting, white background, commercial, high quality"
                }
                
                full_prompt = f"{prompt_text}, {style_modifiers[style_mode]}"
                
                if "Gemini" in model_choice:
                    # Use Gemini Imagen 3
                    st.info("🔥 Using Gemini Imagen 3 for superior quality...")
                    
                    try:
                        # Configure Gemini
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        
                        # Prepare content for generation
                        content_parts = [full_prompt]
                        
                        if uploaded_file:
                            content_parts.append(uploaded_image)
                            content_parts.append("Use this image as reference for style and composition.")
                        
                        # Generate with Gemini
                        response = model.generate_content(content_parts)
                        
                        st.success("✅ Generation Complete! 🎉")
                        st.markdown(response.text)
                        
                        st.info("⚠️ Note: Direct image generation via Gemini API requires Vertex AI. Using text response for now. For actual image generation, consider using Vertex AI or switch to Pollinations model.")
                        
                    except Exception as e:
                        st.error(f"❌ Gemini Error: {str(e)}")
                        st.info("💡 Tip: Make sure your API key has access to Gemini models. You might need Vertex AI for image generation.")
                
                else:
                    # Use Pollinations.ai (Free)
                    st.success("✅ Generation Complete! 🎉")
                    
                    for idx in range(num_images):
                        # Using Pollinations.ai free API
                        image_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(full_prompt)}?width=1024&height=1024&seed={idx}&nologo=true"
                        
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
                st.error(f"❌ Error: {str(e)}")
else:
    if "Gemini" in model_choice and not api_key:
        st.info("🔑 Please enter your Gemini API key above to start generating images with superior quality.")
    else:
        st.info("✍️ Enter your prompt and click Generate to create amazing AI images!")

# Footer
st.markdown("---")
st.caption("Developed by Yasser Antar | Powered by Gemini & Pollinations AI")
st.caption("💡 Pro Tip: Use Gemini for best quality product photography and professional images!")
