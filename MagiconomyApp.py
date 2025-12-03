import streamlit as st
import matplotlib.pyplot as plt
from atomwords import draw_atom_words_from_dict  # your plotting function
import glyphdict
import modsdict
import pandas as pd
import base64
from pdf2image import convert_from_path
def render_pdf_as_images(pdf_path):
    """Convert each PDF page to an image and display it."""
    if not os.path.exists(pdf_path):
        st.error(f"PDF file not found: {pdf_path}")
        return

    # Convert pages to images
    pages = convert_from_path(pdf_path, dpi=150)

    # Display each page as an image
    for i, page in enumerate(pages):
        st.image(page, caption=f"Page {i+1}", use_column_width=True)
def display_pdf(pdf_path: str):
    """Embed a PDF into the Streamlit app."""
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%" height="900"
            type="application/pdf">
        </iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

st.markdown("""
<style>
.styled-table {
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 1.0rem;
    font-family: sans-serif;
    min-width: 400px;
    border: 1px solid #ddd;
}
.styled-table th {
    background-color: #D2B48C;
    color: black;
    padding: 8px;
}
.styled-table td {
    padding: 8px;
    border-bottom: 1px solid #ddd;
}
.styled-table tr:hover {
    background-color: #04665f;
}
</style>
""", unsafe_allow_html=True)


# Example data – replace with your actual dictionaries
words_dict = glyphdict.words_dict
modifiers_dict = modsdict.mod_dict
# ====================== APP LAYOUT ====================== #

st.title("Aeon Spell Caster")
st.image("magics.png", use_container_width=True)

# --- Sidebar Inputs ---
with st.sidebar:

    # ---- NEW VIEW-MODE CONTROL ----
    view_mode = st.radio(
        "View Mode",
        ["Spell Caster", "Glyph Dictionary"],
        index=0
    )
    st.sidebar.header("Controls")
    
    # Glyph selection
    glyph_list = st.sidebar.multiselect(
        "Select Glyphs",
        options=list(words_dict.keys()),
        default=list(words_dict.keys())
    )
    
    # Domain input (optional)
    domain_var = st.sidebar.text_input("Domain", "DefaultDomain")
    
    # Modifier selection
    mods_list = st.sidebar.multiselect(
        "Select Modifiers",
        options=list(modifiers_dict.keys()),
        default=[]
    )
    
    # Range increase
    range_inc = st.sidebar.number_input("Range Increase", min_value=0, value=0)
    
    # Range type
    range_type = st.sidebar.number_input("Range Type Change", min_value=0, value=0)
    
    # Quicken
    quicken_val = st.sidebar.number_input("Quicken", min_value=0, value=0)

if view_mode == "Glyph Dictionary":
    st.header("Glyph Dictionary")

    pdf_path = "Glyph_Dictionary(tobeupdated).pdf"

    st.subheader("Document Pages")

    render_pdf_as_images(pdf_path)

    st.stop()
    


# Apply button
if st.sidebar.button("Apply"):

    if not glyph_list:
        st.warning("Please select at least one glyph.")
    else:
        st.subheader("Orbital Figure and Table Output")

        # --- Generate figure and text ---
        fig, output_text, df= draw_atom_words_from_dict(
            words_list=glyph_list,
            words_dict=words_dict,
            modifiers_dict=modifiers_dict,
            modifiers_to_apply=mods_list,
            quicken=quicken_val,
            range_increase_input=range_inc,
            range_type_change=range_type
        )

        # --- Display figure ---
        st.pyplot(fig)

        # --- Display table/text output ---
        st.text_area("Output & Totals", value=output_text, height=300)
        st.write(df.to_html(classes="styled-table", index=False), unsafe_allow_html=True)

