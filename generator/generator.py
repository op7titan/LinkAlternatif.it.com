import pandas as pd
import os
from jinja2 import Template

# --- KONFIGURASI ---
brands_excel = 'data/brands.xlsx'
news_excel   = 'data/news.xlsx'
output_base  = 'public'

# Baca Data
df_brands = pd.read_excel(brands_excel)
df_news   = pd.read_excel(news_excel)
news_list = df_news.to_dict('records')

# Baca Template Brand
with open('templates/brand_index.html', 'r', encoding='utf-8') as f:
    template_brand = Template(f.read())

# --- LOOPING BRAND ---
for index, brand in df_brands.iterrows():
    folder_name = str(brand['folder_name']).strip()
    
    # 1. PROSES SLIDER (Split string jadi List)
    # Contoh Excel: "slide1.jpg, slide2.jpg" -> ['slide1.jpg', 'slide2.jpg']
    raw_sliders = str(brand['slider_images'])
    slider_list = [s.strip() for s in raw_sliders.split(',')]

    # 2. PROSES WARNA (Default jika kosong di Excel)
    c_primary = brand['color_primary'] if pd.notna(brand['color_primary']) else '#705dd3'
    c_secondary = brand['color_secondary'] if pd.notna(brand['color_secondary']) else '#8769e9'

    # Buat folder
    brand_dir = os.path.join(output_base, folder_name)
    if not os.path.exists(brand_dir):
        os.makedirs(brand_dir)
    
    # 3. RENDER HTML DENGAN VARIABLE BARU
    html = template_brand.render(
        brand_name=brand['brand_name'],
        domain_url=brand['domain_url'],       # <-- URL Domain Asli
        login_url=brand['login_url'],
        register_url=brand['register_url'],
        
        # Kirim Warna
        c_primary=c_primary,
        c_secondary=c_secondary,
        
        # Kirim List Slider
        slider_list=slider_list,
        
        # Kirim Berita
        news_list=news_list
    )
    
    with open(f"{brand_dir}/index.html", 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ {folder_name} selesai (Warna: {c_primary})")