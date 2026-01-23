import streamlit as st
import streamlit.components.v1 as components
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
# --- Session state initialization ---
if "selected_glyphs" not in st.session_state:
    st.session_state["selected_glyphs"] = []

if "active_glyph" not in st.session_state:
    st.session_state["active_glyph"] = None

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




# ====================== APP LAYOUT ====================== #

# -- Domain name → section conversion map --
domain_to_section = {
    "All": set(range(1, 7)),
    "Ley": 6,
    "End": 1,
    "Death": 2,
    "Witchcraft": 3,
    "Shamanism": 4,
    "Druidism": 5,
}

Book_list = {"All Books":set(range(1, 5)),"Book of Glyphs (Standard)":1,"Book of Scrolls":2, "Carnecarta":3, "Book of Phlegmancy":4}
# Mapping for range and range type
range_dict = {1: "self", 2: "touch", 5: "5 ft", 10: "10 ft", 15: "15 ft", 20: "20 ft", 25: "25 ft", 30: "30 ft", 35: "35 ft", 40: "40 ft",45: "45 ft", 50: "50 ft", 55: "55 ft", 60: "60 ft", 100: "100 ft", 120: "120 ft", 150: "150 ft", 200: "200 ft", 250: "250 ft", 300: "300 ft", 350: "350 ft", 400: "400 ft", 450: "450 ft", 500: "500 ft" }
rt_dict = {1: "self", 2: "touch", 3: "point", 4: "beam", 5: "cone", 6: "radial"}

# --- Sidebar Inputs ---
with st.sidebar:

    # ---- NEW VIEW-MODE CONTROL ----
    view_mode = st.radio(
        "View Mode",
        ["Spell Caster", "Glyph Dictionary"],
        index=0
    )
    st.sidebar.header("Controls")
    
    with st.sidebar:

        view_mode = st.radio(
        "View Mode",
        ["Spell Caster", "Glyph Dictionary"],
        index=0,
        key="view_mode_radio")

        st.sidebar.header("Controls")
    
        all_glyphs = list(words_dict.keys())
    
        # --- Book filter ---
        selected_book_ids = set()

        for book_name in chosen_books:
            value = Book_list.get(book_name)
            if isinstance(value, set):
                selected_book_ids |= value
            else:
                selected_book_ids.add(value)

        if "All Books" in chosen_books or not chosen_books:
            filtered_glyphs = all_glyphs
        else:
            filtered_glyphs = [
                g for g in all_glyphs
                if words_dict[g].get("book") in selected_book_ids
            ]


        chosen_books = st.multiselect(
            "Books (Filter Glyphs):",
            options=list(Book_list),
            default=["All Books"]
        )
    
        # --- Domain filter ---
        chosen_domain = st.selectbox(
            "Domain (Filter Glyphs):",
            options=list(domain_to_section.keys()),
            index=0
        )
    
        selected_section = domain_to_section[chosen_domain]
    
        # --- Normalize filters ---
        allowed_books = None if "All Books" in chosen_books or not chosen_books else set(chosen_books)
    
        if chosen_domain == "All":
            allowed_sections = None
        elif isinstance(selected_section, set):
            allowed_sections = set(selected_section)
        else:
            allowed_sections = {selected_section}
    
        # --- Intersection filter ---
        filtered_glyphs = []
        for g in all_glyphs:
            info = words_dict[g]
    
            if allowed_books is not None and info.get("book") not in allowed_books:
                continue
    
            if allowed_sections is not None and info.get("section") not in allowed_sections:
                continue
    
            filtered_glyphs.append(g)
    
        # --- Preserve selected glyphs ---
        display_options = sorted(
            set(filtered_glyphs) | set(st.session_state["selected_glyphs"])
        )
    
        # --- Glyph selector ---
        previous = set(st.session_state["selected_glyphs"])
    
        glyph_list = st.multiselect(
            "Select Glyphs",
            options=display_options,
            default=st.session_state["selected_glyphs"]
        )
    
        current = set(glyph_list)
    
        newly_selected = list(current - previous)
        if newly_selected:
            st.session_state["active_glyph"] = newly_selected[-1]
    
        st.session_state["selected_glyphs"] = glyph_list


    #---
    st.markdown("---")
    st.subheader("Most Recently Selected Glyph Details")
    
    active = st.session_state.get("active_glyph")
    
    if active:
        data = words_dict.get(active, {})
    
        # Decode values
        raw_range = data.get("range")
        raw_range_type = data.get("rt")
    
        range_text = range_dict.get(raw_range, "None")
        range_type_text = rt_dict.get(raw_range_type, "None")
    
        st.markdown(f"**Glyph:** {active}")
        st.markdown(f"**Range:** {range_text}")
        st.markdown(f"**Range Type:** {range_type_text}")
        st.markdown(f"**Comment:** {data.get('comment', '—')}")
    else:
        st.caption("Select a glyph to view details.")
    st.markdown("---")





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
    st.title("Aeon Spell Caster")
    # st.image("magics.png", use_container_width=True)
    # Add text below the image
    st.subheader("Tips/Instructions")
    st.write("**Glyph Dictionary View Mode:** This is where you can learn how the values are calculated and how you can write your own spells! This also shows you the Glyph dictionary with more elaborate descriptions and details.")
    st.write("**Spell Caster View Mode:** This is where you can use the spell caster calculator.")
    st.write("Choose a **Domain** to pick your Glyphs from. (These are the Main Magic Groups for which you want to get the bonuses to your spells from. For example, Ley, End, Druidism, etc.)")
    st.write("You can pick the glyphs in **Select Glyphs** box. Selecting a Glyph will show you more details below it about the range, range type, and general effects. (you may have to select it twice for it to stay)")
    st.write("**Select Modifiers:** lets you choose the modifiers as shown in the Glyph Dictionary View Mode Modifiers section. These are additions to your spell that only work for certain glyphs converting the effects of some glyphs to do damage or throw objects, for example. ")
    st.write("**Range Increase:** Type the number equivalent to how many more multiples of the range you want to increase by. Ex.) if its a default of 10ft inputing a 1 will change the range to 20ft, 2 will change the range to 30 ft and so on. **NOT APPLICABLE TO GLYPHS WITH SELF OR TOUCH RANGE TYPES**")
    st.write("**Range Type Change:** Type the number equivalent to how many stages up you want to go along this list—Point(channeled) → Beam → Cone → Radial. Ex.) if by default it is a beam you would type 2 to change it to radial or 1 to change it to cone. **NOT APPLICABLE TO GLYPHS WITH SELF OR TOUCH RANGE TYPES**")
    st.write("**Quicken:** Type the amount of AP you want to take away from the current AP cost. Ex.) typing 2 for a default 4 AP/ 2Charge cast will result in a 2AP/8Charge cost")
    st.write("")
    st.write("**ONCE YOU HIT APPLY YOUR SPELL WILL APPEAR BELOW HERE**")
    
    
  


if view_mode == "Glyph Dictionary": 
    pdf_path = "Glyph_Dictionary(tobeupdated).pdf" 
    render_pdf_as_images(pdf_path) 
    st.stop()

# Apply button
if st.sidebar.button("Apply"):

    if not glyph_list:
        st.warning("Please select at least one glyph.")
    else:
        st.subheader("Spell Hex Map and Table Output")

        # --- Generate figure and text ---
        fig, output_text, df= draw_atom_words_from_dict(
            words_list=glyph_list,
            words_dict=words_dict,
            modifiers_dict=mod_dict,
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
        st.text_area("**Total Cost and Modifiers**", value=output_text, height=300)
        st.write("")
        st.write("**Glyph functions (comments) and individual cost values**")
        st.write(df.to_html(classes="styled-table", index=False), unsafe_allow_html=True)

