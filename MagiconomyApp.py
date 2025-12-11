import streamlit as st
import matplotlib.pyplot as plt
from atomwords import draw_atom_words_from_dict  # your plotting function
#from plotlyatomwordsWIP import draw_atom_words_from_dict
import glyphdict
words_dict = glyphdict.words_dict
import modsdict
mod_dict = modsdict.mod_dict
import pandas as pd
import base64
import os
from pdf2image import convert_from_path

#from plotly.tools import mpl_to_plotly
#import plotly.graph_objects as go


def render_pdf_as_images(pdf_path):
    """Convert each PDF page to an image and display it."""
    if not os.path.exists(pdf_path):
        st.error(f"PDF file not found: {pdf_path}")
        return

    # Convert pages to images
    pages = convert_from_path(pdf_path, dpi=150)

    # Display each page as an image
    for i, page in enumerate(pages):
        st.image(page, caption=f"Page {i+1}", use_container_width=True)
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


#Sidebar coloration and format
# ---- CUSTOM SIDEBAR STYLING ----

[theme]
primaryColor= "cyan"



# ====================== APP LAYOUT ====================== #

# -- Domain name → section conversion map --
domain_to_section = {
    "Ley": 6,
    "End": 1,
    "Death": 2,
    "Dark Shamanism": 3,
    "Shamanism": 4,
    "Druidism": 5,
}


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
    # --- Glyph selection (unfiltered) ---
    all_glyphs = list(words_dict.keys())

    # --- Domain dropdown ---
    chosen_domain = st.selectbox(
        "Domain (Filter Glyphs):",
        options=list(domain_to_section.keys()),
        index=0  # "All Domains"
    )

    # Convert domain → section number
    selected_section = domain_to_section[chosen_domain]

    # --- Filter glyphs based on domain ---
    if selected_section is None:
        filtered_glyphs = all_glyphs
    else:
        filtered_glyphs = [
            w for w in all_glyphs
            if words_dict[w]["section"] == selected_section
        ]

    # --- Display filtered list ---
    glyph_list = st.multiselect(
        "Select Glyphs",
        options=filtered_glyphs,
        default=[]
    )

    # --- Optional feedback message ---
    if chosen_domain != "All Domains" and len(filtered_glyphs) == 0:
        st.warning(f"No glyphs found in **{chosen_domain}** domain.")
    
    
    # Modifier selection
    mods_list = st.sidebar.multiselect(
        "Select Modifiers",
        options=list(mod_dict.keys()),
        default=[]
    )
    
    # Range increase
    range_inc = st.sidebar.number_input("Range Increase", min_value=0, value=0)
    
    # Range type
    range_type = st.sidebar.number_input("Range Type Change", min_value=0, value=0)
    
    # Quicken
    quicken_val = st.sidebar.number_input("Quicken", min_value=0, value=0)

if view_mode == "Spell Caster":
    st.title("Aeon Spell Caster (Tips Below)")
    st.image("magics.png", use_container_width=True)
    # Add text below the image
    st.subheader("Tips/Instructions")
    st.write("**Spell Caster View Mode:** This is where you can use the spell caster calculator.")
    st.write("Choose a **Domain** to pick your Glyphs from")
    st.write("You can pick the glyphs in **Select Glyphs** box")
    st.write("**Select Modifiers:** lets you choose the modifiers as shown in the Glyph Dictionary View Mode Modifiers section.")
    st.write("**Range Increase:** Type the number equivalent to how many more multiples of the range you want to increase by. Ex.) if its a default of 10ft inputing a 1 will change the range to 20ft, 2 will change the range to 30 ft and so on.")
    st.write("**Range Type Change:** Type the number equivalent to how many stages up you want to go along this list—Point(channeled) → Beam → Cone → Radial. Ex.) if by default it is a beam you would type 2 to change it to radial or 1 to change it to cone.")
    st.write("**Quicken:** Type the amount of AP you want to take away from the current AP cost. Ex.) typing 2 for a default 4 AP/ 2Charge cast will result in a 2AP/8Charge cost")
    st.write("")
    st.write("**Glyph Dictionary View Mode:** This is where you can learn how the values are calculated and how you can write your own spells! This also shows you the Glyph dictionary with more elaborate descriptions and details.")
    
    
    
  


if view_mode == "Glyph Dictionary":

    pdf_path = "Glyph_Dictionary(tobeupdated).pdf"

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
        # --- Convert Matplotlib fig to Plotly ---
        #plotly_fig = mpl_to_plotly(fig)

        # --- Display interactive Plotly figure in Streamlit ---
        #st.plotly_chart(plotly_fig, use_container_width=True)

        

        # --- Display table/text output ---
        st.text_area("Output & Totals", value=output_text, height=300)
        st.write(df.to_html(classes="styled-table", index=False), unsafe_allow_html=True)

