import streamlit as st
import pandas as pd
from io import StringIO
import base64

def combine_comments(csv_files):
    combined_df = pd.concat(csv_files, ignore_index=True)
    return combined_df

def check_login_status():
    return st.session_state.is_logged_in

def main():
    if check_login_status():

        #container = st.container(border=True)
        #container.write("Proses dimulai dengan pengambilan data komentar dari Instagram melalui crawling, diikuti dengan pra-pemrosesan data untuk membersihkan dan menormalkan teks. Selanjutnya, komentar-komentar tersebut dilabeli dengan sentimen menggunakan metode lexicon-based atau machine learning. Setelah proses pelabelan selesai, hasilnya digabungkan menjadi satu file CSV yang berisi data komentar beserta label sentimen yang sesuai. File CSV ini kemudian siap digunakan untuk analisis lebih lanjut dalam program evaluasi. Dengan demikian, alur ini memastikan bahwa data dari komentar Instagram telah diproses dan disiapkan untuk analisis sentimen yang lebih lanjut dengan cara yang efisien dan terstruktur.")


        uploaded_files = st.file_uploader("Upload file CSV (maksimal 5)", accept_multiple_files=True, type="csv")
        if uploaded_files:
            st.write("Berikut adalah file-file yang diupload:")
            for uploaded_file in uploaded_files:
                st.write(uploaded_file.name)
            
            # Proses file-file yang diupload
            csv_files = []
            for uploaded_file in uploaded_files:
                csv_files.append(pd.read_csv(uploaded_file))
            
            combined_df = combine_comments(csv_files)
            
            st.write("Hasil penggabungan komentar:")
            st.write(combined_df)
            
            # Tombol untuk mengunduh file CSV hasil penggabungan
            st.markdown(get_csv_download_link(combined_df), unsafe_allow_html=True)
        else:
            st.warning("Silakan unggah file CSV untuk mulai menganalisis.")
    else:
        st.warning("Anda belum login. Silakan login terlebih dahulu.")

def get_csv_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="combined_comments.csv">Download CSV File</a>'
    return href
