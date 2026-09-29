import streamlit as st
import requests

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

BACKEND_URL = "http://127.0.0.1:8000"

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

document_type = st.selectbox(
    "Document Type",
    [
        "Employment Contract",
        "Lease Agreement",
        "Non-Disclosure Agreement",
        "Service Agreement",
        "Other"
    ]
)

parties = st.text_area(
    "Parties",
    placeholder="Example: Employer: ABC Pvt Ltd\nEmployee: John Doe"
)

terms = st.text_area(
    "Terms",
    placeholder="Enter the important terms and conditions..."
)

dates = st.text_input(
    "Dates",
    placeholder="Example: 01-10-2026 to 30-09-2027"
)

if st.button("Generate Document", type="primary"):
    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "dates": dates
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/generate",
            json=payload,
            timeout=120
        )

        if response.ok:
            data = response.json()
            document = data.get("document", "")

            st.success("Document generated successfully!")

            edited_document = st.text_area(
                "Edit Document",
                value=document,
                height=500
            )

            st.download_button(
                "Download TXT",
                edited_document,
                file_name="legalease_document.txt",
                mime="text/plain"
            )
        else:
            st.error(f"Backend error: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to backend. "
            "Make sure FastAPI is running on port 8000."
        )
    except Exception as e:
        st.error(f"Error: {e}")