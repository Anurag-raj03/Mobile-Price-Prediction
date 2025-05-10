import streamlit as st
import joblib
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Load the pipeline model
pipeline_model = joblib.load('pipeline.jbl')

def fetch_image_urls(phone_brand, model_name, num_images=5):
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
        
        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Construct the search URL for Amazon based on user input
        search_query = f"{phone_brand} {model_name} smartphone"
        search_url = f"https://www.amazon.com/s?k={search_query}&ref=nb_sb_noss"
        
        # Navigate to the search URL
        driver.get(search_url)
        
        # Wait for the page to load
        driver.implicitly_wait(10)
        
        # Find the image elements using the CSS selector (adjust as needed for Amazon)
        image_elements = driver.find_elements(By.CSS_SELECTOR, '.s-image')
        
        # Extract the image URLs
        image_urls = [element.get_attribute('src') for element in image_elements[:num_images]]
        
        # Close the browser
        driver.quit()
        
        return image_urls
    except Exception as e:
        st.error(f"Error fetching images: {e}")
        return []

# Streamlit app
st.title('Mobile Price Prediction')

# Create form for user input
st.header('Enter Mobile Features')
phone_brand = st.selectbox('Phone Brand', ['Poco', 'Realme', 'Apple', 'Samsung', 'Oppo', 'Google', 'Vivo', 'Nothing', 
                                           'Redmi', 'Mi', 'Xiaomi', 'Nokia', 'Motorola', 'Lenovo', 'Nexus', 
                                           'Infinix', 'Oneplus', 'Huawei', 'Moto', 'Alcatel'])
model_name = st.text_input('Model Name')
rating = st.number_input('Rating', min_value=0.0)
ram_gb = st.number_input('RAM (GB)', min_value=0.0)
rom_gb = st.number_input('ROM (GB)', min_value=0.0)
back_cameras = st.number_input('Number of Back Cameras', min_value=1)
back_mp1 = st.number_input('Back/Rare Camera MP', min_value=0.0)
back_mp2 = st.number_input('Back MP 2', min_value=0.0)
back_mp3 = st.number_input('Back MP 3', min_value=0.0)
back_mp4 = st.number_input('Back MP 4', min_value=0.0)
front_cam_mp = st.number_input('Front Camera MP', min_value=0.0)
front_s_cam_mp = st.number_input('Front S_Camera MP', min_value=0.0)
battery_mah = st.number_input('Battery (mAh)', min_value=0.0)
processor_brand = st.selectbox('Processor Brand', ['Mediatek', 'Helio', 'Qualcomm', 'Unisoc', 'iOS', 'Exynes', 
                                                  'Default', 'Dimensity', 'Google', 'Spreadtrum', 'Hisilicon'])
processor_names = st.text_input('Processor Names')

# Prediction and result display
if st.button('Predict Price'):
    features = pd.DataFrame({'Phone Brand': [phone_brand], 'Model Name': [model_name], 'Rating': [rating], 'RAM IN GB': [ram_gb], 
                'ROM IN GB': [rom_gb], 'No.Back Camera': [back_cameras], 'Back/Rare Camera/MP': [back_mp1], 'Back/MP 2': [back_mp2],
                'Back/MP 3': [back_mp3], 'Back/MP 4': [back_mp4], 'Front Camera MP': [front_cam_mp], 'Front S_Camera MP': [front_s_cam_mp],
                'Battery/mAH': [battery_mah], 'Processor Brand': [processor_brand], 'Processor Names': [processor_names]})
    
    # Predict using the pipeline model
    prediction = pipeline_model.predict(features)[0]
    
    st.success(f'The predicted price is: {prediction}')
    
    # Fetch and display mobile images



# Fetch and display mobile images
    image_urls = fetch_image_urls(phone_brand, model_name)
    if image_urls:
        st.header(f'Images for {phone_brand} {model_name}')
        col1, col2,col3 = st.columns(3)
    
    # Display the first two images
        with col1:
            st.image(image_urls[0], caption=f'{phone_brand} {model_name}', width=170)
        with col2:
            if len(image_urls) > 1:
                st.image(image_urls[1], caption=f'{phone_brand} {model_name}', width=170)
        with col3:
            if len(image_urls) > 1:
                st.image(image_urls[1], caption=f'{phone_brand} {model_name}', width=170)        
    else:
        st.warning('No images found for the specified phone brand and model name.')


