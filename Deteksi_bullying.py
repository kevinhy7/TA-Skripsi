import streamlit as st
import pandas as pd

# Function to read CSV file and display results
def process_csv(csv_file_path, threshold):
    # Read CSV file
    df = pd.read_csv(csv_file_path)
    
    # Convert threshold to string
    if threshold < 0:
        threshold_str = 'Negative'
    elif threshold == 0:
        threshold_str = 'Neutral'
    else:
        threshold_str = 'Positive'

    # Display CSV data
    st.write("CSV Data:")
    st.write(df[['text_clean', 'sentiment_label']])
    
    # Split data into three categories: cyberbullying detected, not detected, and neutral
    cyberbullying_detected_df = df[df['sentiment_label'] <= threshold_str][['text_clean', 'sentiment_label']]
    no_cyberbullying_detected_df = df[df['sentiment_label'] > threshold_str][['text_clean', 'sentiment_label']]
    neutral_df = df[df['sentiment_label'] == 'Neutral'][['text_clean', 'sentiment_label']]
    
    # Display Cyberbullying Detected table
    st.write("Cyberbullying Detected:")
    st.write(cyberbullying_detected_df)
    
    # Display No Cyberbullying Detected table
    st.write("No Cyberbullying Detected:")
    st.write(no_cyberbullying_detected_df)

    # Display Neutral table
    st.write("Neutral:")
    st.write(neutral_df)

def main():
    st.title("Cyberbullying Detection App")
    
    # Upload CSV file
    csv_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    # Set threshold for cyberbullying detection
    threshold = st.slider("Set threshold for cyberbullying detection", min_value=-5.0, max_value=5.0, value=0.0, step=1.0)
    
    # If CSV file is uploaded, process it
    if csv_file is not None:
        process_csv(csv_file, threshold)

if __name__ == "__main__":
    main()
