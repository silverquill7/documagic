import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000/api/documents")

st.set_page_config(page_title="DocuMagic Dashboard", layout="wide")
st.title("DocuMagic - Documents")

with st.sidebar:
    st.markdown("### Settings")
    st.write("API:", API_BASE)

st.write("## Documents")
res = requests.get(API_BASE)
if res.status_code != 200:
    st.error("Could not fetch documents: " + str(res.status_code))
else:
    docs = res.json()
    for d in docs:
        st.markdown(f"### {d.get('filename')}  — status: {d.get('status')}")
        st.write("Source:", d.get("source"), "| Sender:", d.get("sender"))
        if d.get("parsed"):
            st.text(d.get("parsed"))
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button(f"Preview {d['id']}", key=f"preview-{d['id']}"):
                detail = requests.get(f"{API_BASE}/{d['id']}")
                if detail.ok:
                    st.code(detail.json().get("content")[:10000])
        with col2:
            if st.button(f"Reparse {d['id']}", key=f"reparse-{d['id']}"):
                r = requests.post(f"{API_BASE}/{d['id']}/reparse")
                if r.ok:
                    st.success("Reparse triggered (completed)")
                else:
                    st.error("Reparse failed: " + str(r.status_code))
