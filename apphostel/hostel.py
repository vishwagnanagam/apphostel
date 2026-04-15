import streamlit as st
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="HostelHub – Smart Hostel Booking",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS – Soft Purple Premium Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Poppins:wght@300;400;500;600;700&display=swap');

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f0ff 0%, #ede9fe 50%, #faf5ff 100%) !important;
    color: #2d1b69 !important;
    font-family: 'Poppins', sans-serif !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #7c3aed 0%, #a855f7 60%, #c084fc 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #fff !important; }
[data-testid="stSidebar"] .stSelectbox > div,
[data-testid="stSidebar"] .stTextInput > div > div {
    background: rgba(255,255,255,0.18) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    color: #fff !important;
    border-radius: 12px !important;
}
[data-testid="stSidebar"] .stSlider > div > div > div { background: rgba(255,255,255,0.4) !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ── Typography ── */
h1,h2,h3,h4,h5,h6 { font-family:'Nunito',sans-serif !important; color:#2d1b69 !important; }
body, p, label { font-family:'Poppins',sans-serif !important; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #c084fc 100%);
    border-radius: 28px;
    padding: 60px 56px;
    margin-bottom: 36px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(168,85,247,0.35);
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 40%;
    width: 220px; height: 220px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.22);
    backdrop-filter: blur(10px);
    color: #fff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 7px 18px;
    border-radius: 100px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,255,255,0.3);
    font-family: 'Poppins', sans-serif !important;
}
.hero-title {
    font-family: 'Nunito', sans-serif !important;
    font-size: clamp(42px, 5vw, 72px);
    font-weight: 900;
    line-height: 1.08;
    color: #fff !important;
    margin: 0 0 14px 0;
    text-shadow: 0 4px 20px rgba(0,0,0,0.15);
}
.hero-sub {
    font-family: 'Poppins', sans-serif !important;
    font-size: 16px;
    color: rgba(255,255,255,0.85) !important;
    max-width: 520px;
    line-height: 1.75;
    margin: 0 0 30px 0;
}
.hero-stats { display: flex; gap: 36px; flex-wrap: wrap; }
.hero-stat .num {
    font-family: 'Nunito', sans-serif;
    font-size: 30px; font-weight: 800;
    color: #fff !important;
}
.hero-stat .lbl {
    font-family: 'Poppins', sans-serif;
    font-size: 12px;
    color: rgba(255,255,255,0.7) !important;
    margin-top: 2px;
}

/* ── Section Titles ── */
.section-title {
    font-family: 'Nunito', sans-serif !important;
    font-size: 28px; font-weight: 800;
    color: #2d1b69 !important;
    margin: 0 0 4px 0;
}
.section-sub {
    font-family: 'Poppins', sans-serif;
    font-size: 14px;
    color: #7c3aed !important;
    margin: 0 0 22px 0;
    font-weight: 500;
}

/* ── Hostel Cards ── */
.hostel-card {
    background: #fff;
    border-radius: 22px;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(124,58,237,0.10);
    margin-bottom: 24px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: fadeUp 0.5s ease both;
    border: 1.5px solid rgba(168,85,247,0.10);
}
.hostel-card:hover {
    transform: translateY(-7px);
    box-shadow: 0 20px 48px rgba(124,58,237,0.22);
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(20px); }
    to   { opacity:1; transform:translateY(0); }
}
.card-img-wrap { position:relative; overflow:hidden; height:190px; }
.card-img-wrap img { width:100%; height:100%; object-fit:cover; transition: transform 0.5s; }
.hostel-card:hover .card-img-wrap img { transform: scale(1.07); }
.card-badge {
    position: absolute; top: 12px; left: 12px;
    padding: 4px 12px; border-radius: 100px;
    font-size: 11px; font-weight: 700; letter-spacing: 0.8px;
    text-transform: uppercase; font-family: 'Poppins', sans-serif;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.badge-premium { background: linear-gradient(90deg,#f59e0b,#ef4444); color:#fff; }
.badge-budget  { background: linear-gradient(90deg,#10b981,#06b6d4); color:#fff; }
.badge-type {
    position: absolute; top: 12px; right: 12px;
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(6px);
    color: #7c3aed;
    padding: 4px 12px; border-radius: 100px;
    font-size: 11px; font-weight: 700; letter-spacing: 0.8px;
    text-transform: uppercase; font-family: 'Poppins', sans-serif;
    border: 1px solid rgba(124,58,237,0.2);
}
.card-body { padding: 18px 18px 14px 18px; }
.card-name {
    font-family: 'Nunito', sans-serif;
    font-size: 17px; font-weight: 800;
    color: #2d1b69; margin: 0 0 5px 0;
}
.card-loc { font-size: 12px; color: #a78bfa; margin: 0 0 12px 0; font-weight: 500; }
.card-row {
    display: flex; align-items: center;
    justify-content: space-between; margin-bottom: 10px;
}
.card-price {
    font-family: 'Nunito', sans-serif;
    font-size: 20px; font-weight: 800; color: #7c3aed;
}
.card-price small { font-size: 11px; color: #a78bfa; font-weight: 500; }
.stars { color: #f59e0b; font-size: 13px; }
.rating-num { font-size: 12px; color: #9ca3af; margin-left: 3px; }
.facilities { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 10px; }
.fac-chip {
    background: #f3e8ff; border: 1px solid #e9d5ff;
    color: #7c3aed; font-size: 10px; padding: 3px 9px;
    border-radius: 100px; font-family: 'Poppins', sans-serif; font-weight: 600;
}
.avail-dot {
    display: inline-block; width: 8px; height: 8px;
    border-radius: 50%; margin-right: 5px; vertical-align: middle;
}
.avail-text { font-size: 12px; color: #6b7280; font-weight: 500; }

/* ── Detail Page ── */
.detail-banner {
    border-radius: 22px; overflow: hidden;
    height: 320px; margin-bottom: 24px;
    position: relative; box-shadow: 0 12px 40px rgba(124,58,237,0.2);
}
.detail-banner img { width:100%; height:100%; object-fit:cover; }
.detail-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(to top, rgba(45,27,105,0.80) 0%, transparent 60%);
}
.detail-overlay-content { position: absolute; bottom: 24px; left: 28px; }
.info-box {
    background: #fff;
    border: 1.5px solid #e9d5ff;
    border-radius: 18px; padding: 22px; margin-bottom: 18px;
    box-shadow: 0 4px 20px rgba(124,58,237,0.07);
}
.info-box h3 {
    font-family: 'Nunito', sans-serif;
    font-size: 18px; font-weight: 800;
    color: #2d1b69; margin: 0 0 12px 0;
}
.price-tag {
    font-family: 'Nunito', sans-serif;
    font-size: 38px; font-weight: 900;
    color: #7c3aed;
}
.gallery-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 10px; margin-bottom: 20px;
}
.gallery-img {
    border-radius: 14px; overflow: hidden; height: 140px;
}
.gallery-img img { width:100%; height:100%; object-fit:cover; }

/* ── Reviews ── */
.review-card {
    background: #faf5ff;
    border: 1px solid #e9d5ff;
    border-radius: 14px; padding: 14px; margin-bottom: 10px;
}
.review-author {
    font-family: 'Nunito', sans-serif;
    font-size: 14px; font-weight: 700; color: #2d1b69; margin-bottom: 3px;
}
.review-stars { color: #f59e0b; font-size: 13px; }
.review-comment { font-size: 13px; color: #6b7280; margin-top: 5px; line-height: 1.6; }

/* ── Recommendation cards ── */
.rec-card {
    background: #fff;
    border: 1.5px solid #e9d5ff;
    border-left: 4px solid #a855f7;
    border-radius: 16px; padding: 14px 16px; margin-bottom: 10px;
    box-shadow: 0 3px 14px rgba(124,58,237,0.08);
    transition: border-left-color 0.2s, transform 0.2s;
}
.rec-card:hover { border-left-color: #7c3aed; transform: translateX(3px); }
.rec-name { font-family:'Nunito',sans-serif; font-size:15px; font-weight:800; color:#2d1b69; margin-bottom:3px; }
.rec-meta { font-size:12px; color:#9ca3af; }
.rec-price { font-size:14px; font-weight:700; color:#7c3aed; margin-top:4px; }

/* ── Booking Confirmed ── */
.booking-confirmed {
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
    border-radius: 22px;
    padding: 32px 36px;
    margin: 16px 0;
    box-shadow: 0 12px 40px rgba(124,58,237,0.3);
    text-align: center;
    animation: fadeUp 0.6s ease;
}
.booking-confirmed .big-emoji { font-size: 52px; margin-bottom: 10px; }
.booking-confirmed h2 {
    font-family: 'Nunito', sans-serif !important;
    font-size: 28px; font-weight: 900;
    color: #fff !important; margin: 0 0 6px 0;
}
.booking-confirmed p { color: rgba(255,255,255,0.88) !important; font-size: 14px; line-height: 1.7; }
.booking-detail-row {
    display: flex; justify-content: space-between;
    background: rgba(255,255,255,0.15);
    border-radius: 12px; padding: 10px 16px; margin-top: 10px;
}
.booking-detail-label { color: rgba(255,255,255,0.7) !important; font-size: 12px; font-weight: 500; }
.booking-detail-val   { color: #fff !important; font-size: 14px; font-weight: 700; }

/* ── Admin Panel ── */
.admin-header {
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    border-radius: 18px; padding: 24px 28px; margin-bottom: 24px;
    box-shadow: 0 8px 30px rgba(124,58,237,0.25);
}
.admin-header h2 { color: #fff !important; font-family: 'Nunito', sans-serif !important; font-size: 24px; margin: 0; }
.admin-header p  { color: rgba(255,255,255,0.8) !important; font-size: 13px; margin: 4px 0 0 0; }
.admin-stat-card {
    background: #fff;
    border: 1.5px solid #e9d5ff;
    border-radius: 16px; padding: 20px; text-align: center;
    box-shadow: 0 4px 16px rgba(124,58,237,0.08);
}
.admin-stat-num {
    font-family: 'Nunito', sans-serif;
    font-size: 32px; font-weight: 900; color: #7c3aed;
}
.admin-stat-lbl { font-size: 12px; color: #9ca3af; font-weight: 600; margin-top: 2px; }

/* ── Sidebar styled ── */
.sidebar-brand {
    text-align: center;
    padding: 10px 0 18px 0;
    border-bottom: 1px solid rgba(255,255,255,0.2);
    margin-bottom: 18px;
}
.sidebar-brand .brand-icon { font-size: 36px; display: block; margin-bottom: 6px; }
.sidebar-brand .brand-name {
    font-family: 'Nunito', sans-serif;
    font-size: 22px; font-weight: 900; color: #fff !important; display: block;
}
.sidebar-brand .brand-tag {
    font-size: 11px; color: rgba(255,255,255,0.7) !important;
    letter-spacing: 1px; display: block; margin-top: 2px;
}
.sidebar-nav-label {
    font-size: 10px; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: rgba(255,255,255,0.55) !important;
    margin-bottom: 8px; margin-top: 16px; display: block;
}
.fav-item {
    background: rgba(255,255,255,0.15);
    border-radius: 12px; padding: 10px 13px; margin-bottom: 8px;
    border: 1px solid rgba(255,255,255,0.2);
}
.fav-name { font-size: 13px; font-weight: 700; color: #fff !important; }
.fav-price { font-size: 11px; color: rgba(255,255,255,0.75) !important; margin-top: 2px; }

/* ── Streamlit overrides ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important; font-size: 14px !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 14px rgba(124,58,237,0.28) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(124,58,237,0.38) !important;
    opacity: 0.92 !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.2) !important;
    border: 1px solid rgba(255,255,255,0.35) !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.32) !important;
}
.stTextInput > div > div, .stTextArea > div > div,
.stSelectbox > div, .stNumberInput > div > div {
    background: #fff !important;
    border: 1.5px solid #e9d5ff !important;
    border-radius: 12px !important;
    color: #2d1b69 !important;
}
.stTextInput input, .stTextArea textarea, .stNumberInput input {
    color: #2d1b69 !important;
    font-family: 'Poppins', sans-serif !important;
}
.stSlider > div > div { accent-color: #a855f7; }
div[data-testid="stMetric"] {
    background: #fff; border: 1.5px solid #e9d5ff;
    border-radius: 16px; padding: 16px;
    box-shadow: 0 3px 12px rgba(124,58,237,0.07);
}
div[data-testid="stMetric"] label { color: #7c3aed !important; font-weight: 600 !important; }
.stSuccess { background: #f0fdf4 !important; border: 1.5px solid #86efac !important; border-radius: 14px !important; }
.stWarning { background: #fffbeb !important; border: 1.5px solid #fde68a !important; border-radius: 14px !important; }
.stError   { background: #fff1f2 !important; border: 1.5px solid #fca5a5 !important; border-radius: 14px !important; }
.stDataFrame { border-radius: 14px !important; overflow: hidden; border: 1.5px solid #e9d5ff !important; }
hr { border-color: rgba(168,85,247,0.15) !important; }
.material-icons{
    font-family: 'Material Icons' !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────
DB = "hostelhub.db"

def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS hostels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, location TEXT, price INTEGER,
        rating REAL, facilities TEXT, image TEXT,
        available_rooms INTEGER, type TEXT, description TEXT,
        contact TEXT, tag TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hostel_id INTEGER, user_name TEXT,
        user_email TEXT, user_phone TEXT,
        rooms_booked INTEGER, message TEXT,
        total_price INTEGER, booked_at TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hostel_id INTEGER, reviewer_name TEXT,
        rating INTEGER, comment TEXT
    )""")

    # Seed hostels if empty
    c.execute("SELECT COUNT(*) FROM hostels")
    if c.fetchone()[0] == 0:
        hostels = [
            # ── Girls hostels ──
            ("Sri Lakshmi Girls Hostel", "Gandi Maisamma, Hyderabad", 5500, 4.7,
             "WiFi,Food,Laundry,Hot Water",
             "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=700",
             12, "Girls",
             "Spacious, well-ventilated rooms with 24/7 security and CCTV. Homely atmosphere with nutritious vegetarian meals included. Walking distance from MRECW.",
             "+91 98765 43210", "Premium"),
            ("Sai Nivas Ladies Hostel", "Gandi Maisamma, Hyderabad", 4200, 4.3,
             "WiFi,Food,Hot Water",
             "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=700",
             8, "Girls",
             "Budget-friendly hostel with clean rooms, filtered water, and a friendly warden. Just 5 minutes from MRECW college gate.",
             "+91 98761 12345", "Budget Friendly"),
            ("Padmavathi Girls Residency", "Gandi Maisamma, Hyderabad", 6500, 4.8,
             "WiFi,Food,Laundry,Hot Water,AC",
             "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=700",
             5, "Girls",
             "Premium air-conditioned rooms with attached bathrooms. High-speed WiFi, gym access, and daily housekeeping. Best-in-class for students.",
             "+91 99887 65432", "Premium"),
            ("Vaishnavi Ladies Hostel", "Gandi Maisamma, Hyderabad", 4800, 4.1,
             "WiFi,Food,Laundry",
             "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=700",
             15, "Girls",
             "Affordable and safe hostel with strict timings and warden supervision. Meals include breakfast, lunch, and dinner.",
             "+91 97654 32109", "Budget Friendly"),
            ("Anugraha Women's Hostel", "Gandi Maisamma, Hyderabad", 5800, 4.5,
             "WiFi,Food,Hot Water,Laundry",
             "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=700",
             9, "Girls",
             "Modern hostel with biometric entry, solar hot water, and study room. Excellent mess quality rated by students.",
             "+91 98080 55567", "Premium"),
            ("Gayatri Girls Residency", "Gandi Maisamma, Hyderabad", 3900, 4.0,
             "WiFi,Hot Water",
             "https://images.unsplash.com/photo-1560448204-603b3fc33ddc?w=700",
             18, "Girls",
             "Most economical hostel near MRECW. Clean dorms, reliable WiFi, and a homely environment. Ideal for first-year students.",
             "+91 96543 21098", "Budget Friendly"),
            ("Kavitha Ladies Hostel", "Gandi Maisamma, Hyderabad", 5200, 4.4,
             "WiFi,Food,Laundry,Hot Water",
             "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=700",
             7, "Girls",
             "Well-maintained hostel with spacious rooms and a rooftop study area. Offers both veg and non-veg meal options.",
             "+91 95432 10987", "Premium"),
            ("Bhagyalakshmi Girls Hostel", "Gandi Maisamma, Hyderabad", 4500, 4.2,
             "WiFi,Food,Hot Water",
             "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=700",
             11, "Girls",
             "Centrally located near MRECW with CCTV surveillance and emergency medical support. Parent-approved and trusted hostel.",
             "+91 94321 09876", "Budget Friendly"),
            # ── Boys hostels ──
            ("Surya Boys Hostel", "Gandi Maisamma, Hyderabad", 4600, 4.3,
             "WiFi,Food,Laundry,Hot Water",
             "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=700",
             14, "Boys",
             "Spacious boys hostel with a gaming lounge, gym area, and rooftop hangout space. Great WiFi and decent food.",
             "+91 93210 98765", "Budget Friendly"),
            ("Chaitanya Men's Residency", "Gandi Maisamma, Hyderabad", 6000, 4.6,
             "WiFi,Food,Laundry,Hot Water,AC",
             "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=700",
             6, "Boys",
             "Premium AC boys hostel with attached bathrooms, high-speed fiber internet, and a well-equipped study room. Near MRECW.",
             "+91 92109 87654", "Premium"),
            ("Srinivas Boys Hostel", "Gandi Maisamma, Hyderabad", 4000, 4.1,
             "WiFi,Hot Water,Food",
             "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=700&crop=bottom",
             20, "Boys",
             "Budget-friendly option for boys with hygienic food and 24-hour security. Shared rooms available at lowest price.",
             "+91 91098 76543", "Budget Friendly"),
            ("Venkat Nivas Boys Hostel", "Gandi Maisamma, Hyderabad", 5300, 4.4,
             "WiFi,Food,Laundry,Hot Water",
             "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=700&crop=center",
             10, "Boys",
             "Mid-range boys hostel with two-sharing rooms, study hall, and indoor sports area. Popular among seniors.",
             "+91 90987 65432", "Premium"),
            ("Ravi Kumar Boys PG", "Gandi Maisamma, Hyderabad", 4900, 4.2,
             "WiFi,Food,Hot Water",
             "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=700&crop=top",
             8, "Boys",
             "Clean and comfortable PG accommodation for boys. Includes power backup and filtered drinking water.",
             "+91 89876 54321", "Budget Friendly"),
            ("Krishna Boys Residency", "Gandi Maisamma, Hyderabad", 6200, 4.7,
             "WiFi,Food,Laundry,Hot Water,AC,Gym",
             "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=700&crop=top",
             4, "Boys",
             "Top-rated boys hostel with AC rooms, gym, and cafeteria. Limited seats — book early for best experience near MRECW.",
             "+91 88765 43210", "Premium"),
            ("Balaji Boys Hostel", "Gandi Maisamma, Hyderabad", 3800, 3.9,
             "WiFi,Hot Water",
             "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=700",
             22, "Boys",
             "Most affordable boys hostel. Basic but clean facilities. Perfect for students on a tight budget. Walking distance from college.",
             "+91 87654 32109", "Budget Friendly"),
            ("Mahesh Boys Premium PG", "Gandi Maisamma, Hyderabad", 7000, 4.9,
             "WiFi,Food,Laundry,Hot Water,AC,Gym,TV",
             "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=700&crop=right",
             3, "Boys",
             "Luxury PG for boys with fully furnished single rooms, daily cleaning, power backup, and a dedicated study lounge. The best in the area.",
             "+91 86543 21098", "Premium"),
        ]
        c.executemany("""INSERT INTO hostels
            (name,location,price,rating,facilities,image,available_rooms,type,description,contact,tag)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""", hostels)

    # Seed default reviews if empty
    c.execute("SELECT COUNT(*) FROM reviews")
    if c.fetchone()[0] == 0:
        default_reviews = [
            # hostel_id, reviewer_name, rating, comment
            (1, "Ananya S.", 5, "Absolutely love this hostel! The food is amazing and the staff is so caring. Feels just like home."),
            (1, "Priya R.", 4, "Great security and clean rooms. WiFi could be faster but overall very happy here."),
            (1, "Divya K.", 5, "Best girls hostel near MRECW. The warden is very supportive. Highly recommended!"),
            (2, "Meena T.", 4, "Very affordable and clean. Perfect for first-year students. Food is good too."),
            (2, "Sneha P.", 4, "Nice hostel at a great price. The warden is strict but caring. Good experience."),
            (3, "Lakshmi G.", 5, "Premium hostel with amazing AC rooms! The gym and study area are top notch. Worth every rupee."),
            (3, "Pooja M.", 5, "The best hostel I've stayed in. Clean, comfortable, great food. Highly recommended!"),
            (3, "Varsha N.", 4, "Excellent facilities and very safe. A bit pricey but definitely worth it."),
            (4, "Rekha J.", 4, "Decent hostel with good food. The laundry service is very convenient. Would recommend."),
            (4, "Archana B.", 4, "Safe and affordable. Good for budget-conscious students. Staff is helpful."),
            (5, "Swathi C.", 5, "Modern and clean. The biometric entry makes me feel very safe. Food is excellent!"),
            (5, "Nidhi A.", 4, "Great hostel overall. The study room is my favourite spot. WiFi is very fast."),
            (6, "Kavya R.", 4, "Most budget-friendly option near college. Basic but clean and safe. Happy with my choice."),
            (6, "Sindhu K.", 3, "Good for the price. Rooms are a bit small but clean. Staff is friendly."),
            (7, "Harini P.", 4, "Loved the rooftop study area! Great food options including non-veg. Comfortable stay."),
            (7, "Bhavana S.", 5, "Really well maintained hostel. The staff goes above and beyond. Excellent experience!"),
            (8, "Padma L.", 4, "Reliable hostel with good security. Close to college which is very convenient."),
            (8, "Usha M.", 4, "Parent-approved for a reason! Very safe and clean. The medical support is a great feature."),
            (9, "Kiran T.", 4, "Boys hostel with great vibes. The gaming lounge is a big plus. Good food and WiFi."),
            (9, "Ravi K.", 5, "Best boys hostel in the area. Rooftop hangout is amazing. Highly recommend!"),
            (10, "Arjun S.", 5, "Premium hostel with all amenities. AC rooms are a game-changer. WiFi is super fast."),
            (10, "Suresh P.", 4, "Great study room and attached bathroom. Pricey but quality is top-notch."),
            (11, "Manoj R.", 4, "Budget-friendly and clean. Food is decent. Good option for first-year students."),
            (11, "Vijay N.", 3, "Basic facilities but safe and clean. Good for the price. Staff is helpful."),
            (12, "Arun B.", 4, "Mid-range hostel with great two-sharing rooms. Study hall is very useful."),
            (12, "Deepak C.", 5, "Popular among seniors for a reason! Great facilities and good food. Loved it."),
            (13, "Sanjay M.", 4, "Clean and comfortable PG. Power backup is very useful. Drinking water is filtered."),
            (13, "Rahul P.", 4, "Good hostel at a fair price. Staff is cooperative. Happy with my stay."),
            (14, "Ashwin K.", 5, "Top-rated for a reason! Gym and cafeteria are excellent. AC rooms are super comfy."),
            (14, "Varun S.", 5, "Best boys hostel near MRECW. Limited seats but totally worth it. Book early!"),
            (15, "Ganesh R.", 4, "Most affordable option. Basic but clean. Perfect for budget students. Close to college."),
            (15, "Pavan T.", 3, "Rooms are small but it's very cheap. Clean and safe. Good for tight budgets."),
            (16, "Nikhil A.", 5, "Luxury PG experience! Single rooms, daily cleaning, amazing study lounge. Worth every penny!"),
            (16, "Rohit S.", 5, "The absolute best hostel in the area. Fully furnished and all amenities. Highly recommended!"),
        ]
        c.executemany("""INSERT INTO reviews (hostel_id, reviewer_name, rating, comment)
                         VALUES (?,?,?,?)""", default_reviews)

    conn.commit()
    conn.close()

init_db()

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def get_valid_image(img):
    if not img or img.strip() == "":
        return "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=700"
    
    if "unsplash.com" not in img:
        return "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=700"
    
    return img
def fetch_hostels(search="", type_filter="All", min_price=0, max_price=10000,
                  min_rating=0.0, sort_by="Default"):
    conn = get_conn()
    c = conn.cursor()
    query = "SELECT * FROM hostels WHERE price BETWEEN ? AND ? AND rating >= ?"
    params = [min_price, max_price, min_rating]
    if type_filter != "All":
        query += " AND type = ?"
        params.append(type_filter)
    if search:
        query += " AND (name LIKE ? OR location LIKE ? OR tag LIKE ?)"
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]
    if sort_by == "Price: Low to High":
        query += " ORDER BY price ASC"
    elif sort_by == "Price: High to Low":
        query += " ORDER BY price DESC"
    else:
        query += " ORDER BY rating DESC"
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_hostel(hid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM hostels WHERE id=?", (hid,))
    row = c.fetchone()
    conn.close()
    return row

def book_hostel(hid, user_name, user_email, user_phone, rooms, message):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT available_rooms, price FROM hostels WHERE id=?", (hid,))
    row = c.fetchone()
    avail, price = row
    if rooms > avail:
        conn.close()
        return False, 0
    total = price * rooms
    booked_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("UPDATE hostels SET available_rooms=available_rooms-? WHERE id=?", (rooms, hid))
    c.execute("""INSERT INTO bookings
        (hostel_id,user_name,user_email,user_phone,rooms_booked,message,total_price,booked_at)
        VALUES (?,?,?,?,?,?,?,?)""",
        (hid, user_name, user_email, user_phone, rooms, message, total, booked_at))
    conn.commit()
    conn.close()
    return True, total

def add_review(hostel_id, name, rating, comment):
    import sqlite3
    conn = sqlite3.connect("hostel.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO reviews (hostel_id, name, rating, comment) VALUES (?, ?, ?, ?)",
        (hostel_id, name, rating, comment)
    )

    conn.commit()
    conn.close()

def fetch_reviews(hid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT reviewer_name,rating,comment FROM reviews WHERE hostel_id=?", (hid,))
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_all_bookings():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""SELECT b.id, h.name, b.user_name, b.user_email, b.user_phone,
                        b.rooms_booked, b.total_price, b.booked_at
                 FROM bookings b JOIN hostels h ON b.hostel_id=h.id
                 ORDER BY b.id DESC""")
    rows = c.fetchall()
    conn.close()
    return rows

def add_hostel_admin(name, location, price, htype, facilities, image,
                     available_rooms, contact, description, tag):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""INSERT INTO hostels
        (name,location,price,rating,facilities,image,available_rooms,type,description,contact,tag)
        VALUES (?,?,?,4.0,?,?,?,?,?,?,?)""",
        (name, location, price, facilities, image, available_rooms, htype, description, contact, tag))
    conn.commit()
    conn.close()

def get_recommendations():
    conn = get_conn()
    c = conn.cursor()
    # Score = rating * 10 - price / 600 + availability bonus
    c.execute("""SELECT *, (rating * 10 - price / 600.0 + CASE WHEN available_rooms > 10 THEN 3
                 WHEN available_rooms > 5 THEN 1 ELSE 0 END) AS score
                 FROM hostels WHERE available_rooms > 0
                 ORDER BY score DESC LIMIT 4""")
    rows = c.fetchall()
    conn.close()
    return rows

def star_str(rating):
    full  = int(rating)
    half  = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty

def simulate_email(user_name, user_email, hostel_name, rooms, total):
    """Simulate email sending — logs to session state as confirmation."""
    email_body = f"""
    Dear {user_name},

    🎉 Your booking is CONFIRMED!

    ─────────────────────────────
    Hostel   : {hostel_name}
    Rooms    : {rooms}
    Total    : ₹{total:,}/month
    ─────────────────────────────

    Thank you for choosing HostelHub!
    For support, contact us at support@hostelhub.in

    Warm regards,
    HostelHub Team 🏨
    """
    # Store in session state as "sent email log"
    if "email_log" not in st.session_state:
        st.session_state.email_log = []
    st.session_state.email_log.append({
        "to": user_email, "subject": f"Booking Confirmed – {hostel_name}",
        "body": email_body
    })
    return True

# Extra Unsplash images per hostel category for gallery
GALLERY_IMAGES = {
    "Girls": [
        "https://images.unsplash.com/photo-1560185893-a55cbc8c57e8?w=500",
        "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500",
        "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=500",
    ],
    "Boys": [
        "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=500",
        "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=500",
        "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500",
    ],
}

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for key, val in [("page","home"),("selected_id",None),("favorites",[]),
                 ("booking_confirmed",None),("email_log",[])]:
    if key not in st.session_state:
        st.session_state[key] = val

def go_detail(hid):
    st.session_state.selected_id = hid
    st.session_state.page = "detail"
    st.session_state.booking_confirmed = None

def go_home():
    st.session_state.page = "home"
    st.session_state.booking_confirmed = None

def go_admin():
    st.session_state.page = "admin"

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span class="brand-icon">🏨</span>
        <span class="brand-name">HostelHub</span>
        <span class="brand-tag">☰ MRECW Smart Booking</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="sidebar-nav-label">🧭 Navigation</span>', unsafe_allow_html=True)
    if st.button("Browse Hostels", use_container_width=True):
        go_home()
    if st.button("Admin Panel", use_container_width=True):
        go_admin()

    st.markdown('<span class="sidebar-nav-label">🔍 Filters</span>', unsafe_allow_html=True)
    search = st.text_input("Search hostel / area", placeholder="e.g. Premium, Girls…")
    type_filter = st.selectbox("Hostel Type", ["All", "Girls", "Boys"])
    price_range = st.slider("Price Range (₹/month)", 2000, 10000, (3000, 7500), step=100)
    min_rating  = st.slider("Min Rating ⭐", 0.0, 5.0, 3.5, step=0.1)
    sort_by     = st.selectbox("Sort By", ["Default","Price: Low to High","Price: High to Low"])

    st.markdown('<span class="sidebar-nav-label">❤️ My Favourites</span>', unsafe_allow_html=True)
    if st.session_state.favorites:
        for fid in st.session_state.favorites:
            h = fetch_hostel(fid)
            if h:
                st.markdown(f"""
                <div class="fav-item">
                  <div class="fav-name">{h[1]}</div>
                  <div class="fav-price">₹{h[3]:,}/mo · {h[8]}</div>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:rgba(255,255,255,0.5);font-size:12px;">No favourites yet.<br>Click 🤍 on any hostel!</p>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────
def render_home():
    # Hero
    st.markdown("""
    <div class="hero">
      <div class="hero-badge">🎓 Exclusively for Students</div>
      <div class="hero-title">HostelHub</div>
      <div class="hero-sub">Premium hostel listings near Malla Reddy Engineering College, Gandi Maisamma — Hyderabad's most trusted student housing platform.</div>
      <div class="hero-stats">
        <div class="hero-stat"><div class="num">16+</div><div class="lbl">Verified Hostels</div></div>
        <div class="hero-stat"><div class="num">800+</div><div class="lbl">Happy Students</div></div>
        <div class="hero-stat"><div class="num">4.4★</div><div class="lbl">Avg. Rating</div></div>
        <div class="hero-stat"><div class="num">100%</div><div class="lbl">Safe & Verified</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Smart Recommendations
    st.markdown('<div class="section-title">🤖 Smart Picks For You</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Top-scored hostels based on rating, price & room availability</div>', unsafe_allow_html=True)

    recs = get_recommendations()
    rcols = st.columns(4)
    for i, h in enumerate(recs):
        with rcols[i]:
            st.markdown(f"""
            <div class="rec-card">
              <div class="rec-name">{h[1]}</div>
              <div class="rec-meta">{h[8]} · {star_str(h[4])} {h[4]}</div>
              <div class="rec-price">₹{h[3]:,}/mo · {h[7]} rooms</div>
            </div>""", unsafe_allow_html=True)
            if st.button("View →", key=f"rec_{h[0]}", use_container_width=True):
                go_detail(h[0])
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # All Listings
    hostels = fetch_hostels(
        search=search, type_filter=type_filter,
        min_price=price_range[0], max_price=price_range[1],
        min_rating=min_rating, sort_by=sort_by,
    )

    girls_count = sum(1 for h in hostels if h[8] == "Girls")
    boys_count  = sum(1 for h in hostels if h[8] == "Boys")

    st.markdown(f'<div class="section-title">All Hostels</div>', unsafe_allow_html=True)
    if not hostels:
        st.warning("No hostels match your filters. Try adjusting the search or filters.")
        return

    cols = st.columns(3)
    for i, h in enumerate(hostels):
        hid, name, loc, price, rating, facs, img, avail, htype, desc, contact, tag = h[:12]
        
        fac_list    = facs.split(",")
        avail_color = "#10b981" if avail > 5 else ("#f59e0b" if avail > 0 else "#ef4444")
        avail_text  = f"{avail} rooms left" if avail > 0 else "Fully Booked"
        badge_cls   = "badge-premium" if tag == "Premium" else "badge-budget"
        fac_chips   = "".join([f'<span class="fac-chip">{f.strip()}</span>' for f in fac_list[:4]])

        with cols[i % 3]:
            st.markdown(f"""
            <div class="hostel-card">
              <div class="card-img-wrap">
                <img src="{get_valid_image(img)}" 
                    onerror="this.src='https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=700';"
                    alt="{name}" loading="lazy">
                <span class="card-badge {badge_cls}">{tag}</span>
                <span class="badge-type">{htype}</span>
              </div>
              <div class="card-body">
                <div class="card-name">{name}</div>
                <div class="card-loc">📍 {loc}</div>
                <div class="card-row">
                  <div class="card-price">₹{price:,}<small>/month</small></div>
                  <div><span class="stars">{star_str(rating)}</span><span class="rating-num">{rating}</span></div>
                </div>
                <div class="facilities">{fac_chips}</div>
                <div class="avail-text">
                  <span class="avail-dot" style="background:{avail_color}"></span>
                  {avail_text}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            bcol1, bcol2 = st.columns([3, 1])
            with bcol1:
                if st.button("View Details", key=f"view_{hid}", use_container_width=True):
                    go_detail(hid)
                    st.rerun()
            with bcol2:
                heart = "❤️" if hid in st.session_state.favorites else "🤍"
                if st.button(heart, key=f"fav_{hid}"):
                    if hid in st.session_state.favorites:
                        st.session_state.favorites.remove(hid)
                    else:
                        st.session_state.favorites.append(hid)
                    st.rerun()

# ─────────────────────────────────────────────
# DETAIL PAGE
# ─────────────────────────────────────────────
def render_detail():
    hid = st.session_state.selected_id
    h   = fetch_hostel(hid)
    if not h:
        st.error("Hostel not found.")
        go_home(); return

    hid2, name, loc, price, rating, facs, img, avail, htype, desc, contact, tag = h[:12]
    fac_list    = facs.split(",")
    avail_color = "#10b981" if avail > 5 else ("#f59e0b" if avail > 0 else "#ef4444")

    if st.button("← Back to Listings"):
        go_home(); st.rerun()

    # Banner
    st.markdown(f"""
    <div class="detail-banner">
      <img src="{get_valid_image(img)}">
      <div class="detail-overlay">
        <div class="detail-overlay-content">
          <div style="font-family:'Poppins',sans-serif;font-size:11px;color:#c084fc;letter-spacing:2px;text-transform:uppercase;font-weight:600;">{htype} Hostel · {tag}</div>
          <div style="font-family:'Nunito',sans-serif;font-size:34px;font-weight:900;color:#fff;margin:5px 0 4px 0;">{name}</div>
          <div style="font-family:'Poppins',sans-serif;font-size:13px;color:rgba(255,255,255,0.8);">📍 {loc} &nbsp;·&nbsp; ⭐ {rating} &nbsp;·&nbsp; {avail} rooms available</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        # About
        st.markdown(f"""
        <div class="info-box">
          <h3>📖 About this Hostel</h3>
          <p style="color:#6b7280;font-family:'Poppins',sans-serif;font-size:14px;line-height:1.85;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

        # Image Gallery
        gallery_imgs = GALLERY_IMAGES.get(htype, GALLERY_IMAGES["Girls"])
        st.markdown('<div class="info-box"><h3>Photo Gallery</h3>', unsafe_allow_html=True)
        gcols = st.columns(3)
        for gi, gimg in enumerate(gallery_imgs):
            with gcols[gi]:
                st.markdown(f"""
                <div class="gallery-img">
                  <img src="{gimg}&auto=format&fit=crop" alt="Gallery {gi+1}" style="width:100%;height:150px;object-fit:cover;border-radius:12px;">
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Facilities
        chips = "".join([f'<span class="fac-chip" style="font-size:12px;padding:5px 13px;">{f.strip()}</span>' for f in fac_list])
        st.markdown(f"""
        <div class="info-box">
          <h3>Facilities</h3>
          <div class="facilities">{chips}</div>
        </div>
        """, unsafe_allow_html=True)

        # Reviews
        reviews = fetch_reviews(hid)
        st.markdown('<div class="info-box"><h3>⭐ Student Reviews</h3>', unsafe_allow_html=True)
        for rv in reviews[-5:]:
            reviewer, r_rating, r_comment = rv
            st.markdown(f"""
            <div class="review-card">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div class="review-author">👤 {reviewer}</div>
                <div class="review-stars">{star_str(r_rating)} <span style="font-size:12px;color:#9ca3af;">{r_rating}/5</span></div>
              </div>
              <div class="review-comment">"{r_comment}"</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Add review
        with st.expander("Add Your Review"):
            r_name = st.text_input("Your Name", key=f"name_{hid}")
            r_rating = st.slider("Your Rating", 1, 5, 4, key=f"rating_{hid}")
            r_comment = st.text_area("Your Review", key=f"comment_{hid}")

            if st.button("Submit Review", key=f"submit_{hid}"):
                if r_comment.strip() and r_name.strip():
                    add_review(hid, r_name.strip(), r_rating, r_comment)
                    st.success("Review submitted!")
                    st.rerun()
                else:
                    st.warning("Enter name and review")

    with col_right:
        # Price box
        st.markdown(f"""
        <div class="info-box">
          <h3>💰 Pricing</h3>
          <div class="price-tag">₹{price:,}</div>
          <div style="font-size:12px;color:#9ca3af;font-family:'Poppins',sans-serif;">per month</div>
          <br>
          <div style="font-size:13px;color:#6b7280;font-family:'Poppins',sans-serif;">
            <span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:{avail_color};margin-right:6px;vertical-align:middle;"></span>
            {avail} room{"s" if avail!=1 else ""} available
          </div>
          <div style="font-size:13px;color:#6b7280;margin-top:6px;">⭐ {rating} · {htype} Hostel</div>
        </div>
        """, unsafe_allow_html=True)

        # Contact
        maps_url = f"https://www.google.com/maps/search/{loc.replace(' ', '+')}"
        st.markdown(f"""
        <div class="info-box">
          <h3>📞 Contact & Location</h3>
          <p style="font-size:15px;color:#7c3aed;font-weight:600;font-family:'Poppins',sans-serif;">{contact}</p>
          <a href="{maps_url}" target="_blank" style="display:inline-block;background:linear-gradient(135deg,#7c3aed,#a855f7);color:#fff;padding:9px 18px;border-radius:11px;font-family:'Poppins',sans-serif;font-weight:600;font-size:13px;text-decoration:none;box-shadow:0 4px 14px rgba(124,58,237,0.3);">📍 Open in Google Maps</a>
        </div>
        """, unsafe_allow_html=True)

        # ── Booking Confirmed UI ──
        if st.session_state.booking_confirmed:
            bc = st.session_state.booking_confirmed
            st.markdown(f"""
            <div class="booking-confirmed">
              <div class="big-emoji">🎉</div>
              <h2>Booking Confirmed!</h2>
              <p>Your room has been successfully reserved at <strong>{bc['hostel']}</strong>.</p>
              <div class="booking-detail-row">
                <span class="booking-detail-label">👤 Name</span>
                <span class="booking-detail-val">{bc['name']}</span>
              </div>
              <div class="booking-detail-row">
                <span class="booking-detail-label">📧 Email</span>
                <span class="booking-detail-val">{bc['email']}</span>
              </div>
              <div class="booking-detail-row">
                <span class="booking-detail-label">🛏️ Rooms</span>
                <span class="booking-detail-val">{bc['rooms']} room{"s" if bc['rooms']!=1 else ""}</span>
              </div>
              <div class="booking-detail-row">
                <span class="booking-detail-label">💰 Total</span>
                <span class="booking-detail-val">₹{bc['total']:,}/month</span>
              </div>
              <div class="booking-detail-row">
                <span class="booking-detail-label">📅 Booked On</span>
                <span class="booking-detail-val">{bc['date']}</span>
              </div>
              <p style="margin-top:14px;font-size:12px;">📩 Confirmation email sent to your inbox!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Booking form
            st.markdown('<div class="info-box"><h3>📅 Book Now</h3>', unsafe_allow_html=True)
            if avail > 0:
                book_name  = st.text_input("Full Name *", placeholder="e.g. Priya Sharma", key="book_name")
                book_email = st.text_input("Email *", placeholder="priya@example.com", key="book_email")
                book_phone = st.text_input("Phone Number *", placeholder="+91 98765 43210", key="book_phone")
                rooms      = st.number_input("Number of Rooms", min_value=1, max_value=avail, value=1, key="book_rooms")
                book_msg   = st.text_area("Message (Optional)", placeholder="Any special requirements?", key="book_msg", height=80)
                total_disp = price * rooms
                st.markdown(f'<p style="font-size:13px;color:#6b7280;">Total: <span style="color:#7c3aed;font-weight:700;font-size:16px;">₹{total_disp:,}/month</span></p>', unsafe_allow_html=True)

                if st.button("✅ Confirm Booking", key="confirm_book", use_container_width=True):
                    if not book_name.strip():
                        st.warning("Please enter your full name.")
                    elif not book_email.strip() or "@" not in book_email:
                        st.warning("Please enter a valid email address.")
                    elif not book_phone.strip():
                        st.warning("Please enter your phone number.")
                    else:
                        success, total = book_hostel(
                            hid, book_name.strip(), book_email.strip(),
                            book_phone.strip(), rooms, book_msg.strip()
                        )
                        if success:
                            simulate_email(book_name.strip(), book_email.strip(), name, rooms, total)
                            st.session_state.booking_confirmed = {
                                "hostel": name, "name": book_name.strip(),
                                "email": book_email.strip(), "rooms": rooms,
                                "total": total, "date": datetime.now().strftime("%d %b %Y, %I:%M %p")
                            }
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("Not enough rooms available. Please reduce the number of rooms.")
            else:
                st.markdown('<p style="color:#ef4444;font-size:14px;">😔 This hostel is fully booked right now. Check back later!</p>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Favourite button
        heart = "❤️ Remove from Favourites" if hid in st.session_state.favorites else "🤍 Add to Favourites"
        if st.button(heart, key="fav_detail", use_container_width=True):
            if hid in st.session_state.favorites:
                st.session_state.favorites.remove(hid)
            else:
                st.session_state.favorites.append(hid)
            st.rerun()

# ─────────────────────────────────────────────
# ADMIN PANEL
# ─────────────────────────────────────────────
def render_admin():
    st.markdown("""
    <div class="admin-header">
      <h2>Admin Panel</h2>
      <p>Manage hostels, view bookings and monitor platform activity</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM hostels")
    total_h = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM bookings")
    total_b = c.fetchone()[0]
    c.execute("SELECT SUM(total_price) FROM bookings")
    total_rev = c.fetchone()[0] or 0
    c.execute("SELECT AVG(rating) FROM hostels")
    avg_rat = round(c.fetchone()[0] or 0, 1)
    conn.close()

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f'<div class="admin-stat-card"><div class="admin-stat-num">{total_h}</div><div class="admin-stat-lbl">Total Hostels</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="admin-stat-card"><div class="admin-stat-num">{total_b}</div><div class="admin-stat-lbl">Total Bookings</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="admin-stat-card"><div class="admin-stat-num">₹{total_rev:,}</div><div class="admin-stat-lbl">Total Revenue</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown(f'<div class="admin-stat-card"><div class="admin-stat-num">{avg_rat}⭐</div><div class="admin-stat-lbl">Avg. Rating</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["➕ Add Hostel", "🏨 All Hostels", "📋 All Bookings"])

    # ── Tab 1: Add hostel ──
    with tab1:
        st.markdown("### Add New Hostel")
        c1, c2 = st.columns(2)
        with c1:
            a_name     = st.text_input("Hostel Name *", placeholder="e.g. Sri Rama Girls Hostel")
            a_location = st.text_input("Location *", placeholder="e.g. Gandi Maisamma, Hyderabad")
            a_price    = st.number_input("Price (₹/month) *", min_value=1000, max_value=20000, value=5000, step=100)
            a_type     = st.selectbox("Hostel Type *", ["Girls", "Boys"])
            a_fac      = st.text_input("Facilities (comma-separated)", placeholder="WiFi,Food,Laundry,Hot Water")
        with c2:
            a_image    = st.text_input("Image URL", placeholder="https://images.unsplash.com/photo-…")
            a_rooms    = st.number_input("Available Rooms", min_value=1, max_value=100, value=10)
            a_contact  = st.text_input("Contact Number", placeholder="+91 98765 43210")
            a_tag      = st.selectbox("Tag", ["Budget Friendly", "Premium"])
        a_desc = st.text_area("Description", placeholder="Describe the hostel facilities, location, and highlights…", height=100)

        if st.button("➕ Add Hostel", use_container_width=True):
            if not a_name.strip() or not a_location.strip():
                st.warning("Hostel name and location are required.")
            else:
                img_url = a_image.strip() or "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=700"
                add_hostel_admin(a_name.strip(), a_location.strip(), a_price, a_type,
                                 a_fac or "WiFi", img_url, a_rooms,
                                 a_contact or "N/A", a_desc or "No description provided.", a_tag)
                st.success(f"✅ '{a_name}' has been successfully added to the platform!")
                st.balloons()

    # ── Tab 2: All hostels ──
    with tab2:
        st.markdown("### All Registered Hostels")
        all_h = fetch_hostels()
        if all_h:
            import pandas as pd
            df = pd.DataFrame(all_h, columns=["ID","Name","Location","Price","Rating",
                                               "Facilities","Image","Rooms","Type","Description","Contact","Tag"])
            df = df[["ID","Name","Location","Type","Price","Rating","Rooms","Tag","Contact"]]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hostels found.")

    # ── Tab 3: Bookings ──
    with tab3:
        st.markdown("### All Bookings")
        bookings = fetch_all_bookings()
        if bookings:
            import pandas as pd
            df = pd.DataFrame(bookings, columns=["ID","Hostel","Name","Email","Phone","Rooms","Total (₹)","Booked At"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No bookings yet.")

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "detail":
    render_detail()
elif st.session_state.page == "admin":
    render_admin()