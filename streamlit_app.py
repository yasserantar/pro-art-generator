
import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(
    page_title="Pro Art Generator",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Main Title & Description
st.title("✨ Pro AI Art Generator")
st.markdown("### Generate High-Quality Images using Google Imagen 3")

# 3. API Key Management
# Securely gets the key from Streamlit Secrets or User Input
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    api_key = st.text_input("Enter your Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)

        # 4. User Inputs
        prompt_text = st.text_area("Describe your image (English or Arabic):", height=100, placeholder="E.g., A futuristic city in neon lights...")

        # Advanced Settings Expander
        with st.expander("⚙️ Advanced Settings"):
            col1, col2 = st.columns(2)
            with col1:
                style_mode = st.selectbox(
                    "Art Style:", 
                    ["Photorealistic", "Cinematic", "3D Render", "Anime/Manga", "Oil Painting", "Digital Art", "No Style (Raw)"]
                )
            with col2:
                aspect_ratio = st.selectbox(
                    "Aspect Ratio:", 
                    ["Square (1:1)", "Widescreen (16:9)", "Portrait (9:16)", "Landscape (4:3)"]
                )

        # 5. Generate Button
        if st.button("🚀 Generate Image", use_container_width=True):
            if not prompt_text:
                st.warning("Please enter a description first!")
            else:
                with st.spinner("Generating your masterpiece... 🎨"):
                    try:
                        # Constructing the enhanced prompt
                        style_modifier = ""
                        if style_mode == "Photorealistic":
                            style_modifier = ", photorealistic, 8k, highly detailed, sharp focus, realistic textures"
                        elif style_mode == "Cinematic":
                            style_modifier = ", cinematic lighting, dramatic atmosphere, movie scene, 4k"
                        elif style_mode == "3D Render":
                            style_modifier = ", 3d render, unreal engine 5, octane render, isometric"
                        elif style_mode == "Anime/Manga":
                            style_modifier = ", anime style, studio ghibli, vibrant colors"

                        full_prompt = f"{prompt_text} {style_modifier}"

                        # Call Google Imagen 3 Model
                        model = genai.ImageGenerationModel("imagen-3.0-generate-001")
                        response = model.generate_images(
                            prompt=full_prompt,
                            number_of_images=1,
                            aspect_ratio=aspect_ratio.split(" ")[1].replace("(", "").replace(")", "") if "Square" not in aspect_ratio else "1:1"
                        )

                        # Display Result
                        st.success("Generation Complete! ✨")
                        st.image(response[0].image, caption="Generated Image", use_column_width=True)

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
