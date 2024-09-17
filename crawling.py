import streamlit as st
import instaloader
import pandas as pd

# Fungsi untuk crawling komentar
def crawl_comments(username, password, url, max_comments):
    st.write(f"Crawling the comments from: {url}")

    L = instaloader.Instaloader()

    try:
        # Autentikasi dengan login
        L.context.login(user=username, passwd=password) 
        #===============AKUN INSTAGRAN LOGIN=================
        #user : nesztman pass : PjOnuC8G84RBXhV
        #user : crawling5 pass : Afta2034!
        #user : udin.petod766 pass : Afta2034!
        #====================================================

        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        comments = []
        count = 0

        for comment in post.get_comments():
            comments.append(comment.text)
            count += 1

            if count >= max_comments:
                break

        st.success(f"Crawling was successful. Total {count} comments were successfully captured.")
        return comments

    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")
        return []

# Fungsi untuk menampilkan hasil crawling dan menyimpan dalam CSV
def show_results(comments):
    st.header("Comment Crawling Result")
    
    if comments:
        st.write("An example of some comments:")
        st.write(comments[:2])

        # Form untuk memasukkan jumlah komentar yang akan diunduh
        download_count = st.number_input("Jumlah komentar yang akan diunduh", min_value=1, max_value=len(comments), value=len(comments))
        
        # Bagi hasil crawling menjadi beberapa file CSV
        num_files = len(comments) // 300
        for i in range(num_files):
            start_idx = i * 300
            end_idx = (i + 1) * 300
            csv_data = pd.DataFrame(comments[start_idx:end_idx], columns=["Komentar"]).to_csv(index=False)
            st.download_button(label=f"Unduh CSV {i+1}", data=csv_data, file_name=f"comments_{i+1}.csv", key=f"comments_csv_{i+1}")

    else:
        st.warning("Tidak ada komentar yang berhasil diambil.")

# Fungsi untuk menampilkan hasil crawling dan menyimpan dalam CSV
def show_results(comments):
    st.header("Crawling Result Comments")
    
    if comments:
        st.write("Example of some comments:")
        st.write(comments[:15])

        # Form untuk memasukkan jumlah komentar yang akan diunduh
        download_count = st.number_input("Jumlah komentar yang akan diunduh", min_value=1, max_value=len(comments), value=len(comments))
        
        # Tombol unduh CSV
        csv_data = pd.DataFrame(comments[:download_count], columns=["Komentar"]).to_csv(index=False)
        st.download_button(label="Unduh CSV", data=csv_data, file_name="comments.csv", key="comments_csv")

    else:
        st.warning("Tidak ada komentar yang berhasil diambil.")

# Main program
def crawler():
    #st.set_page_config(page_title="Instagram Comment Crawler", page_icon=":camera:")

    #st.title("Instagram Comment Crawler")

    # Form untuk memasukkan kredensial Instagram
    username = st.text_input("Username Instagram")
    password = st.text_input("Password Instagram")

    # Form untuk memasukkan URL Instagram
    instagram_url = st.text_input("Masukkan URL Instagram", "")
    
    # Form untuk memasukkan jumlah komentar yang akan diambil
    max_comments = st.number_input("Jumlah maksimal komentar yang diambil perhari (maks 320)", min_value=1, value=10)

    # Tombol untuk melakukan crawling
    # Tombol untuk melakukan crawling
    if st.button("Crawling"):
    # Mengganti max_comments dengan nilai yang besar atau tidak ada batas
        comments = crawl_comments(username, password, instagram_url, max_comments)
        show_results(comments)