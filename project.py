import streamlit as st
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
from io import BytesIO  
import base64

# ===================== CONFIG & THEME =====================

st.set_page_config(
    page_title="🧮 Matrix Transformations in Image Processing",
    layout="wide"
)
# ---------- VIDEO BACKGROUND (HTML langsung) ----------
def set_video_background(video_path: str):
    """Set an mp4 video as full-screen background using HTML/CSS."""
    if not os.path.exists(video_path):
        st.warning(f"Video background tidak ditemukan: {video_path}")
        return

    with open(video_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    video_data_url = f"data:video/mp4;base64,{b64}"

    html = """
        <style>
        .video-bg {
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100%;
            min-height: 100%;
            width: auto;
            height: auto;
            z-index: -1;
            object-fit: cover;
        }
        .stApp {
            background: transparent !important;
        }
        </style>
        <video class="video-bg" autoplay muted loop playsinline>
            <source src="{video_data_url}" type="video/mp4">
        </video>
        """.format(video_data_url=video_data_url)
    st.markdown(html, unsafe_allow_html=True)

set_video_background("assets/background.mp4")

# ----- Initialize Session State -----
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "light"
if "language" not in st.session_state:
    st.session_state["language"] = "id"
if "original_img" not in st.session_state:
    st.session_state.original_img = None
if "geo_transform" not in st.session_state:
    st.session_state["geo_transform"] = None
if "image_filter" not in st.session_state:
    st.session_state["image_filter"] = None

# ===================== TRANSLATIONS =====================

translations = {
    "id": {
        "title": "🔢 Operasi Matriks untuk Editing Visual",
        "subtitle": "🎯 Eksplorasi langsung perubahan matriks 2D dan penyesuaian gambar",
        "app_goal": "🎯 **Tujuan aplikasi:** Penjelasan praktis yang menunjukkan fungsi perubahan matriks 2D dan penyaringan gambar pada foto menggunakan ide aljabar linier.",
        "features": "- ↩️ Perubahan: memindah, mengukur, memutar, memiringkan, membalik\n- 🧽 Penyesuaian: menghaluskan, memfokuskan, menemukan garis, menghilangkan latar, mengubah ke hitam putih, menyesuaikan cahaya & bayangan",
        "concept_1_title": "### 🌀 Perubahan Matriks Dua Dimensi",
        "concept_1_text1": "Gambar datar adalah sekumpulan titik \\((x, y)\\) yang bisa diubah lewat tindakan lurus seperti memindah, mengukur, memutar, memiringkan, dan membalik, ditampilkan oleh matriks 2×2 atau 3×3 (titik seragam).",
        "concept_1_text2": "Menggunakan matriks ini pada posisi titik menggesernya: mengukur mengubah skala, memutar berputar di tengah, memiringkan membuat miring, dan membalik membalik pandangan di garis tertentu.",
        "concept_2_title": "### 📊 Penyesuaian Gambar (Pencampuran)",
        "concept_2_text1": "Penyesuaian menggunakan kisi kecil (matriks pencampuran) yang meluncur di gambar; di setiap tempat, ia membuat nilai titik baru dari total kali kisi dengan titik sekitar.",
        "concept_2_text2": "Kisi dengan angka baik seragam membuat pandangan lebih halus atau kabur, sementara kisi dengan tengah baik kuat dan sekitar buruk membuat lebih tajam dan menonjolkan tepi.",
        "concept_3_title": "### 🎲 Mengapa Praktis?",
        "concept_3_text1": "Aplikasi ini praktis karena pengguna bisa menyetel pengaturan (seperti derajat putar, faktor ukur, kekuatan miring, jenis kisi untuk halus atau fokus, dll.) dan langsung lihat perubahan di gambar. ✨",
        "concept_3_text2": "Ini menghubungkan struktur kisi atau matriks dengan hasil visual, membuat gagasan seperti perubahan lurus dan pencampuran lebih gampang dipahami secara alami.",
        "quick_concepts": "#### 📝 Ide Utama",
        "quick_concepts_text": "- ↩️ Perubahan 2D: geser posisi titik (memindah, mengukur, memutar, memiringkan, membalik).\n- 📊 Pencampuran: kisi kecil meluncur di gambar untuk membuat nilai titik baru.",
        "upload_title": "### 📷 Tambah Foto",
        "upload_label": "Tambah foto di sini (PNG/JPG/JPEG) 📂",
        "upload_success": "✅ Foto ditambah dengan baik!",
        "upload_preview": "📷 Tampilan Foto Awal",
        "upload_info": "⬆️ Tolong tambah foto dulu untuk pakai alat di bawah.",
        "tools_title": "### 🔧 Alat Editing Foto",
        "tools_subtitle": "🎛️ Pilih kotak di bawah untuk buka setelan perubahan atau penyesuaian.",
        "geo_title": "#### 🔄 Perubahan Bentuk",
        "geo_desc": "Perubahan bentuk mengubah posisi titik, ukuran, dan arah menggunakan tindakan lurus (matriks).",
        "btn_translation": "↔️ Pindah",
        "btn_scaling": "📏 Ukuran",
        "btn_rotation": "🔄 Putar",
        "btn_shearing": "📐 Miring",
        "btn_reflection": "🪞 Cermin",
        "geo_info": "🔔 Tolong tambah foto dulu untuk coba perubahan.",
        "trans_settings": "**↔️ Setelan Pindah**",
        "trans_dx": "dx (geser samping)",
        "trans_dy": "dy (geser atas-bawah)",
        "btn_apply": "Pakai",
        "trans_result": "Hasil Pindah",
        "scale_settings": "**📏 Setelan Ukuran**",
        "scale_x": "Ukuran X",
        "scale_y": "Ukuran Y",
        "scale_result": "Hasil Ukuran",
        "rot_settings": "**🔄 Setelan Putar**",
        "rot_angle": "Sudut putar (derajat)",
        "rot_result": "Hasil Putar",
        "shear_settings": "**📐 Setelan Miring**",
        "shear_x": "Faktor miring X",
        "shear_y": "Faktor miring Y",
        "shear_result": "Hasil Miring",
        "refl_settings": "**🪞 Setelan Cermin**",
        "refl_axis": "Garis cermin",
        "refl_result": "Hasil Cermin",
        "hist_title": "#### 📈 Bagan Foto",
        "hist_desc": "Bagan menampilkan sebaran kekuatan titik (redup–terang), berguna untuk periksa cahaya dan bayangan.",
        "btn_histogram": "Tampilkan Bagan 📈",
        "hist_warning": "Tolong tambah foto dulu untuk tampilkan bagan.",
        "filter_title": "#### 🔧 Penyesuaian Foto",
        "filter_desc": "Penyesuaian mengubah nilai titik berdasarkan tetangga (pencampuran) untuk lakukan halus, fokus, temukan garis, hilangkan latar, dan lain.",
        "btn_blur": "🔲 Halus",
        "btn_sharpen": "✨ Fokus",
        "btn_background": "🎯 Latar",
        "btn_grayscale": "⚫ Hitam Putih",
        "btn_edge": "🔍 Garis",
        "btn_brightness": "☀️ Cahaya",
        "filter_info": "🔔 Tolong tambah foto dulu untuk pakai penyesuaian.",
        "blur_settings": "**🔲 Setelan Penyesuaian Halus**",
        "blur_kernel": "Ukuran kisi",
        "blur_result": "Hasil Halus",
        "sharpen_settings": "**✨ Setelan Penyesuaian Fokus**",
        "sharpen_desc": "Tingkatkan rincian dan garis di foto.",
        "sharpen_result": "Hasil Fokus",
        "bg_settings": "**🎯 Setelan Hilangkan Latar**",
        "bg_method": "Cara (demo pakai HSV saja sekarang)",
        "bg_result": "Hasil Hilangkan Latar",
        "gray_settings": "**⚫ Setelan Ubah Hitam Putih**",
        "gray_desc": "Ubah foto ke hitam putih (abu-abu).",
        "gray_result": "Hasil Hitam Putih",
        "edge_settings": "**🔍 Setelan Temukan Garis**",
        "edge_method": "Cara garis",
        "edge_result": "Foto Garis",
        "bright_settings": "**☀️ Setelan Cahaya & Bayangan**",
        "bright_brightness": "Cahaya",
        "bright_contrast": "Bayangan",
        "bright_result": "Hasil Cahaya/Bayangan",
        "team_title": "### 👥 Orang Kelompok",
        "team_subtitle": "Kelompok 5 – Orang dan Tugas",
        "team_sid": "**ID:**",
        "team_role": "**Tugas:**",
        "team_contribution": "Bantuan:",
        "team_group": "**Kelompok:**",
        "axis_x": "Garis-X",
        "axis_y": "Garis-Y",
        "axis_diag": "Silang",
        "dark_mode": "Gaya Malam",
        "light_mode": "Gaya Siang",
    },
    "en": {
        "title": "🔢 Matrix Operations for Visual Editing",
        "subtitle": "🎯 Live exploration of 2D matrix changes and picture adjustments",
        "app_goal": "🎯 **Goal:** A hands-on exploration showing how 2D matrix changes and picture adjustments affect visuals through linear algebra ideas.",
        "features": "- ↩️ Changes: moving, sizing, turning, slanting, flipping\n- 🧽 Adjustments: smoothing, focusing, outline spotting, backdrop clearing, turning to monochrome, tweaking light & shade",
        "concept_1_title": "### 🌀 2D Matrix Changes",
        "concept_1_text1": "A flat image is a group of spots \\((x, y)\\) that get moved by straight-line actions like moving, sizing, turning, slanting, and flipping, shown by 2×2 or 3×3 matrices (uniform spots).",
        "concept_1_text2": "Using these matrices on spot places shifts them: sizing changes the scale, turning spins the view around its middle, slanting makes it lean, and flipping reverses the view on a chosen line.",
        "concept_2_title": "### 📊 Picture Adjustments (Mixing)",
        "concept_2_text1": "Adjusting uses a tiny grid (mixing matrix) that glides over the image; at each spot, it makes a fresh spot value by adding up the grid times nearby spots.",
        "concept_2_text2": "Grids with even good numbers make the view softer or fuzzy, while grids with a big good middle and bad sides make it sharper and highlight edges.",
        "concept_3_title": "### 🎲 Why Hands-On?",
        "concept_3_text1": "The app is hands-on since users can tweak settings (such as turn degrees, size rates, slant strengths, grid kinds for smooth or focus, etc.) and right away see the changes on the view. ✨",
        "concept_3_text2": "It links the grid or matrix setup to seen effects, making thoughts like straight changes and mixing simpler to grasp naturally.",
        "quick_concepts": "#### 📝 Key Ideas",
        "quick_concepts_text": "- ↩️ 2D Changes: shift spot places (moving, sizing, turning, slanting, flipping).\n- 📊 Mixing: a tiny grid gliding over the image to make fresh spot values.",
        "upload_title": "### 📷 Add Picture",
        "upload_label": "Add a picture here (PNG/JPG/JPEG) 📂",
        "upload_success": "✅ Picture added well!",
        "upload_preview": "📷 Starting Picture View",
        "upload_info": "⬆️ Kindly add a picture first to use the tools below.",
        "tools_title": "### 🔧 Picture Editing Tools",
        "tools_subtitle": "🎛️ Pick a box below to open change or adjust settings.",
        "geo_title": "#### 🔄 Shape Changes",
        "geo_desc": "Shape changes alter the spot position, size, and direction using straight actions (matrices).",
        "btn_translation": "↔️ Move",
        "btn_scaling": "📏 Size",
        "btn_rotation": "🔄 Turn",
        "btn_shearing": "📐 Slant",
        "btn_reflection": "🪞 Mirror",
        "geo_info": "🔔 Kindly add a picture first to try changes.",
        "trans_settings": "**↔️ Move Settings**",
        "trans_dx": "dx (side move)",
        "trans_dy": "dy (up-down move)",
        "btn_apply": "Use",
        "trans_result": "Move Outcome",
        "scale_settings": "**📏 Size Settings**",
        "scale_x": "Size X",
        "scale_y": "Size Y",
        "scale_result": "Size Outcome",
        "rot_settings": "**🔄 Turn Settings**",
        "rot_angle": "Turn angle (degrees)",
        "rot_result": "Turn Outcome",
        "shear_settings": "**📐 Slant Settings**",
        "shear_x": "Slant factor X",
        "shear_y": "Slant factor Y",
        "shear_result": "Slant Outcome",
        "refl_settings": "**🪞 Mirror Settings**",
        "refl_axis": "Mirror line",
        "refl_result": "Mirror Outcome",
        "hist_title": "#### 📈 Picture Chart",
        "hist_desc": "The chart displays the spread of spot strengths (dim–bright), handy for checking light and shade.",
        "btn_histogram": "Show Chart 📈",
        "hist_warning": "Kindly add a picture first to show the chart.",
        "filter_title": "#### 🔧 Picture Adjustments",
        "filter_desc": "Adjustments change spot values based on neighbors (mixing) to do smooth, focus, outline finding, backdrop removal, and more.",
        "btn_blur": "🔲 Smooth",
        "btn_sharpen": "✨ Focus",
        "btn_background": "🎯 Backdrop",
        "btn_grayscale": "⚫ Monochrome",
        "btn_edge": "🔍 Outline",
        "btn_brightness": "☀️ Light",
        "filter_info": "🔔 Kindly add a picture first to use adjustments.",
        "blur_settings": "**🔲 Smooth Adjustment Settings**",
        "blur_kernel": "Grid size",
        "blur_result": "Smooth Outcome",
        "sharpen_settings": "**✨ Focus Adjustment Settings**",
        "sharpen_desc": "Boost details and outlines in the picture.",
        "sharpen_result": "Focus Outcome",
        "bg_settings": "**🎯 Backdrop Removal Settings**",
        "bg_method": "Way (demo uses HSV only now)",
        "bg_result": "Backdrop Removal Outcome",
        "gray_settings": "**⚫ Monochrome Change Settings**",
        "gray_desc": "Change the picture to monochrome (black and white).",
        "gray_result": "Monochrome Outcome",
        "edge_settings": "**🔍 Outline Finding Settings**",
        "edge_method": "Outline way",
        "edge_result": "Outline Picture",
        "bright_settings": "**☀️ Light & Shade Settings**",
        "bright_brightness": "Light",
        "bright_contrast": "Shade",
        "bright_result": "Light/Shade Outcome",
        "team_title": "### 👥 Group People",
        "team_subtitle": "Group 5 – People and Jobs",
        "team_sid": "**ID:**",
        "team_role": "**Job:**",
        "team_group": "**Group:**",
        "team_contribution": "Help:",
        "axis_x": "X-line",
        "axis_y": "Y-line",
        "axis_diag": "Cross",
        "dark_mode": "Night Style",
        "light_mode": "Day Style",
    }
}

# ===================== HEADER WITH TOGGLES =====================

# Get current language and theme
lang = st.session_state["language"]
t = translations[lang]
theme_mode = st.session_state["theme_mode"]

with st.container(border=True):
    # Title dan controls dalam 3 kolom sejajar
    header_col1, header_col2, header_col3 = st.columns([6, 1, 1], vertical_alignment="center")

    with header_col1:
        st.title(t["title"])

    with header_col2:
        # Language toggle - shows opposite language
        lang_button_text = "🇬🇧 EN" if lang == "id" else "🇮🇩 ID"
        if st.button(lang_button_text, key="lang_toggle", use_container_width=True):
            st.session_state["language"] = "en" if lang == "id" else "id"
            st.rerun()

    with header_col3:
        # Theme toggle - shows opposite mode icon
        theme_button_text = "🌙 Dark" if theme_mode == "light" else "☀️ Light"
        if st.button(theme_button_text, key="theme_toggle", use_container_width=True):
            st.session_state["theme_mode"] = "dark" if theme_mode == "light" else "light"
            st.rerun()

st.subheader(t["subtitle"])

# ----- Global layout + theme CSS -----

base_css = """
<style>
.block-container {
    max-width: 1200px;
    padding: 2.5rem 2rem 1.2rem 2rem;
}
section[data-testid="stExpander"]{
    border-radius:10px;
    padding:8px;
    box-shadow:0 1px 6px rgba(0,0,0,0.04);
    margin-bottom:10px;
    background-color: var(--stLightBlue-50);
}
section[data-testid="stExpander"] .streamlit-expanderHeader{
    font-size:16px;
}
.stImage > img{
    max-height:420px;
    object-fit:contain;
}
div[data-testid="column"] button {
    padding-top: 8px !important;
    padding-bottom: 8px !important;
    padding-left: 12px !important;
    padding-right: 12px !important;
    font-size: 14px !important;
    width: 100%;
    font-weight: 500 !important;
}
/* Green border for containers */
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 2px solid #4CAF50 !important;
    border-radius: 12px !important;
}
/* Team member photo container - square with crop */
.team-photo-container {
    width: 140px;
    height: 140px;
    border-radius: 12px;
    overflow: hidden;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f0f0f0;
    border: 3px solid #4CAF50;
}
.team-photo-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}
</style>
"""

light_css = """
<style>
.stMarkdown, .stMarkdown p, .stMarkdown li {
    color: #1b5e20 !important;
}
button[kind="secondary"] {
    background-color: #ffffff !important;
    color: #1b5e20 !important;
    border: 2px solid #4CAF50 !important;
    font-weight: 600 !important;
}
button[kind="secondary"]:hover {
    background-color: #e8f5e9 !important;
    border-color: #2e7d32 !important;
}
.team-photo-container {
    background: #e8f5e9;
    border-color: #4CAF50;
}
</style>
"""

dark_css = """
<style>
.stMarkdown, .stMarkdown p, .stMarkdown li {
    color: #c8e6c9 !important;
}
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: rgba(27, 58, 27, 0.3) !important;
}
button[kind="secondary"] {
    background-color: #1e3a1e !important;
    color: #c8e6c9 !important;
    border: 2px solid #66bb6a !important;
    font-weight: 600 !important;
}
button[kind="secondary"]:hover {
    background-color: #2d5a2d !important;
    border-color: #81c784 !important;
}
.team-photo-container {
    background: #1e3a1e;
    border-color: #66bb6a;
}
</style>
"""
st.markdown(base_css, unsafe_allow_html=True)
if theme_mode == "light":
    st.markdown(light_css, unsafe_allow_html=True)
else:
    st.markdown(dark_css, unsafe_allow_html=True)

# ===================== APP GOAL =====================

with st.container(border=True):
    st.markdown(t["app_goal"])
    st.markdown(t["features"])

# ===================== THREE CONCEPT BOXES =====================

col1, col2, col3 = st.columns(3, vertical_alignment="top")

with col1:
    with st.container(border=True):
        st.markdown(t["concept_1_title"])
        st.markdown(t["concept_1_text1"])
        st.markdown(t["concept_1_text2"])

with col2:
    with st.container(border=True):
        st.markdown(t["concept_2_title"])
        st.markdown(t["concept_2_text1"])
        st.markdown(t["concept_2_text2"])

with col3:
    with st.container(border=True):
        st.markdown(t["concept_3_title"])
        st.markdown(t["concept_3_text1"])
        st.markdown(t["concept_3_text2"])

# ===================== HELPER FUNCTIONS =====================

def load_image(file):
    img = Image.open(file).convert("RGB")
    img_np = np.array(img)
    return img_np

def to_opencv(img_rgb):
    return cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

def to_streamlit(img_bgr):
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

def apply_affine_transform(img_rgb, M, output_size=None):
    img_bgr = to_opencv(img_rgb)
    h, w = img_bgr.shape[:2]
    if output_size is None:
        output_size = (w, h)

    if M.shape == (3, 3):
        M_affine = M[0:2, :]
    else:
        M_affine = M

    transformed = cv2.warpAffine(
        img_bgr, M_affine, output_size,
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT
    )
    return to_streamlit(transformed)

def manual_convolution_gray(img_gray, kernel):
    k_h, k_w = kernel.shape
    pad_h = k_h // 2
    pad_w = k_w // 2
    padded = np.pad(img_gray, ((pad_h, pad_h), (pad_w, pad_w)), mode="reflect")
    h, w = img_gray.shape
    output = np.zeros_like(img_gray, dtype=np.float32)
    for i in range(h):
        for j in range(w):
            region = padded[i:i + k_h, j:j + k_w]
            output[i, j] = np.sum(region * kernel)
    output = np.clip(output, 0, 255).astype(np.uint8)
    return output

def rgb_to_gray(img_rgb):
    img_bgr = to_opencv(img_rgb)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    return gray

def adjust_brightness_contrast(img_rgb, brightness=0, contrast=0):
    img_bgr = to_opencv(img_rgb)
    beta = brightness
    alpha = 1 + (contrast / 100.0)
    adjusted = cv2.convertScaleAbs(img_bgr, alpha=alpha, beta=beta)
    return to_streamlit(adjusted)

def image_to_bytes(img_rgb, fmt="PNG"):
    """
    Convert numpy image (RGB, RGBA, or grayscale) to bytes for download.

    - PNG: simpan apa adanya (termasuk alpha/transparan).
    - JPEG: otomatis buang alpha (RGBA -> RGB) agar tidak error.
    """
    if img_rgb is None:
        raise ValueError("image_to_bytes received None image")

    arr = np.array(img_rgb)

    # Grayscale -> RGB
    if arr.ndim == 2:
        arr = cv2.cvtColor(arr, cv2.COLOR_GRAY2RGB)

    # JPEG tidak mendukung alpha channel
    if fmt.upper() == "JPEG" and arr.ndim == 3 and arr.shape[2] == 4:
        arr = arr[:, :, :3]

    pil_img = Image.fromarray(arr.astype("uint8"))
    buf = BytesIO()
    pil_img.save(buf, format=fmt)
    return buf.getvalue()

# ===================== ADVANCED BACKGROUND HELPERS =====================

def _feather_mask(mask: np.ndarray, radius: int) -> np.ndarray:
    """Feather/smooth mask edges using Gaussian blur."""
    if radius <= 0:
        m = mask.astype(np.float32)
        if m.max() > 1.0:
            m = m / 255.0
        return m

    m = mask.astype(np.float32)
    if m.max() > 1.0:
        m = m / 255.0

    ksize = radius * 2 + 1
    m_blur = cv2.GaussianBlur(m, (ksize, ksize), 0)
    return np.clip(m_blur, 0.0, 1.0)


def _refine_hair_region(image_rgb: np.ndarray,
                        mask: np.ndarray,
                        refine_hair: bool = True) -> np.ndarray:
    """Refine mask around hair and fine details using edge cues."""
    m = mask.copy().astype(np.uint8)
    if m.max() > 1:
        m = (m > 127).astype(np.uint8)

    if not refine_hair:
        return m

    img_bgr = to_opencv(image_rgb)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_dilated = cv2.dilate(edges, np.ones((3, 3), np.uint8))

    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))

    m[edge_dilated > 0] = 1
    return m.astype(np.uint8)


def _remove_small_holes(mask: np.ndarray,
                        min_area: int = 100) -> np.ndarray:
    """Remove small holes inside the foreground mask."""
    m = mask.copy().astype(np.uint8)
    if m.max() > 1:
        m = (m > 127).astype(np.uint8)

    inv = (1 - m).astype(np.uint8)
    contours, _ = cv2.findContours(inv, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) < min_area:
            cv2.drawContours(inv, [cnt], -1, 0, thickness=cv2.FILLED)

    cleaned = 1 - inv
    return cleaned.astype(np.uint8)


def _apply_solid_background(image_rgb: np.ndarray,
                            mask_float: np.ndarray,
                            color: tuple[int, int, int]) -> np.ndarray:
    """Replace background with solid RGB color."""
    h, w = image_rgb.shape[:2]
    bg = np.full((h, w, 3), color, dtype=np.uint8)

    alpha = mask_float[:, :, None]
    out = (alpha * image_rgb.astype(np.float32) +
           (1.0 - alpha) * bg.astype(np.float32))
    return out.astype(np.uint8)


def _apply_blur_background(image_rgb: np.ndarray,
                           mask_float: np.ndarray,
                           ksize: int = 21) -> np.ndarray:
    """Blur only the background while keeping subject sharp."""
    if ksize % 2 == 0:
        ksize += 1
    blurred = cv2.GaussianBlur(image_rgb, (ksize, ksize), 0)

    alpha = mask_float[:, :, None]
    out = (alpha * image_rgb.astype(np.float32) +
           (1.0 - alpha) * blurred.astype(np.float32))
    return out.astype(np.uint8)


def segment_foreground(image: np.ndarray) -> np.ndarray:
    """
    SIMPLE foreground segmentation.

    Untuk sementara: subject dianggap di tengah gambar (ellipse).
    Nanti bisa kamu ganti dengan model segmentasi beneran.
    """
    h, w = image.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)

    center = (w // 2, h // 2)
    axes = (int(w * 0.35), int(h * 0.45))
    cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)

    return mask


# ===================== ADVANCED BACKGROUND MAIN FUNCTION =====================

def remove_background_advanced(
    image: np.ndarray,
    mode: str = "auto",
    target_background_type: str | None = None,
    output_mode: str = "transparent",
    solid_color: tuple[int, int, int] | None = None,
    feather_radius: int = 3,
    refine_hair: bool = True,
) -> np.ndarray:
    """
    Advanced background removal supporting multiple background types and outputs.
    """
    if image is None:
        raise ValueError("Input image is None")

    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("`image` must be RGB with shape (H, W, 3)")

    h, w = image.shape[:2]
    img_bgr = to_opencv(image)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    L_channel = img_lab[:, :, 0]

    bg_type = (target_background_type or mode or "auto").lower()

    # ---------- RAW MASK PER MODE ----------
    if bg_type in ["solid", "studio"]:
        border_thick = max(5, min(h, w) // 20)
        border_pixels = np.concatenate([
            img_hsv[:border_thick, :, :].reshape(-1, 3),
            img_hsv[-border_thick:, :, :].reshape(-1, 3),
            img_hsv[:, :border_thick, :].reshape(-1, 3),
            img_hsv[:, -border_thick:, :].reshape(-1, 3),
        ], axis=0)
        bg_color = np.median(border_pixels, axis=0).astype(np.float32)

        hsv_flat = img_hsv.reshape(-1, 3).astype(np.float32)
        dist = np.linalg.norm(hsv_flat - bg_color[None, :], axis=1)
        dist_img = dist.reshape(h, w)
        thresh = np.percentile(dist_img, 60)
        raw_mask = (dist_img > thresh).astype(np.uint8)

    elif bg_type == "gradient":
        L_norm = cv2.normalize(L_channel, None, 0, 255, cv2.NORM_MINMAX)
        edges = cv2.Canny(L_norm, 50, 150)
        thr = cv2.adaptiveThreshold(
            L_norm, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 21, 5
        )
        raw_mask = ((thr == 255) | (edges > 0)).astype(np.uint8)

    elif bg_type == "textured":
        prior_mask = segment_foreground(image)
        if prior_mask.max() > 1:
            prior_mask = (prior_mask > 127).astype(np.uint8)

        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 160)
        prior_dilated = cv2.dilate(prior_mask, np.ones((7, 7), np.uint8))
        edge_near_prior = cv2.dilate(edges, np.ones((5, 5), np.uint8))
        raw_mask = ((prior_dilated == 1) | (edge_near_prior > 0)).astype(np.uint8)

    elif bg_type == "natural":
        prior_mask = segment_foreground(image)
        if prior_mask.max() > 1:
            prior_mask = (prior_mask > 127).astype(np.uint8)

        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 200)

        border_thick = max(5, min(h, w) // 20)
        border_pixels = img_lab[:border_thick, :, :].reshape(-1, 3)
        bg_L = np.median(border_pixels[:, 0])

        L_diff = np.abs(L_channel.astype(np.float32) - bg_L)
        contrast_mask = (L_diff > 15).astype(np.uint8)

        raw_mask = ((prior_mask == 1) | (edges > 0)) & contrast_mask

    elif bg_type == "minimalist":
        border_thick = max(5, min(h, w) // 20)
        border_pixels = img_hsv[:border_thick, :, :].reshape(-1, 3)
        bg_color = np.median(border_pixels, axis=0).astype(np.float32)

        hsv_flat = img_hsv.reshape(-1, 3).astype(np.float32)
        dist = np.linalg.norm(hsv_flat - bg_color[None, :], axis=1)
        dist_img = dist.reshape(h, w)
        thresh = np.percentile(dist_img, 70)
        raw_mask = (dist_img > thresh).astype(np.uint8)

    elif bg_type == "abstract":
        prior_mask = segment_foreground(image)
        if prior_mask.max() > 1:
            prior_mask = (prior_mask > 127).astype(np.uint8)

        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        raw = ((prior_mask == 1) | (edges > 0)).astype(np.uint8)
        raw = cv2.morphologyEx(raw, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
        raw_mask = raw

    elif bg_type == "vintage":
        L_blur = cv2.GaussianBlur(L_channel, (5, 5), 0)
        _, thr = cv2.threshold(L_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        raw = thr == 255
        raw = cv2.morphologyEx(raw.astype(np.uint8), cv2.MORPH_OPEN,
                               np.ones((3, 3), np.uint8))
        raw_mask = raw

    else:
        # AUTO: analisa rata/tidaknya brightness di border
        border_thick = max(5, min(h, w) // 20)
        border_pixels = img_lab[:border_thick, :, :].reshape(-1, 3)
        L_border = border_pixels[:, 0]
        std_L = np.std(L_border)

        if std_L < 5:
            return remove_background_advanced(
                image=image,
                mode="solid",
                target_background_type="solid",
                output_mode=output_mode,
                solid_color=solid_color,
                feather_radius=feather_radius,
                refine_hair=refine_hair,
            )
        elif std_L < 15:
            return remove_background_advanced(
                image=image,
                mode="gradient",
                target_background_type="gradient",
                output_mode=output_mode,
                solid_color=solid_color,
                feather_radius=feather_radius,
                refine_hair=refine_hair,
            )
        else:
            return remove_background_advanced(
                image=image,
                mode="textured",
                target_background_type="textured",
                output_mode=output_mode,
                solid_color=solid_color,
                feather_radius=feather_radius,
                refine_hair=refine_hair,
            )

    # ---------- POST-PROCESSING MASK ----------
    mask_clean = _remove_small_holes(raw_mask, min_area=100)
    mask_refined_bin = _refine_hair_region(image, mask_clean, refine_hair=refine_hair)
    mask_float = _feather_mask(mask_refined_bin, radius=feather_radius)

    # ---------- OUTPUT ----------
    if output_mode == "custom_mask":
        return (mask_float * 255.0).astype(np.uint8)

    if output_mode == "transparent":
        alpha = (mask_float * 255.0).astype(np.uint8)
        rgba = np.dstack([image.astype(np.uint8), alpha])
        return rgba

    if output_mode == "solid_color":
        if solid_color is None:
            solid_color = (255, 255, 255)
        rgb_out = _apply_solid_background(image.astype(np.uint8),
                                          mask_float, solid_color)
        return rgb_out

    if output_mode == "blurred":
        rgb_out = _apply_blur_background(image.astype(np.uint8),
                                         mask_float, ksize=25)
        return rgb_out

    raise ValueError(f"Unsupported output_mode: {output_mode}")

def compute_histogram(img_rgb):
    img_bgr = to_opencv(img_rgb)
    color = ('b', 'g', 'r')
    fig, ax = plt.subplots(figsize=(8, 4))
    for i, col in enumerate(color):
        hist = cv2.calcHist([img_bgr], [i], None, [256], [0, 256])
        ax.plot(hist, color=col)
        ax.set_xlim([0, 256])
    ax.set_title("Color Histogram")
    ax.set_xlabel("Pixel value")
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    return fig

def simple_background_removal_hsv(img_rgb):
    img_bgr = to_opencv(img_rgb)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 0])
    upper = np.array([180, 255, 200])
    mask_bg = cv2.inRange(hsv, lower, upper)
    mask_fg = cv2.bitwise_not(mask_bg)
    fg = cv2.bitwise_and(img_bgr, img_bgr, mask=mask_fg)
    fg_rgb = to_streamlit(fg)
    return fg_rgb

def image_to_bytes(img_rgb, fmt="PNG"):
    """
    Convert numpy RGB or RGBA image to bytes for download.
    - PNG: akan simpan apa adanya (termasuk alpha/transparan).
    - JPEG: otomatis buang alpha (RGBA -> RGB) agar tidak error.
    """
    if img_rgb is None:
        raise ValueError("image_to_bytes received None image")

    arr = np.array(img_rgb)
    # kalau grayscale, naikkan ke RGB
    if arr.ndim == 2:
        arr = cv2.cvtColor(arr, cv2.COLOR_GRAY2RGB)

    # kalau JPEG, buang alpha dulu kalau ada
    if fmt.upper() == "JPEG" and arr.ndim == 3 and arr.shape[2] == 4:
        arr = arr[:, :, :3]

    pil_img = Image.fromarray(arr.astype("uint8"))
    buf = BytesIO()
    pil_img.save(buf, format=fmt)
    return buf.getvalue()

def create_square_image_html(image_path, size=140):
    """Create HTML for square cropped image"""
    return f"""
    <div class="team-photo-container">
        <img src="data:image/jpeg;base64,{{base64_img}}" alt="Team member"/>
    </div>
    """

def safe_display_square_image(path):
    """Display image in square format with proper cropping"""
    if os.path.exists(path):
        try:
            img = Image.open(path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) // 2
            top = (height - min_dim) // 2
            right = left + min_dim
            bottom = top + min_dim
            img_cropped = img.crop((left, top, right, bottom))
            img_resized = img_cropped.resize((140, 140), Image.Resampling.LANCZOS)

            import base64
            buffered = BytesIO()
            img_resized.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            st.markdown(f"""
            <div class="team-photo-container">
                <img src="data:image/jpeg;base64,{img_str}" alt="Team member"/>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")
    else:
        st.markdown("""
        <div class="team-photo-container">
            <div style="width:100%; height:100%; display:flex; align-items:center; justify-content:center; background:#ddd; color:#666;">
                No Image
            </div>
        </div>
        """, unsafe_allow_html=True)

# Ensure images folder and placeholders exist
images_dir = "images"
os.makedirs(images_dir, exist_ok=True)
placeholder_files = [
    os.path.join(images_dir, "gitsi.jpg"),
    os.path.join(images_dir, "bella.jpg"),
    os.path.join(images_dir, "chinta.jpg"),
    os.path.join(images_dir, "yessa.jpg"),
]
for p in placeholder_files:
    if not os.path.exists(p):
        placeholder = Image.new("RGB", (400, 400), color=(200, 200, 200))
        placeholder.save(p, format="JPEG")

# ===================== CONCEPTS SHORT REMINDER =====================

with st.container(border=True):
    st.markdown(t["quick_concepts"])
    st.markdown(t["quick_concepts_text"])

# ===================== UPLOAD IMAGE =====================

with st.container(border=True):
    st.markdown(t["upload_title"])
    uploaded_file = st.file_uploader(
        label=t["upload_label"],
        type=["png", "jpg", "jpeg"],
        key="image_uploader"
    )

    if uploaded_file is not None:
        original_img = load_image(uploaded_file)
        st.session_state.original_img = original_img
        st.success(t["upload_success"])
        st.image(
            original_img,
            caption=t["upload_preview"],
            use_column_width=True
        )
    else:
        st.info(t["upload_info"])

original_img = st.session_state.original_img

# ===================== TOOLS TITLE =====================

st.markdown(t["tools_title"])
st.write(t["tools_subtitle"])

tools_col_left, tools_col_right = st.columns(2, vertical_alignment="top")

# ==================== LEFT: GEOMETRIC TRANSFORMATIONS ====================
with tools_col_left:
    with st.container(border=True):
        st.markdown(t["geo_title"])
        st.write(t["geo_desc"])
        st.markdown("---")

        trans_col1, trans_col2, trans_col3 = st.columns(3)
        with trans_col1:
            if st.button(t["btn_translation"], key="btn_trans_click", type="secondary"):
                st.session_state["geo_transform"] = "translation"
        with trans_col2:
            if st.button(t["btn_scaling"], key="btn_scale_click", type="secondary"):
                st.session_state["geo_transform"] = "scaling"
        with trans_col3:
            if st.button(t["btn_rotation"], key="btn_rot_click", type="secondary"):
                st.session_state["geo_transform"] = "rotation"

        trans_col4, trans_col5, _ = st.columns(3)
        with trans_col4:
            if st.button(t["btn_shearing"], key="btn_shear_click", type="secondary"):
                st.session_state["geo_transform"] = "shearing"
        with trans_col5:
            if st.button(t["btn_reflection"], key="btn_refl_click", type="secondary"):
                st.session_state["geo_transform"] = "reflection"

        # Transform parameter panel
        if original_img is None:
            st.info(t["geo_info"])
        else:
            if st.session_state["geo_transform"] == "translation":
                st.markdown(t["trans_settings"])
                dx = st.slider(t["trans_dx"], -200, 200, 0, key="trans_dx")
                dy = st.slider(t["trans_dy"], -200, 200, 0, key="trans_dy")
                if st.button(f"{t['btn_apply']} ✅", key="btn_apply_trans", type="primary"):
                    T = np.array([[1, 0, dx],
                                  [0, 1, dy],
                                  [0, 0, 1]], dtype=np.float32)
                    translated_img = apply_affine_transform(original_img, T)
                    st.image(translated_img, caption=t["trans_result"], use_column_width=True)

                    col_png, col_jpg = st.columns(2)
                    with col_png:
                        st.download_button(
                            label="⬇️ Download PNG",
                            data=image_to_bytes(translated_img, fmt="PNG"),
                            file_name="translation_result.png",
                            mime="image/png",
                            key="dl_trans_png"
                        )
                    with col_jpg:
                        st.download_button(
                            label="⬇️ Download JPG",
                            data=image_to_bytes(translated_img, fmt="JPEG"),
                            file_name="translation_result.jpg",
                            mime="image/jpeg",
                            key="dl_trans_jpg"
                        )

            elif st.session_state["geo_transform"] == "scaling":
                st.markdown(t["scale_settings"])
                sx = st.slider(t["scale_x"], 0.1, 3.0, 1.0, key="scale_x")
                sy = st.slider(t["scale_y"], 0.1, 3.0, 1.0, key="scale_y")
                if st.button(f"{t['btn_apply']} ✅", key="btn_apply_scale", type="primary"):
                    h, w = original_img.shape[:2]
                    S = np.array([[sx, 0, 0],
                                  [0, sy, 0],
                                  [0, 0, 1]], dtype=np.float32)
                    new_w = int(w * sx)
                    new_h = int(h * sy)
                    scaled_img = apply_affine_transform(original_img, S, output_size=(new_w, new_h))
                    st.image(scaled_img, caption=t["scale_result"], use_column_width=True)

                    col_png, col_jpg = st.columns(2)
                    with col_png:
                        st.download_button(
                            label="⬇️ Download PNG",
                            data=image_to_bytes(scaled_img, fmt="PNG"),
                            file_name="scaling_result.png",
                            mime="image/png",
                            key="dl_scale_png"
                        )
                    with col_jpg:
                        st.download_button(
                            label="⬇️ Download JPG",
                            data=image_to_bytes(scaled_img, fmt="JPEG"),
                            file_name="scaling_result.jpg",
                            mime="image/jpeg",
                            key="dl_scale_jpg"
                        )

            elif st.session_state["geo_transform"] == "rotation":
                st.markdown(t["rot_settings"])
                angle = st.slider(t["rot_angle"], -180, 180, 0, key="rot_angle")
                if st.button(f"{t['btn_apply']} ✅", key="btn_apply_rot", type="primary"):
                    h, w = original_img.shape[:2]
                    cx, cy = w / 2, h / 2
                    theta = np.deg2rad(angle)
                    cos_t = np.cos(theta)
                    sin_t = np.sin(theta)
                    R = np.array([[cos_t, -sin_t, 0],
                                  [sin_t,  cos_t, 0],
                                  [0,      0,     1]], dtype=np.float32)
                    T1 = np.array([[1, 0, -cx],
                                   [0, 1, -cy],
                                   [0, 0, 1]], dtype=np.float32)
                    T2 = np.array([[1, 0, cx],
                                   [0, 1, cy],
                                   [0, 0, 1]], dtype=np.float32)
                    M = T2 @ R @ T1
                    rotated_img = apply_affine_transform(original_img, M)
                    st.image(rotated_img, caption=t["rot_result"], use_column_width=True)

                    col_png, col_jpg = st.columns(2)
                    with col_png:
                        st.download_button(
                            label="⬇️ Download PNG",
                            data=image_to_bytes(rotated_img, fmt="PNG"),
                            file_name="rotation_result.png",
                            mime="image/png",
                            key="dl_rot_png"
                        )
                    with col_jpg:
                        st.download_button(
                            label="⬇️ Download JPG",
                            data=image_to_bytes(rotated_img, fmt="JPEG"),
                            file_name="rotation_result.jpg",
                            mime="image/jpeg",
                            key="dl_rot_jpg"
                        )

            elif st.session_state["geo_transform"] == "shearing":
                st.markdown(t["shear_settings"])
                shear_x = st.slider(t["shear_x"], -1.0, 1.0, 0.0, key="shear_x")
                shear_y = st.slider(t["shear_y"], -1.0, 1.0, 0.0, key="shear_y")
                if st.button(f"{t['btn_apply']} ✅", key="btn_apply_shear", type="primary"):
                    Sh = np.array([[1,      shear_x, 0],
                                   [shear_y, 1,      0],
                                   [0,       0,      1]], dtype=np.float32)
                    sheared_img = apply_affine_transform(original_img, Sh)
                    st.image(sheared_img, caption=t["shear_result"], use_column_width=True)

                    col_png, col_jpg = st.columns(2)
                    with col_png:
                        st.download_button(
                            label="⬇️ Download PNG",
                            data=image_to_bytes(sheared_img, fmt="PNG"),
                            file_name="shearing_result.png",
                            mime="image/png",
                            key="dl_shear_png"
                        )
                    with col_jpg:
                        st.download_button(
                            label="⬇️ Download JPG",
                            data=image_to_bytes(sheared_img, fmt="JPEG"),
                            file_name="shearing_result.jpg",
                            mime="image/jpeg",
                            key="dl_shear_jpg"
                        )

            elif st.session_state["geo_transform"] == "reflection":
                st.markdown(t["refl_settings"])
                axis = st.selectbox(t["refl_axis"], [t["axis_x"], t["axis_y"], t["axis_diag"]], key="refl_axis")
                if st.button(f"{t['btn_apply']} ✅", key="btn_apply_refl", type="primary"):
                    h, w = original_img.shape[:2]
                    if axis == t["axis_x"]:
                        Rf = np.array([[1, 0, 0],
                                       [0, -1, h],
                                       [0, 0, 1]], dtype=np.float32)
                    elif axis == t["axis_y"]:
                        Rf = np.array([[-1, 0, w],
                                       [0, 1, 0],
                                       [0, 0, 1]], dtype=np.float32)
                    else:
                        Rf = np.array([[0, 1, 0],
                                       [1, 0, 0],
                                       [0, 0, 1]], dtype=np.float32)
                    reflected_img = apply_affine_transform(original_img, Rf)
                    st.image(reflected_img, caption=t["refl_result"], use_column_width=True)

                    col_png, col_jpg = st.columns(2)
                    with col_png:
                        st.download_button(
                            label="⬇️ Download PNG",
                            data=image_to_bytes(reflected_img, fmt="PNG"),
                            file_name="reflection_result.png",
                            mime="image/png",
                            key="dl_refl_png"
                        )
                    with col_jpg:
                        st.download_button(
                            label="⬇️ Download JPG",
                            data=image_to_bytes(reflected_img, fmt="JPEG"),
                            file_name="reflection_result.jpg",
                            mime="image/jpeg",
                            key="dl_refl_jpg"
                        )

    # Histogram box
    with st.container(border=True):
        st.markdown(t["hist_title"])
        st.write(t["hist_desc"])
        show_hist = st.button(t["btn_histogram"], key="btn_histogram", type="secondary")
        if show_hist:
            if original_img is not None:
                hist_fig = compute_histogram(original_img)
                st.pyplot(hist_fig)
                plt.close(hist_fig)
            else:
                st.warning(t["hist_warning"])

with tools_col_right:
    with st.container(border=True):
        st.markdown(t["filter_title"])
        st.write(t["filter_desc"])
        st.markdown("---")

        # Tombol pilih filter
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            if st.button(t["btn_blur"], key="btn_blur_click", type="secondary"):
                st.session_state["image_filter"] = "blur"
        with filter_col2:
            if st.button(t["btn_sharpen"], key="btn_sharpen_click", type="secondary"):
                st.session_state["image_filter"] = "sharpen"
        with filter_col3:
            if st.button(t["btn_background"], key="btn_bg_click", type="secondary"):
                st.session_state["image_filter"] = "background"

        filter_col4, filter_col5, filter_col6 = st.columns(3)
        with filter_col4:
            if st.button(t["btn_grayscale"], key="btn_gray_click", type="secondary"):
                st.session_state["image_filter"] = "grayscale"
        with filter_col5:
            if st.button(t["btn_edge"], key="btn_edge_click", type="secondary"):
                st.session_state["image_filter"] = "edge"
        with filter_col6:
            if st.button(t["btn_brightness"], key="btn_bright_click", type="secondary"):
                st.session_state["image_filter"] = "brightness"

        if original_img is None:
            st.info(t["filter_info"])
        else:
            # ===================== RIGHT IMAGE FILTERING =====================

            # ---- BLUR ----
            if st.session_state["image_filter"] == "blur":
                st.markdown(t["blur_settings"])
                kernel_size = st.selectbox(
                    t["blur_kernel"],
                    [3, 5, 7],
                    index=0,
                    key="blur_kernel_size"
                )
                if st.button(f"{t['btn_apply']} ✅", key="btn_apply_blur", type="primary"):
                    gray = rgb_to_gray(original_img)
                    k = kernel_size
                    blur_kernel = np.ones((k, k), dtype=np.float32) / (k * k)
                    blurred_gray = manual_convolution_gray(gray, blur_kernel)
                    blurred_rgb = cv2.cvtColor(blurred_gray, cv2.COLOR_GRAY2RGB)

                    st.image(blurred_rgb, caption=t["blur_result"], use_column_width=True)

                    col_png, col_jpg = st.columns(2)
                    with col_png:
                        st.download_button(
                            label="⬇️ Download PNG",
                            data=image_to_bytes(blurred_rgb, fmt="PNG"),
                            file_name="blur_result.png",
                            mime="image/png",
                            key="dl_blur_png"
                        )
                    with col_jpg:
                        st.download_button(
                            label="⬇️ Download JPG",
                            data=image_to_bytes(blurred_rgb, fmt="JPEG"),
                            file_name="blur_result.jpg",
                            mime="image/jpeg",
                            key="dl_blur_jpg"
                        )

            # ---- SHARPEN ----
            elif st.session_state["image_filter"] == "sharpen":
                st.markdown(t["sharpen_settings"])
                st.write(t["sharpen_desc"])
                if st.button(f"{t['btn_apply']} ✅", key="btn_apply_sharpen", type="primary"):
                    gray = rgb_to_gray(original_img)
                    sharpen_kernel = np.array(
                        [[0, -1, 0],
                         [-1, 5, -1],
                         [0, -1, 0]],
                        dtype=np.float32
                    )
                    sharpened_gray = manual_convolution_gray(gray, sharpen_kernel)
                    sharpened_rgb = cv2.cvtColor(sharpened_gray, cv2.COLOR_GRAY2RGB)

                    st.image(sharpened_rgb, caption=t["sharpen_result"], use_column_width=True)

                    col_png, col_jpg = st.columns(2)
                    with col_png:
                        st.download_button(
                            label="⬇️ Download PNG",
                            data=image_to_bytes(sharpened_rgb, fmt="PNG"),
                            file_name="sharpen_result.png",
                            mime="image/png",
                            key="dl_sharp_png"
                        )
                    with col_jpg:
                        st.download_button(
                            label="⬇️ Download JPG",
                            data=image_to_bytes(sharpened_rgb, fmt="JPEG"),
                            file_name="sharpen_result.jpg",
                            mime="image/jpeg",
                            key="dl_sharp_jpg"
                        )

            # ---- BACKGROUND REMOVAL / REPLACE ----
            elif st.session_state["image_filter"] == "background":
                st.markdown(t["bg_settings"])
                method = st.selectbox(
                    t["bg_method"],
                    [
                        "HSV Color Thresholding",
                        "Blur Background",
                        "Remove Background (Transparent)",
                        "Solid Red Background",
                        "Solid Blue Background",
                        "Solid Yellow Background",
                        "Solid Green Background",
                        "Solid Brown Background",
                    ],
                    key="bg_method"
                )

                if st.button(f"{t['btn_apply']} ✅", key="btn_apply_bg", type="primary"):
                    bg_removed_img = None
                    output_for_download = None

                    try:
                        if method == "HSV Color Thresholding":
                            bg_removed_img = simple_background_removal_hsv(original_img)
                            output_for_download = bg_removed_img
                        else:
                            if method == "Blur Background":
                                output_mode = "blurred"
                                solid_color = None
                            elif method == "Remove Background (Transparent)":
                                output_mode = "transparent"
                                solid_color = None
                            elif method == "Solid Red Background":
                                output_mode = "solid_color"
                                solid_color = (255, 0, 0)
                            elif method == "Solid Blue Background":
                                output_mode = "solid_color"
                                solid_color = (0, 0, 255)
                            elif method == "Solid Yellow Background":
                                output_mode = "solid_color"
                                solid_color = (255, 255, 0)
                            elif method == "Solid Green Background":
                                output_mode = "solid_color"
                                solid_color = (0, 255, 0)
                            elif method == "Solid Brown Background":
                                output_mode = "solid_color"
                                solid_color = (150, 75, 0)
                            else:
                                output_mode = "transparent"
                                solid_color = None

                            result = remove_background_advanced(
                                image=original_img,
                                mode="auto",
                                output_mode=output_mode,
                                solid_color=solid_color,
                                feather_radius=3,
                                refine_hair=True,
                            )

                            bg_removed_img = result

                            if result.ndim == 3 and result.shape[2] == 4:
                                output_for_download = result[:, :, :3]
                            else:
                                output_for_download = result

                    except Exception as e:
                        st.error(f"Error saat memproses background: {e}")
                        bg_removed_img = None
                        output_for_download = None

                    if bg_removed_img is not None:
                        st.image(bg_removed_img, caption=t["bg_result"], use_column_width=True)

                        col_png, col_jpg = st.columns(2)
                        with col_png:
                            st.download_button(
                                label="⬇️ Download PNG",
                                data=image_to_bytes(bg_removed_img, fmt="PNG"),
                                file_name="background_result.png",
                                mime="image/png",
                                key="dl_bg_png"
                            )
                        with col_jpg:
                            if output_for_download is not None:
                                st.download_button(
                                    label="⬇️ Download JPG",
                                    data=image_to_bytes(output_for_download, fmt="JPEG"),
                                    file_name="background_result.jpg",
                                    mime="image/jpeg",
                                    key="dl_bg_jpg"
                                )
                    else:
                        st.warning("Gagal menghasilkan gambar background. Coba metode lain atau gambar lain.")

            # ---- GRAYSCALE ----
            elif st.session_state["image_filter"] == "grayscale":
                st.markdown(t["gray_settings"])
                st.write(t["gray_desc"])
                if st.button(f"{t['btn_apply']} ✅", key="btn_apply_gray", type="primary"):
                    gray_img = rgb_to_gray(original_img)
                    gray_rgb = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2RGB)

                    st.image(gray_rgb, caption=t["gray_result"], use_column_width=True)

                    col_png, col_jpg = st.columns(2)
                    with col_png:
                        st.download_button(
                            label="⬇️ Download PNG",
                            data=image_to_bytes(gray_rgb, fmt="PNG"),
                            file_name="grayscale_result.png",
                            mime="image/png",
                            key="dl_gray_png"
                        )
                    with col_jpg:
                        st.download_button(
                            label="⬇️ Download JPG",
                            data=image_to_bytes(gray_rgb, fmt="JPEG"),
                            file_name="grayscale_result.jpg",
                            mime="image/jpeg",
                            key="dl_gray_jpg"
                        )

            # ---- EDGE DETECTION ----
            elif st.session_state["image_filter"] == "edge":
                st.markdown(t["edge_settings"])
                method_edge = st.selectbox(
                    t["edge_method"], ["Sobel", "Canny"], key="edge_method"
                )
                if st.button(f"{t['btn_apply']} ✅", key="btn_apply_edge", type="primary"):
                    img_bgr = to_opencv(original_img)
                    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
                    if method_edge == "Sobel":
                        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
                        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
                        mag = cv2.magnitude(grad_x, grad_y)
                        mag = np.clip(mag, 0, 255).astype(np.uint8)
                        edge_bgr = cv2.cvtColor(mag, cv2.COLOR_GRAY2BGR)
                    else:
                        edges = cv2.Canny(gray, 100, 200)
                        edge_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
                    edge_img = to_streamlit(edge_bgr)

                    st.image(edge_img, caption=f"{t['edge_result']} ({method_edge})", use_column_width=True)

                    col_png, col_jpg = st.columns(2)
                    with col_png:
                        st.download_button(
                            label="⬇️ Download PNG",
                            data=image_to_bytes(edge_img, fmt="PNG"),
                            file_name="edge_result.png",
                            mime="image/png",
                            key="dl_edge_png"
                        )
                    with col_jpg:
                        st.download_button(
                            label="⬇️ Download JPG",
                            data=image_to_bytes(edge_img, fmt="JPEG"),
                            file_name="edge_result.jpg",
                            mime="image/jpeg",
                            key="dl_edge_jpg"
                        )

            # ---- BRIGHTNESS / CONTRAST ----
            elif st.session_state["image_filter"] == "brightness":
                st.markdown(t["bright_settings"])
                brightness = st.slider(t["bright_brightness"], -100, 100, 0, key="brightness_value")
                contrast = st.slider(t["bright_contrast"], -100, 100, 0, key="contrast_value")
                if st.button(f"{t['btn_apply']} ✅", key="btn_apply_bright", type="primary"):
                    adjusted_img = adjust_brightness_contrast(original_img, brightness, contrast)

                    st.image(adjusted_img, caption=t["bright_result"], use_column_width=True)

                    col_png, col_jpg = st.columns(2)
                    with col_png:
                        st.download_button(
                            label="⬇️ Download PNG",
                            data=image_to_bytes(adjusted_img, fmt="PNG"),
                            file_name="brightness_contrast_result.png",
                            mime="image/png",
                            key="dl_bright_png"
                        )
                    with col_jpg:
                        st.download_button(
                            label="⬇️ Download JPG",
                            data=image_to_bytes(adjusted_img, fmt="JPEG"),
                            file_name="brightness_contrast_result.jpg",
                            mime="image/jpeg",
                            key="dl_bright_jpg"
                        )

# ===================== TEAM MEMBERS =====================

st.markdown(t["team_title"])
st.write(t["team_subtitle"])

members = [
    {"img": "images/gitsi.jpg", "name": "Gita Sion Nauli Simatupang", "sid": "004202400055", "role": "Leader", "Contribution": "Project Manager, Geometric Transformations Module"},
    {"img": "images/bella.jpg", "name": "Bella Amelia", "sid": "004202400050", "role": "Member", "Contribution": "Image Filtering Module, UI/UX Design"},
    {"img": "images/chinta.jpg", "name": "Chinta Amanda Dwi Putri Carelina", "sid": "004202400035", "role": "Member", "Contribution": "Background Removal Module, Image Upload & Download"},
    {"img": "images/yessa.jpg", "name": "Yessa Kireina Hanna Sevira", "sid": "004202400009", "role": "Member", "Contribution": "Histogram Module, Image Processing Functions"},
]

cols_row1 = st.columns(2, vertical_alignment="top")
for i in range(2):
    with cols_row1[i]:
        with st.container(border=True):
            m = members[i]
            col_img, col_info = st.columns([1, 2], vertical_alignment="center")
            with col_img:
                safe_display_square_image(m["img"])
            with col_info:
                st.markdown(f"**{m['name']}**")
                st.markdown(f"{t['team_sid']} {m['sid']}")
                st.markdown(f"{t['team_role']} {m['role']}")
                st.markdown(f"{t['team_group']} 5")
                st.markdown(f"{t['team_contribution']} {m['Contribution']}")

cols_row2 = st.columns(2, vertical_alignment="top")
for i in range(2, 4):
    with cols_row2[i - 2]:
        with st.container(border=True):
            m = members[i]
            col_img, col_info = st.columns([1, 2], vertical_alignment="center")
            with col_img:
                safe_display_square_image(m["img"])
            with col_info:
                st.markdown(f"**{m['name']}**")
                st.markdown(f"{t['team_sid']} {m['sid']}")
                st.markdown(f"{t['team_role']} {m['role']}")
                st.markdown(f"{t['team_group']} 5")
                st.markdown(f"{t['team_contribution']} {m['Contribution']}")





