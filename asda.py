import streamlit as st
import requests
from collections import Counter
import yake
import re

# YouTube API Setup
API_KEY = st.secrets["API_KEY"]  # Set via Streamlit Secrets
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

# Streamlit App
st.title("🚀 YouTube Video SEO Optimizer")

# User Input
target_keyword = st.text_input("social security benefits' Trump Executive Order:")
num_competitors = st.slider("5”)

if st.button("Generate SEO Recommendations"):
    if not target_keyword:
        st.warning("Please enter a keyword!")
    else:
        try:
            # Fetch Top Competitor Videos
            params = {
                "part": "snippet",
                "q": target_keyword,
                "type": "video",
                "order": "viewCount",
                "maxResults": num_competitors,
                "key": API_KEY
            }
            response = requests.get(YOUTUBE_SEARCH_URL, params=params).json()

            if "items" not in response:
                st.error("No videos found. Try a different keyword.")
                st.stop()

            # Extract Titles & Descriptions
            titles = []
            descriptions = []
            for item in response["items"]:
                titles.append(item["snippet"]["title"])
                descriptions.append(item["snippet"]["description"])

            # YAKE Keyword Extraction
            def extract_keywords(text_list):
                kw_extractor = yake.KeywordExtractor(top=20)
                all_keywords = []
                for text in text_list:
                    text_clean = re.sub(r'\W+', ' ', text.lower())
                    keywords = kw_extractor.extract_keywords(text_clean)
                    all_keywords.extend([kw[0] for kw in keywords])
                return Counter(all_keywords).most_common(10)

            # Get Recommendations
            title_keywords = extract_keywords(titles)
            desc_keywords = extract_keywords(descriptions)

            # Display Results
            st.subheader("🔥 Top Title Keywords")
            st.write("Use these in your video title:")
            st.code(", ".join([kw[0] for kw in title_keywords]))

            st.subheader("📝 Top Description Keywords")
            st.write("Include these in your description:")
            st.code(", ".join([kw[0] for kw in desc_keywords]))

            st.subheader("🏆 Top Ranking Competitors")
            for idx, title in enumerate(titles[:5], 1):
                st.write(f"{idx}. {title}")

        except Exception as e:
            st.error(f"Error: {str(e)}")
