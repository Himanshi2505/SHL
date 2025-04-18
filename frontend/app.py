import streamlit as st
import requests

st.title("SHL Assessment Recommendation System")

query = st.text_area("Enter job description or query")

if st.button("Get Recommendations"):
    if query:
        with st.spinner("Fetching assessments..."):
            response = requests.get("http://localhost:8000/api/recommend", params={"query": query})
            results = response.json()["results"]

            if results:
                st.success(f"Top {len(results)} assessments found:")
                for item in results:
                    st.markdown(f"### [{item['name']}]({item['url']})")
                    st.write(f"**Remote Testing:** {item['remote_testing']}")
                    st.write(f"**Adaptive/IRT:** {item['adaptive_irt']}")
                    st.write(f"**Duration:** {item['duration']} | **Test Type:** {item['test_type']}")
                    st.markdown("---")
            else:
                st.warning("No relevant assessments found.")
