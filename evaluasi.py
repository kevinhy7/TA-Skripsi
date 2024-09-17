import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns

def check_login_status():
    return st.session_state.is_logged_in

# Add initialization block
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Fungsi untuk halaman evaluasi
def evaluasi():
    if check_login_status():

        # Upload file CSV
        uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])

        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)

            # Menampilkan jumlah data dalam file
            st.markdown(
                f"<p>Jumlah data dalam file: {data.shape[0]}</p>", 
                unsafe_allow_html=True
            )

            # Memastikan dataset memiliki minimal 2 kelas (positif, negatif, netral)
            if len(data['sentiment_label'].unique()) < 2:
                st.error("Dataset harus memiliki minimal 2 kelas.")
                return
            
            col1, col2 = st.columns(2)

            # Menampilkan jumlah masing-masing sentimen
            sentiment_counts = {
                'positif': (data['nilai_sentiment'] > 0).sum(),
                'negatif': (data['nilai_sentiment'] < 0).sum(),
                'netral': (data['nilai_sentiment'] == 0).sum()
            }
            
            with col1:
                st.write("\nJumlah Masing-masing Sentimen:")
                st.write("Positif:", sentiment_counts.get('positif', 0))
                st.write("Negatif:", sentiment_counts.get('negatif', 0))
                st.write("Netral:", sentiment_counts.get('netral', 0))

            # Membersihkan data dari nilai NaN
            data_clean = data.dropna()

            # Memisahkan data menjadi fitur (X) dan label (y)
            X = data_clean['text_clean']
            y = data_clean['sentiment_label']

            # Memisahkan data menjadi set pelatihan dan pengujian
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=70)

            # Membuat vektor fitur TF-IDF
            tfidf_vectorizer = TfidfVectorizer()
            X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)

            # Konversi vektor fitur TF-IDF menjadi DataFrame
            tfidf_df = pd.DataFrame(X_train_tfidf.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

            # Tampilkan DataFrame TF-IDF
            #with col3:
            st.write("\nDataFrame TF-IDF:")
            st.write(tfidf_df)

            # Melatih model (contoh menggunakan regresi logistik)
            model = LogisticRegression(max_iter=1000)
            model.fit(X_train_tfidf, y_train)

            # Membuat prediksi pada set pengujian
            X_test_tfidf = tfidf_vectorizer.transform(X_test)
            y_pred = model.predict(X_test_tfidf)

            # Menghitung confusion matrix
            cm = confusion_matrix(y_test, y_pred)

            # Menghitung metrik evaluasi dalam persentase
            accuracy = accuracy_score(y_test, y_pred) * 100
            precision = precision_score(y_test, y_pred, average='weighted') * 100
            recall = recall_score(y_test, y_pred, average='weighted') * 100

            with col2:
                # Menampilkan metrik evaluasi dalam persentase
                st.write("\nMetrik Evaluasi:")
                st.write("Akurasi:", f"{accuracy:.2f}%")
                st.write("Presisi:", f"{precision:.2f}%")
                st.write("Recall:", f"{recall:.2f}%")

            # Menampilkan confusion matrix sebagai gambar
            st.write("\nConfusion Matrix:")
            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
            ax.set_xticklabels(data['sentiment_label'].unique())  # Label untuk sumbu x
            ax.set_yticklabels(data['sentiment_label'].unique())  # Label untuk sumbu y
            ax.set_xlabel('prediction')
            ax.set_ylabel('Actual')
            ax.set_title('Confusion Matrix')
            st.pyplot(fig)

            # Visualisasi diagram batang untuk kelas aktual
            st.write("\nVisualisasi Diagram Batang untuk Kelas Aktual:")
            fig, ax = plt.subplots(figsize=(3, 2))
            sns.countplot(data=data, x='sentiment_label', palette='viridis', ax=ax)
            ax.set_title('Diagram Batang untuk Kelas Aktual')
            ax.set_xlabel('Class')
            ax.set_ylabel('amount')
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)

            # Visualisasi diagram lingkaran untuk kelas prediksi
            st.write("\nVisualisasi Diagram Lingkaran untuk Kelas Prediksi:")
            fig, ax = plt.subplots(figsize=(8, 6))
            pd.Series(y_pred).value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['skyblue', 'salmon', 'lightgreen'], ax=ax)
            ax.set_title('Diagram Lingkaran untuk Kelas Prediksi')
            ax.set_ylabel('')
            st.pyplot(fig)

            # Filter hanya baris dengan sentimen negatif
            data_negatif = data_clean[data_clean['sentiment_label'] == 'Negative']

            if data_negatif.empty:
                st.warning("Tidak ada data dengan sentimen negatif.")
                return

            # Menampilkan dataframe untuk kolom text_clean, sentiment_label, dan nilai_sentiment
            st.write("\nDataframe untuk Kolom text_clean, sentiment_label, dan nilai_sentiment:")
            st.write(data_negatif[['text_clean', 'sentiment_label', 'nilai_sentiment']])

            
        else:
            st.warning("Silakan unggah file CSV untuk mulai menganalisis.")
    else:
        st.warning("Anda belum login. Silakan login terlebih dahulu.")

# Menjalankan fungsi evaluasi saat aplikasi dijalankan
evaluasi()
