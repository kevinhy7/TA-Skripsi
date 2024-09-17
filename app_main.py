from email.mime import image
import streamlit as st
import pandas as pd
from io import BytesIO
import base64
from crawling import crawler as crawler_main
from Pre_procesing import preprocessing_dataframe
from pelabelan import sentistrength, process_uploaded_file  # Import sentistrength and process_uploaded_file from pelabelan.py
from evaluasi import evaluasi
from gabung import main as gabung  # Import combine_comments function
from PIL import Image
import auth

# Inisialisasi session_state
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Fungsi untuk logout
def logout():
    st.session_state.is_logged_in = False
    st.session_state.username = ""
    st.experimental_rerun()

# Fungsi untuk halaman home
def home():
    st.title("Beranda")

    if st.session_state.is_logged_in:
        st.write(f"Selamat datang, {st.session_state.username}!")
        #st.button("Logout", on_click=logout)

        # Konten analisis sentiment
        st.header("Project TA")
        st.header("Analisis Sentimen")
        st.write("Analisis sentimen adalah proses untuk mengidentifikasi dan memahami opini, perasaan, dan sikap yang terkandung dalam teks, seperti ulasan pelanggan atau posting media sosial. Tujuannya adalah untuk memberikan wawasan tentang bagaimana orang merespons suatu topik, merek, produk, atau peristiwa, sehingga membantu organisasi membuat keputusan bisnis yang lebih baik, meningkatkan pengalaman pelanggan, mendeteksi isu atau masalah, dan meningkatkan reputasi merek mereka.")
        # Membuat teks di bawah dengan ikon anak panah ke arah kiri
        st.write("""
        <div style="text-align:center">
            <h3>Siap Mencoba melakukan analisis sentiment</h3>
            <p><i class="fas fa-arrow-circle-left"></i></p>
        </div>
        """, unsafe_allow_html=True)

        # Menambahkan hak cipta di bawah
        st.write("""
        <div style="text-align:center">
            <p>Hak Cipta © 2024 Kevinhy7 - 202011420010</p>
        </div>
        """, unsafe_allow_html=True)
        # Tambahkan konten analisis sentiment sesuai kebutuhan

    else:
        st.warning("Anda belum login. Silakan login terlebih dahulu.")

# Fungsi untuk halaman crawler
def crawler():
    st.title("Mengambil Komentar Instagram")
    st.write("Tahapan Crawling Data Komentar Instagram")
    st.write("1. Masukan User dan Pass instagram (User dan Pass Tidak Akan disimpan Kedalam Sistem) ")
    st.write("2. Masukan Link Postingan Instagram \t \t pastikan link seperti ini https://www.instagram.com/p/C9J-d24xPY9/")
    st.write("3. Atur batasan Sebarapa banyak komentar yang mau Dicrawling (Batas harian 1 akun 320 komentar)")
    st.write("4. Tekan Muali Crawling")
    st.write("5. Review Singkat Dalam Bentuk Dataframe")
    st.write("6. Unduh dataset Menjadi Dokument .csv / excel")
    if st.session_state.is_logged_in:
        crawler_main()
    else:
        st.warning("Anda belum login. Silakan login terlebih dahulu.")

# Fungsi untuk halaman pre-processing
def preprocessing_page():
    st.title("Pre-processing")
    st.write("Tahapan Preprocessing Data Komentar Instagram")

    st.write("1. Upload File CSV Yang Sudah Diunduh Pada Proses Crawling")
    st.write("2. Tekan Mulai Pre-processing")
    st.write("3. Review Singkat Dalam Bentuk Dataframe")
    st.write("4. Unduh dataset Menjadi Dokument .csv / excel")

    if st.session_state.is_logged_in:
        data_file = st.file_uploader("Upload CSV file", type=["csv"])
        if data_file is not None:
            df = pd.read_csv(data_file)
            st.dataframe(df)

            if st.button('Start Pre-processing'):
                df = preprocessing_dataframe(df)
                st.write("Data setelah pre-processing:")
                st.dataframe(df)

                # Menampilkan tombol unduh hanya jika proses preprocessing telah selesai
                if df is not None:
                    st.download_button(label='Download CSV', data=df.to_csv(index=False, encoding='utf-8'), file_name='Labeled.csv')
        else:
            st.warning("Silakan unggah file CSV untuk mulai menganalisis.")
    else:
        st.warning("Anda belum login. Silakan login terlebih dahulu.")

# Fungsi untuk halaman pelabelan
def pelabelan_page():
    st.title("Analisis Sentimen Dengan Sentistrength Dan Lexicon Based")

    st.write("Tahapan Pelabelan Data Komentar Instagram")

    st.write("1. Upload File CSV Yang Sudah Diunduh Pada Proses Pre-Procesing")
    st.write("2. Data Akan Secara Otomatis Dilabeli")
    st.write("3. Review Singkat Dalam Bentuk Dataframe")
    st.write("4. Unduh dataset Menjadi Dokument .csv / excel")

    if st.session_state.is_logged_in:
        # Your code for the pelabelan page goes here
        # You can use sentistrength and process_uploaded_file from pelabelan.py directly

        # Konfigurasi Streamlit untuk mengunggah file CSV
        uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])
        lexicon_file = "G:/analisis_sentiment/Lexicon based/lexicon_based_dataset1.csv"  # Path to lexicon file, change it accordingly

        if uploaded_file is not None:
            # Membuat objek senti
            config = dict()
            config["negation"] = True
            config["booster"]  = True
            config["ungkapan"]  = True
            config["consecutive"]  = True
            config["repeated"]  = True
            config["emoticon"]  = True
            config["question"]  = True
            config["exclamation"]  = True
            config["punctuation"]  = True
            senti = sentistrength(config, lexicon_file)

            # Panggil fungsi untuk memproses file yang diunggah
            results = process_uploaded_file(uploaded_file, senti)
            
            # Tampilkan hasil analisis sentimen
            st.write("Hasil Analisis Sentimen:")
            df_results = pd.DataFrame(results)
            st.write(df_results)

            # Tombol unduh file CSV
            filename = "Pembobotan Lexicon Based & Sentistrenght.csv"
            csv = df_results.to_csv(index=False)
            # Menggunakan fungsi download_button untuk menghasilkan tombol unduh
            st.download_button(label="Klik di sini untuk mengunduh hasil" , data=csv , file_name=filename , mime='text/csv')


        else:
            st.warning("Silakan unggah file CSV untuk mulai menganalisis.")
    else:
         # Jika pengguna belum login, tampilkan pesan peringatan
        st.warning("Anda belum login. Silakan login terlebih dahulu.")


def main():
    # Set page configuration based on login status
    if st.session_state.is_logged_in:
        st.set_page_config(page_title="Home", page_icon=":house:")
    else:
        st.set_page_config(layout="wide", page_title="Login and Register", page_icon=":lock:")

    # Render content based on login status and selected page
    if st.session_state.is_logged_in:
        # Render content for logged-in users
        with st.sidebar:
            st.sidebar.title("Navigasi")
            image_url = "https://getthematic.com/assets/img/sentiment-analysis/fine-grained.png"  # Ganti dengan URL gambar yang sesuai
            st.image(image_url, use_column_width=True)
            st.caption("© Kevin Heryadi Yunior 2024")

        selected_page = st.sidebar.radio("Pilih Halaman", ["Beranda", "Crawling", "Preprocessing", "Pelabelan", "gabungkan file csv", "Evaluasi" , "Logout"])

        if selected_page == "Beranda":
            home()  # Call the home function here
        elif selected_page == "Crawling":
            crawler()
        elif selected_page == "Preprocessing":
            preprocessing_page()  # Call the preprocessing_page function here
        elif selected_page == "Pelabelan":
            pelabelan_page()
        elif selected_page == "gabungkan file csv":
            st.title("Gabungkan Komentar dari File CSV")
            gabung()
        elif selected_page == "Evaluasi":
            st.title("Evaluasi dan Perhitungan Confusion Matrix 3 X 3")
            evaluasi()
        elif selected_page == "Logout":
            logout()
    else:
        # Render content for non-logged-in users
        col1, col2 = st.columns([1.5 , 1.5])  # Adjust the ratio based on your preference

        with col1:
            image_url = "https://th.bing.com/th/id/R.cb943c1e254b2a775ad2e568695faa67?rik=Ok321CxdWW4sdg&pid=ImgRaw&r=0"  # Ganti dengan URL gambar yang sesuai
            # Tampilkan tulisan "Analisis Sentiment Cyberbullying" di tengah
            st.markdown(
                """
                <div style="text-align: center;">
                    <h1>Analisis Sentiment Cyberbullying</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Tampilkan gambar
            st.image(image_url, use_column_width=True)
            

        with col2:
            with st.expander("Login", expanded=True):
                if auth.login():
                    st.session_state.is_logged_in = True  # Set session state to indicate user is logged in

            with st.expander("Registrasi"):
                auth.register()

    # Fungsi untuk mengeksekusi aplikasinya
if __name__ == '__main__':
    main()