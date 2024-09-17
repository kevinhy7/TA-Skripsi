import streamlit as st
import pandas as pd
import numpy as np
import re
import string
import nltk
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import hashlib

# Fungsi-fungsi Pre-processing
def cleansing(text):
    if isinstance(text, str):
        text = re.sub(r"\d+","", text)
        text = text.encode('ascii', 'replace').decode('ascii')
        text = ' '.join(re.sub(r"([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)", " ", text).split())
        text = re.sub(r'[^a-zA-Z]', ' ', text)
        text = re.sub(r'\b[a-zA-Z]\b', ' ', text)
        text = re.sub(r'(.)\1+', r'\1\1', text)
        text = re.sub(r'[\?\.\!]+(?=[\?.\!])', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.translate(text.maketrans("", "", string.punctuation))
        text = text.strip()
    else:
        text = str(text)
    return text

def casefolding(text):
    text = text.lower()
    return text

def tokenize(text):
    text = word_tokenize(text)
    return text

def normalized_term(text):
    normalizad_word = pd.read_excel("G:/analisis_sentiment/dataset/normal.xlsx")
    normalizad_word_dict = {}
    for index, row in normalizad_word.iterrows():
        if row[0] not in normalizad_word_dict:
            normalizad_word_dict[row[0]] = row[1]
    return [normalizad_word_dict[term] if term in normalizad_word_dict else term for term in text]

def load_stopwords_from_csv():
    stopwords_file = "G:/analisis_sentiment/dataset/stopwordsID.csv"
    stopwords_list = set()
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            stopwords_list.update(row)
    return stopwords_list

def stopword(text, stopwords_list):
    filtered = [word for word in text if word.lower() not in stopwords_list]
    return filtered 

def steamming(text):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    text = [stemmer.stem(word) for word in text]
    return text

def remove_punct(text):
    text = " ".join([char for char in text if char not in string.punctuation])
    return text

def hash_text(text):
    return hashlib.md5(text.encode()).hexdigest()

def preprocessing_dataframe(df):
    st.write("===========================================================")
    st.write("Start Pre-processing")

    # Load stopwords
    stopwords_list = load_stopwords_from_csv()

    # cleaning
    df['cleaning'] = df['Komentar'].apply(cleansing)
    st.text("Cleaned text:")
    st.dataframe(df['cleaning'])

    # case folding
    df['Case_Folding'] = df['cleaning'].apply(casefolding)
    st.text("Case folded text:")
    st.dataframe(df['Case_Folding'])

    # tokenizing
    df['Tokenization'] = df['Case_Folding'].apply(tokenize)
    st.text("Tokenized text:")
    st.dataframe(df['Tokenization'])

    # Inisialisasi session_state jika belum ada
    if 'unique_hashes' not in st.session_state:
        st.session_state.unique_hashes = set()

    # hashing
    df['Hashed_Text'] = df['Tokenization'].apply(lambda x: hash_text(' '.join(x)))

    # Check for duplicate sentences
    df = df[df['Hashed_Text'].apply(lambda x: x not in st.session_state.unique_hashes or st.session_state.unique_hashes.add(x))]

    # normalization
    df['Normalisasi'] = df['Tokenization'].apply(normalized_term)
    st.text("Normalized text:")
    st.dataframe(df['Normalisasi'])

    # removal stopwords
    df['Stopwords'] = df['Normalisasi'].apply(lambda x: stopword(x, stopwords_list))
    st.text("Stopword removed text:")
    st.dataframe(df['Stopwords'])

    # stemming
    df['Steaming'] = df['Stopwords'].apply(steamming)
    st.text("Stemmed text:")
    st.dataframe(df['Steaming'])

    # Remove Punctuation
    df['text_clean'] = df['Steaming'].apply(lambda x: remove_punct(x))
    #st.write("Text with removed punctuation:")
    #st.write(df['text_clean'])

    # Remove NaN file
    df['text_clean'].replace('', np.nan, inplace=True)
    df.dropna(subset=['text_clean'], inplace=True)

    # Reset index number
    df = df.reset_index(drop=True)
    st.write("Finish Pre-processing")
    st.write("===========================================================")

    return df
