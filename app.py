import streamlit as st
import base64
import os
import re
import json
from datetime import datetime
from FSM import CiputFSM, State

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Ciput Community - Photography Hub",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. DATA KATALOG FOTO
PHOTO_GALLERY = [
    {
        "id": 1,
        "title": "Sunset di Parangtritis",
        "category": "Pantai",
        "photographer": "Andi Saputra",
        "price": 250000,
        "likes": 128,
        "description": "Keindahan matahari terbenam di Pantai Parangtritis Yogyakarta",
        "bg_color": "linear-gradient(135deg, #FF6B35, #F7931E)",
        "image_path": "assets/pantai.jpg",
        "date": "2024-05-15"
    },
    {
        "id": 2,
        "title": "Tari Bedhaya",
        "category": "Culture",
        "photographer": "Sari Dewi",
        "price": 350000,
        "likes": 95,
        "description": "Keanggunan Tari Bedhaya Keraton Yogyakarta",
        "bg_color": "linear-gradient(135deg, #9B59B6, #E74C3C)",
        "image_path": "assets/tari.jpg",
        "date": "2024-05-10"
    },
    {
        "id": 3,
        "title": "Pre-wedding Modern",
        "category": "Wedding",
        "photographer": "Budi Santoso",
        "price": 500000,
        "likes": 203,
        "description": "Konsep pre-wedding modern dengan gaya urban",
        "bg_color": "linear-gradient(135deg, #E91E63, #FF9800)",
        "image_path": "assets/prewed.jpg",
        "date": "2024-05-08"
    },
    {
        "id": 4,
        "title": "Street Photography Malioboro",
        "category": "Street",
        "photographer": "Cahyo Nugroho",
        "price": 180000,
        "likes": 67,
        "description": "Dinamika kehidupan malam di Malioboro",
        "bg_color": "linear-gradient(135deg, #2C3E50, #3498DB)",
        "image_path": "assets/malioboro.jpg",
        "date": "2024-05-05"
    },
    {
        "id": 5,
        "title": "Batik",
        "category": "Culture",
        "photographer": "Dewi Lestari",
        "price": 300000,
        "likes": 156,
        "description": "Elegansi batik dalam potret modern",
        "bg_color": "linear-gradient(135deg, #8E44AD, #C0392B)",
        "image_path": "assets/batik.jpg",
        "date": "2024-05-01"
    },
    {
        "id": 6,
        "title": "Candi Borobudur",
        "category": "Candi",
        "photographer": "Eko Prasetyo",
        "price": 400000,
        "likes": 312,
        "description": "Candi Borobudur saat matahari terbit",
        "bg_color": "linear-gradient(135deg, #27AE60, #F1C40F)",
        "image_path": "assets/borobudur.jpg",
        "date": "2024-04-28"
    }
]

# 3. BANNER
BANNERS = [
    {"id": 1, "title": "Batik Photography", "emoji": "🦋", "bg_color": "linear-gradient(135deg, #0F2C59, #1A3E73)", "desc": "Kolaborasi Batik & Fotografi"},
    {"id": 2, "title": "Pre-wedding Batik", "emoji": "💍", "bg_color": "linear-gradient(135deg, #8B0000, #D4AF37)", "desc": "Momen Spesial dengan Batik"},
    {"id": 3, "title": "Studio Batik", "emoji": "📸", "bg_color": "linear-gradient(135deg, #2E8B57, #D4AF37)", "desc": "Studio Eksklusif Bernuansa Batik"},
    {"id": 4, "title": "Outdoor Hunting", "emoji": "🌳", "bg_color": "linear-gradient(135deg, #D2691E, #D4AF37)", "desc": "Sesi Foto Outdoor Profesional"},
]

# 4. FUNGSI BACKGROUND BATIK
def get_batik_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 400 400">
    <defs>
        <pattern id="batik-parang" x="0" y="0" width="200" height="200" patternUnits="userSpaceOnUse">
            <rect width="200" height="200" fill="#F5EDE0"/>
            <path d="M-20 40 Q30 20 80 40 T180 40" stroke="#0F2C59" stroke-width="3" fill="none" opacity="0.3"/>
            <path d="M-20 90 Q30 70 80 90 T180 90" stroke="#0F2C59" stroke-width="3" fill="none" opacity="0.3"/>
            <path d="M20 60 Q40 50 60 60" stroke="#D4AF37" stroke-width="2" fill="none" opacity="0.5"/>
            <circle cx="40" cy="30" r="3" fill="#D4AF37" opacity="0.4"/>
            <circle cx="90" cy="80" r="3" fill="#D4AF37" opacity="0.4"/>
        </pattern>
        <pattern id="batik-kawung" x="0" y="0" width="150" height="150" patternUnits="userSpaceOnUse">
            <rect width="150" height="150" fill="none"/>
            <circle cx="75" cy="75" r="25" stroke="#0F2C59" stroke-width="2.5" fill="none" opacity="0.25"/>
            <circle cx="75" cy="75" r="18" stroke="#D4AF37" stroke-width="1.5" fill="none" opacity="0.35"/>
            <circle cx="75" cy="75" r="4" fill="#D4AF37" opacity="0.3"/>
        </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#batik-parang)"/>
    <rect width="100%" height="100%" fill="url(#batik-kawung)"/>
</svg>'''

def get_batik_background():
    svg_content = get_batik_svg()
    b64 = base64.b64encode(svg_content.encode()).decode()
    return f"data:image/svg+xml;base64,{b64}"

BATIK_BG = get_batik_background()

# 5. INISIALISASI SESSION STATE
# Inisialisasi photo_gallery
if 'photo_gallery' not in st.session_state:
    st.session_state.photo_gallery = PHOTO_GALLERY.copy()  # Gunakan PHOTO_GALLERY yang sudah ada

if 'liked_photos' not in st.session_state:
    st.session_state.liked_photos = set()

if 'bot' not in st.session_state:
    st.session_state.bot = CiputFSM()
    st.session_state.bot.step()
    st.session_state.history = [{
        "role": "assistant",
        "content": st.session_state.bot.get_response()
    }]
else:
    if 'history' not in st.session_state:
        st.session_state.history = [{
            "role": "assistant",
            "content": st.session_state.bot.get_response()
        }]

# 6. FUNGSI LIKE

def like_photo(photo_id):
    for photo in st.session_state.photo_gallery:
        if photo['id'] == photo_id:
            photo['likes'] += 1
            st.session_state.liked_photos.add(photo_id)
            return True
    return False

# 7. CUSTOM CSS
custom_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Outfit:wght@300;400;600&display=swap');
    
    .stApp {{
        background: url('{BATIK_BG}') repeat;
        background-size: 400px 400px;
        background-attachment: fixed;
    }}
    
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(250, 247, 240, 0.88);
        z-index: -1;
        pointer-events: none;
    }}
    
    .batik-header {{
        background: linear-gradient(135deg, #0F2C59 0%, #1A3E73 100%);
        padding: 40px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 30px;
        border: 2px solid #D4AF37;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}
    
    .batik-header h1 {{
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        color: #FAF7F0;
        margin-bottom: 10px;
    }}
    
    .batik-header p {{
        font-family: 'Outfit', sans-serif;
        color: #D4AF37;
        font-size: 1.1rem;
        letter-spacing: 3px;
    }}
    
    .elegant-card {{
        background: linear-gradient(135deg, #0F2C59, #1A3E73);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        border: 1px solid #D4AF37;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        transition: transform 0.3s;
    }}
    
    .elegant-card:hover {{
        transform: translateY(-5px);
    }}
    
    .elegant-card h2 {{
        color: #D4AF37;
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        margin-bottom: 20px;
        border-left: 4px solid #D4AF37;
        padding-left: 15px;
    }}
    
    .elegant-card p {{
        color: #E6DFD3;
        line-height: 1.7;
    }}
    
    /* Tab yang sedang aktif */
    div[data-baseweb="tab-list"] button[aria-selected="true"] {{
        color: #D4AF37 !important;
        border-bottom: 3px solid #D4AF37 !important;
    }}
    
    .table-container {{
        background: rgba(255,255,255,0.95);
        border-radius: 16px;
        overflow: hidden;
        margin: 20px 0;
        border: 1px solid #D4AF37;
    }}
    
    .table-header {{
        background: linear-gradient(135deg, #0F2C59, #1A3E73);
        padding: 12px 20px;
        border-bottom: 2px solid #D4AF37;
    }}
    
    .table-header h3 {{
        color: #D4AF37;
        margin: 0;
    }}
    
    .table-row {{
        display: flex;
        padding: 12px 20px;
        border-bottom: 1px solid rgba(212,175,55,0.2);
    }}
    
    .table-row:last-child {{
        border-bottom: none;
    }}
    
    .table-icon {{
        font-size: 1.8rem;
        width: 50px;
    }}
    
    .table-text strong {{
        color: #0F2C59;
    }}
    
    .table-text p {{
        color: #555;
        margin: 5px 0 0;
        font-size: 0.85rem;
    }}
    
    .contact-card {{
        background: linear-gradient(135deg, #FFF9E8, #FDF5E0);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #D4AF37;
        margin-bottom: 20px;
    }}
    
    .contact-card h4 {{
        color: #0F2C59;
        margin-bottom: 15px;
    }}
    
    .photo-card {{
        background: white;
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 20px;
        border: 1px solid #D4AF37;
        transition: transform 0.3s;
    }}
    
    .photo-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(212,175,55,0.2);
    }}
    
    .photo-image {{
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 12px 12px 0 0;
    }}
    
    .photo-info {{
        padding: 15px;
    }}
    
    .photo-title {{
        font-family: 'Playfair Display', serif;
        font-size: 1rem;
        font-weight: bold;
        color: #0F2C59;
    }}
    .photo-card img {{
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 12px 12px 0 0;
        transition: transform 0.3s;
    }}

    .photo-card:hover img {{
        transform: scale(1.02);
    }}
    
    .member-card {{
        background: linear-gradient(135deg, #0F2C59, #1A3E73);
        border: 2px solid #D4AF37;
        border-radius: 20px;
        padding: 25px;
        color: white;
    }}
    
    .member-card-title {{
        color: #D4AF37;
        font-size: 1.4rem;
        border-bottom: 2px solid rgba(212,175,55,0.3);
        padding-bottom: 10px;
        margin-bottom: 15px;
    }}
    
    .user-bubble {{
        background: linear-gradient(135deg, #0F2C59, #1A3E73);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 5px 20px;
        max-width: 80%;
        margin-left: auto;
        margin-bottom: 12px;
        border: 1px solid #D4AF37;
    }}
    
    .bot-bubble {{
        background: rgba(255,255,255,0.95);
        color: #1A2E40;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 5px;
        max-width: 80%;
        margin-bottom: 12px;
        border-left: 4px solid #D4AF37;
    }}
    
    /* TOMBOL KOTAK ELEGAN UNTUK CHATBOT */
    div.stButton > button {{
        background: linear-gradient(135deg, #0F2C59, #1A3E73) !important;
        color: white !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 12px !important;
        padding: 10px 5px !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        width: 100%;
        white-space: nowrap;
        height: auto;
        min-height: 55px;
        transition: all 0.3s ease !important;
    }}
    
    div.stButton > button:hover {{
        background: linear-gradient(135deg, #D4AF37, #C5A33A) !important;
        color: #0F2C59 !important;
        transform: translateY(-2px);
        border-color: #0F2C59 !important;
    }}
    
    .invoice-card {{
        background: linear-gradient(135deg, #FFF9E8, #FDF5E0);
        border-left: 5px solid #D4AF37;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
    }}
    
    .batik-divider {{
        height: 2px;
        background: linear-gradient(90deg, transparent, #D4AF37, #D4AF37, transparent);
        margin: 20px 0;
    }}
    
    .badge {{
        background: #D4AF37;
        color: #0F2C59;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: bold;
    }}
    
    .custom-card {{
        background: rgba(255,255,255,0.95);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #D4AF37;
        margin-bottom: 20px;
    }}
    
    .gold-text {{
        color: #D4AF37;
        font-weight: bold;
    }}
    .quote-text {{
        background: rgba(212, 175, 55, 0.15);
        padding: 15px;
        border-radius: 12px;
        margin-top: 15px;
        text-align: center;
        color: #FAF7F0;
        font-style: italic;
        font-weight: 500;
        border-left: 3px solid #D4AF37;
        border-right: 3px solid #D4AF37;
        transition: all 0.3s ease;
    }}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 8. HEADER
st.markdown(
    """
    <div class="batik-header">
        <h1>📸 CIPUT COMMUNITY</h1>
        <p>BATIK & PHOTOGRAPHY HARMONY</p>
        <p style="font-size: 0.9rem; margin-top: 15px; color: #E6DFD3;">
            ✨ Mengabadikan Momen dengan Sentuhan Budaya Nusantara ✨
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 9. TABS
tab_portal, tab_gallery, tab_chatbot = st.tabs(["🏛️ Filosofi Ciput", "📷 Katalog Foto", "💬 CIPUT Bot"])

# ==========================================
# TAB 1: FILOSOFI CIPUT
# ==========================================
with tab_portal:
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # CARD Penjelasan Ciput
        st.markdown("""
        <div class="elegant-card">
            <h2>📖 Apa Itu CIPUT?</h2>
            <p><b>Ciput Community</b> adalah komunitas fotografi profesional yang berbasis di Yogyakarta. 
            Nama <span class="gold-text">CIPUT</span> memiliki makna filosofis yang mendalam:</p>
            <ul style="color: #E6DFD3;">
                <li><b>CI</b> = Cipta — Kreativitas dalam berkarya</li>
                <li><b>PU</b> = Putra — Putra-putri Indonesia</li>
                <li><b>T</b> = Tradisi — Melestarikan budaya Nusantara</li>
            </ul>
            <p>"Cipta Putra Tradisi" berarti <b>“Menciptakan Karya Anak Bangsa yang Berakar pada Tradisi”</b>.</p>
            <div class="quote-text">
                ✨ Menjadikan setiap momen berharga sebagai karya seni yang sarat makna budaya ✨
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # CARD Kenapa Kolaborasi dengan Batik
        st.markdown("""
        <div class="elegant-card">
            <h2>🦋 Kenapa Kolaborasi dengan Batik?</h2>
            <div class="table-container">
                <div class="table-header">
                    <h3>✨ Nilai Filosofi Batik ✨</h3>
                </div>
                <div class="table-row">
                    <div class="table-icon">🎯</div>
                    <div class="table-text">
                        <strong>Identitas Budaya yang Kuat</strong>
                        <p>Batik adalah warisan budaya Indonesia yang diakui UNESCO.</p>
                    </div>
                </div>
                <div class="table-row">
                    <div class="table-icon">🎨</div>
                    <div class="table-text">
                        <strong>Estetika Unik dan Bermakna</strong>
                        <p>Setiap motif batik memiliki filosofi mendalam.</p>
                    </div>
                </div>
                <div class="table-row">
                    <div class="table-icon">📸</div>
                    <div class="table-text">
                        <strong>Momen Berkesan</strong>
                        <p>Pre-wedding, wisuda, family gathering terasa lebih sakral.</p>
                    </div>
                </div>
                <div class="table-row">
                    <div class="table-icon">🌏</div>
                    <div class="table-text">
                        <strong>Promosi Budaya ke Dunia</strong>
                        <p>Setiap foto adalah promosi budaya Indonesia.</p>
                    </div>
                </div>
                <div class="table-row">
                    <div class="table-icon">💝</div>
                    <div class="table-text">
                        <strong>Dukung Ekonomi Kreatif Lokal</strong>
                        <p>Mendukung perajin batik lokal.</p>
                    </div>
                </div>
                <div class="table-row">
                    <div class="table-icon">🕊️</div>
                    <div class="table-text">
                        <strong>Menjaga Warisan Leluhur</strong>
                        <p>Mengajak generasi muda bangga menggunakan batik.</p>
                    </div>
                </div>
            </div>
            <div style="text-align: center; margin-top: 15px; color: #D4AF37">
                <i>"Batik Bukan Sekadar Motif, tapi Cerita. Fotografi Bukan Sekadar Gambar, tapi Kenangan."</i>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        # Motto & Visi
        st.markdown("""
        <div class="elegant-card" style="text-align: center;">
            <div style="font-size: 3rem;">✨</div>
            <h2 style="border-left: none;">Motto Kami</h2>
            <p style="font-family: 'Playfair Display', serif;">"Mengabadikan Momen dengan Sentuhan Budaya Nusantara"</p>
            <div class="batik-divider"></div>
            <h3 style="color: #D4AF37;">Visi</h3>
            <p>Menjadi komunitas fotografi terdepan yang mengangkat kearifan lokal Indonesia.</p>
            <div class="batik-divider"></div>
            <h3 style="color: #D4AF37;">Misi</h3>
            <ul style="text-align: left; color: #FAF7F0 ">
                <li>Melestarikan budaya batik melalui fotografi</li>
                <li>Mengembangkan bakat fotografer muda Indonesia</li>
                <li>Menciptakan karya foto bernilai seni tinggi</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Kontak
        st.markdown("""
        <div class="contact-card">
            <h4>📞 Hubungi Kami</h4>
            <p>📱 WhatsApp: +62 812-3456-7890<br>
            📷 Instagram: @ciput.community<br>
            ✉️ Email: info@ciputcommunity.com<br>
            📍 Yogyakarta, Indonesia</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 2: KATALOG FOTO
# ==========================================
with tab_gallery:
    st.markdown('<div class="batik-divider"></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>🌟 Layanan Unggulan Kami 🌟</h2>", unsafe_allow_html=True)
    
    banner_cols = st.columns(4)
    for idx, banner in enumerate(BANNERS):
        with banner_cols[idx]:
            st.markdown(f"""
            <div style="background: {banner['bg_color']}; border-radius: 16px; padding: 20px; text-align: center; margin-bottom: 20px; border: 1px solid #D4AF37;">
                <div style="font-size: 3rem;">{banner['emoji']}</div>
                <div style="color: #D4AF37; font-weight: bold;">{banner['title']}</div>
                <div style="color: #E6DFD3; font-size: 0.8rem;">{banner['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="batik-divider"></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>📷 Galeri Foto Pilihan</h2>", unsafe_allow_html=True)
    
    categories = ["Semua"] + list(set(p['category'] for p in st.session_state.photo_gallery))
    selected_category = st.selectbox("📂 Filter Kategori", categories)
    
    filtered_photos = st.session_state.photo_gallery if selected_category == "Semua" else [p for p in st.session_state.photo_gallery if p['category'] == selected_category]
    
    # Tampilkan total likes
    total_likes = sum(p['likes'] for p in st.session_state.photo_gallery)
    st.markdown(f"<p style='text-align: center;'>❤️ Total <b>{total_likes}</b> likes dari <b>{len(st.session_state.photo_gallery)}</b> foto</p>", unsafe_allow_html=True)
    st.markdown('<div class="batik-divider"></div>', unsafe_allow_html=True)
    
    # Grid Foto
    # Grid Foto dengan st.image
    cols = st.columns(3)
    for idx, photo in enumerate(filtered_photos):
        with cols[idx % 3]:
            is_liked = photo['id'] in st.session_state.liked_photos
            
            # Coba tampilkan gambar dengan st.image
            try:
                st.image(photo['image_path'], use_container_width=True)
            except:
                # Jika error, tampilkan gradient
                st.markdown(f'<div style="background: {photo["bg_color"]}; height: 180px; display: flex; align-items: center; justify-content: center; font-size: 3rem; border-radius: 12px;">{photo["emoji"]}</div>', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="padding: 10px 0;">
                <div style="font-family: 'Playfair Display', serif; font-size: 1rem; font-weight: bold; color: #0F2C59;">{photo['title']}</div>
                <div style="font-size: 0.75rem; color: #666;">
                    📸 {photo['photographer']} | <span class="badge">{photo['category']}</span>
                </div>
                <div style="font-size: 0.75rem;">❤️ {photo['likes']} likes</div>
                <div style="font-size: 0.7rem; color: #D4AF37; font-weight: bold;">💰 Rp {photo['price']:,}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # TOMBOL LIKE 
            if not is_liked:
                if st.button(f"❤️ Like", key=f"like_{photo['id']}", use_container_width=True):
                    like_photo(photo['id'])
                    st.rerun()
            else:
                st.button(f"✅ Liked", key=f"liked_{photo['id']}", disabled=True, use_container_width=True)

# ==========================================
# TAB 3: CHATBOT (DENGAN TOMBOL KOTAK ELEGAN)
# ==========================================
with tab_chatbot:
    col_chat, col_panel = st.columns([3, 2])
    
    bot = st.session_state.bot
    bot_state = bot.state
    
    with col_panel:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0F2C59, #1A3E73); padding: 20px; border-radius: 20px; margin-bottom: 20px; border: 2px solid #D4AF37; text-align: center;">
            <div style="font-size: 4rem;">📸</div>
            <h3 style="color: #D4AF37;">CIPUT Bot</h3>
            <p style="color: #E6DFD3;">Asisten Virtual Fotografi</p>
        </div>
        """, unsafe_allow_html=True)
        
        lang_map = {"id": "🇮🇩 Indonesia", "en": "🇬🇧 English", "jv": "ꦗ Jawa"}
        rev_map = {"🇮🇩 Indonesia": "id", "🇬🇧 English": "en", "ꦗ Jawa": "jv"}
        current = lang_map.get(bot.language, "🇮🇩 Indonesia")
        selected = st.selectbox("🌐 Pilih Bahasa", list(lang_map.values()))
        if rev_map[selected] != bot.language:
            bot.language = rev_map[selected]
            st.rerun()
        
        st.divider()
        
        if bot_state == State.ORDERING:
            st.markdown("### 🧮 Kalkulator Booking")
            service = st.selectbox("Layanan", ["Sewa Studio", "Sesi Outdoor", "Dokumentasi Event"])
            hours = st.slider("Durasi (Jam)", 1, 12, 2)
            if st.button("➕ Tambah ke Keranjang"):
                price = {"Sewa Studio": 150000, "Sesi Outdoor": 250000, "Dokumentasi Event": 500000}[service]
                bot.cart.append({'item': service, 'qty': hours, 'price': price})
                st.success(f"✅ {service} ({hours} jam) ditambahkan!")
                st.rerun()
            if bot.cart:
                st.markdown("### 🛒 Keranjang")
                for item in bot.cart:
                    st.markdown(f"- {item['item']} x{item['qty']} = Rp {item['price'] * item['qty']:,}")
                st.metric("Total", f"Rp {bot.calculate_total():,}")
                if st.button("✅ Selesai Booking"):
                    st.session_state.history.append({"role": "user", "content": "selesai"})
                    bot.step("selesai")
                    st.session_state.history.append({"role": "assistant", "content": bot.get_response()})
                    st.rerun()
        
        elif bot_state in [State.REG_NAME, State.REG_EMAIL, State.REG_PHONE, State.REG_CONFIRM]:
            st.markdown("### 👤 Kartu Member")
            data = bot.registration_data
            st.markdown(f"""
            <div class="member-card">
                <div class="member-card-title">CIPUT COMMUNITY</div>
                <p><strong>Nama:</strong> {data.get('name', '...')}</p>
                <p><strong>Email:</strong> {data.get('email', '...')}</p>
                <p><strong>WA:</strong> {data.get('phone', '...')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        elif bot_state in [State.CONFIRMATION, State.PAYMENT]:
            st.markdown("### 💳 Pembayaran")
            st.markdown(f"""
            <div class="invoice-card">
                <h3 style="color: #D4AF37;">Rp {bot.calculate_total():,}</h3>
                <p>Transfer ke BCA: 829-1029-381<br>a/n CIPUT COMMUNITY</p>
                <small>Ketik "selesai" setelah transfer</small>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🔄 Reset Chatbot", use_container_width=True):
            st.session_state.bot = CiputFSM()
            st.session_state.bot.step()
            st.session_state.history = [{"role": "assistant", "content": st.session_state.bot.get_response()}]
            st.rerun()
    
    with col_chat:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 💬 CIPUT Assistant")
        
        # 6 TOMBOL KOTAK ELEGAN DALAM 1 BARIS
        cols = st.columns(6)
        
        btn_data = [
            (cols[0], "📸 Info", "info"),
            (cols[1], "💵 Harga", "pricelist"),
            (cols[2], "📞 Kontak", "kontak"),
            (cols[3], "✍️ Daftar", "daftar"),
            (cols[4], "📅 Booking", "booking"),
            (cols[5], "❓ Kenapa", "kenapa ciput")
        ]
        
        for col, label, msg in btn_data:
            with col:
                if st.button(label, key=f"btn_{msg}", use_container_width=True):
                    st.session_state.history.append({"role": "user", "content": msg})
                    bot.step(msg)
                    st.session_state.history.append({"role": "assistant", "content": bot.get_response()})
                    st.rerun()
        
        st.markdown('<div class="batik-divider"></div>', unsafe_allow_html=True)
        
        chat_container = st.container(height=400)
        with chat_container:
            for msg in st.session_state.history:
                formatted = msg["content"].replace("\n", "<br>")
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-bubble">{formatted}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-bubble">📸 {formatted}</div>', unsafe_allow_html=True)
        
        if prompt := st.chat_input("Ketik pesan Anda..."):
            st.session_state.history.append({"role": "user", "content": prompt})
            bot.step(prompt)
            st.session_state.history.append({"role": "assistant", "content": bot.get_response()})
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="batik-divider"></div>
<div style="text-align: center; padding: 20px; color: #7F8C8D;">
    ✨ Ciput Community - Batik & Photography Harmony ✨<br>Yogyakarta, Indonesia
</div>
""", unsafe_allow_html=True)
