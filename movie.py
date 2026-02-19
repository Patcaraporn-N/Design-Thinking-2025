#พัชรพร
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1. ตั้งค่า Chrome Options (เช่น ปรับให้ทำงานแบบ Background หรือไม่)
chrome_options = Options()
# chrome_options.add_argument("--headless") # เปิดบรรทัดนี้หากไม่ต้องการให้หน้าต่าง Browser เด้งขึ้นมา

# 2. เริ่มต้น WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 3. ไปยังหน้าเว็บเป้าหมาย
    url = "https://www.rottentomatoes.com/browse/tv_series_browse/?page=7"
    driver.get(url)
    time.sleep(2) # รอให้หน้าเว็บโหลดครู่หนึ่ง

    # 4. ดึงข้อมูล (ตัวอย่าง: ชื่อหนังทั้งหมดในหน้าแรก)
    movies = driver.find_elements(By.CSS_SELECTOR, ".js-tile-link")

    print(f"พบหนังทั้งหมด {len(movies)} เรื่องในหน้านี้\n")

    for tile in movies:
        # ดึงชื่อหนัง (อยู่ใน span ของ tile)
        title = tile.find_element(By.CSS_SELECTOR, "span[data-qa='discovery-media-list-item-title']").text
        # ดึงราคา (อยู่ในคลาส .price_color)
        try:
            review = tile.find_element(By.CSS_SELECTOR, "rt-text[slot='criticsScore']").text
        except:
            review = "ไม่มีคะแนน"

        
        print(f"ชื่อเรื่อง: {title}")
        print(f"คะแนนจากนักวิจารณ์: {review}")
        print("-" * 20)

finally:
    # 5. ปิด Browser
    driver.quit()

#นันท์ภัส
import streamlit as st
import pandas as pd
st.title("📂 อัปโหลดไฟล์ CSV")

uploaded_file = st.file_uploader("เลือกไฟล์ CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("โหลดไฟล์สำเร็จ ✅")
    st.dataframe(df)
