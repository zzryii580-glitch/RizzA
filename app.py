import requests
import streamlit as st

st.set_page_config(
    page_title="Chongqing 24/7 Custom AI Agency", page_icon="🏙️", layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #030508;
        color: #00ffcc;
        font-family: 'Courier New', monospace;
    }
    .neon-title {
        color: #ffffff;
        text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc, 0 0 30px #ff007f, 0 0 40px #ff007f;
        font-size: 2.3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    @keyframes particleMove {
        0% { background-position: 0 0; }
        100% { background-position: 1000px 1000px; }
    }
    .starfield-bg {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 999;
        background-image: radial-gradient(2px 2px at 30px 40px, #00ffcc, rgba(0,0,0,0)),
                          radial-gradient(2px 2px at 100px 150px, #ff007f, rgba(0,0,0,0));
        background-repeat: repeat; background-size: 250px 250px;
        animation: particleMove 15s linear infinite; opacity: 0.3;
    }
    .stTextArea textarea {
        background-color: #090e1a !important; color: #00ffcc !important; border: 1px solid #ff007f !important;
    }
    </style>
    <div class="starfield-bg"></div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="neon-title">CHONGQING 24/7 CUSTOM AI AGENCY</div>',
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #ff007f;'>Sistem AI Mandiri"
    " Menggunakan Model Sendiri & API Key Pribadi | DANA & WhatsApp</p>",
    unsafe_allow_html=True,
)

st.sidebar.markdown("### 🌆 Status Pusat Operasi")
st.sidebar.success("Agen Aktif: 🟢 24 Jam Non-Stop")
st.sidebar.info(
    "• Animasi Partikel: Aktif\n• Model AI: Lokal Mandiri\n• API Key: Kustom"
    " Pribadi\n• DANA & WA: Terhubung"
)

col1, col2 = st.columns([2, 1])

with col1:
  st.markdown("### 📝 Perintah Kerja Klien")
  user_prompt = st.text_area(
      "Masukkan instruksi konten atau kampanye pemasaran:",
      placeholder=(
          "Contoh: Buatkan konten promosi produk fashion cyberpunk gaya"
          " Chongqing."
      ),
      height=140,
  )
  client_phone = st.text_input(
      "Nomor WhatsApp Anda (Untuk notifikasi darurat):",
      placeholder="628xxxxxxxxxx",
  )

  if st.button("🚀 Jalankan Agen AI Sendiri"):
    if not user_prompt:
      st.warning("Mohon isi instruksi perintah kerja terlebih dahulu!")
    else:
      with st.spinner(
          "🤖 Model AI lokal Anda sedang bekerja secara mandiri..."
      ):
        try:
          response = requests.post(
              "http://localhost:8000/run-agent",
              json={"prompt": user_prompt, "client_phone": client_phone},
              timeout=150,
          )

          if response.status_code == 200:
            res_data = response.json()
            st.success("✨ Tugas Berhasil Dikerjakan oleh AI Buatan Anda!")
            st.markdown("### Hasil Output Model AI:")
            st.write(res_data["result"])
          else:
            st.error(
                f"Kendala pada sistem: {response.json().get('detail')}"
            )
        except Exception as e:
          st.error(
              f"Gagal terhubung ke backend. Pastikan 'backend.py' menyala."
              f" Error: {e}"
          )

with col2:
  st.markdown("### 💳 Pembayaran Otomatis DANA")
  st.markdown(
      "Simulasi pembayaran klien masuk secara otomatis ke DANA Anda."
  )
  if st.button("Simulasi Pembayaran Masuk (DANA)"):
    try:
      pay_res = requests.post(
          "http://localhost:8000/webhook/dana-payment",
          json={"order_id": "CHQ-CUSTOM-01", "status": "success", "amount": 100000},
      )
      st.success(pay_res.json()["message"])
    except Exception as e:
      st.error(f"Gagal memproses pembayaran: {e}")
