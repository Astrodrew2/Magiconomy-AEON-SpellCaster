import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from atomwords import draw_atom_words_from_dict
import glyphdict
import modsdict
import pandas as pd
import base64
import os
from pdf2image import convert_from_path

words_dict = glyphdict.words_dict
mod_dict = modsdict.mod_dict

# --- Session state initialization ---
if "selected_glyphs" not in st.session_state:
    st.session_state["selected_glyphs"] = []

if "spell_applied" not in st.session_state:
    st.session_state["spell_applied"] = False

def render_pdf_as_images(pdf_path):
    """Convert each PDF page to an image and display it."""
    if not os.path.exists(pdf_path):
        st.error(f"PDF file not found: {pdf_path}")
        return

    pages = convert_from_path(pdf_path, dpi=150)
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
.control-box {
    padding: 1.5rem;
    border: 2px solid #D2B48C;
    border-radius: 8px;
    background-color: #f9f7f4;
    margin-bottom: 1rem;
}
label {
    white-space: nowrap !important;
}
h2, h3, h4, h5, h6 {
    white-space: nowrap !important;
}
textarea {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ====================== APP HEADER ====================== #
col1, col2 = st.columns([5, 1])
with col1:
    st.title("Aeon Spell Caster")
with col2:
    show_tips = st.button("ℹ️ Tips", use_container_width=True)

# ====================== VIEW MODE SELECTOR ====================== #
view_mode = st.radio(
    "View Mode",
    ["Spell Caster", "Glyph Dictionary"],
    index=0,
    horizontal=True
)

# ====================== TIPS SECTION ====================== #
if show_tips:
    with st.expander("Instructions & Tips", expanded=True):
        st.markdown("""
### How to Use This Spell Caster:

**View Modes:**
- **Spell Caster:** Create and visualize spells with custom parameters
- **Glyph Dictionary:** Browse the complete Magiconomy book and glyph reference guide

**Filtering Glyphs:**
- **Books:** Select which spell books you have access to
- **Domain:** Choose a magical domain (Ley, End, Druidism, etc.)
- **Mastery:** Filter by your skill level (Novice, Skilled, Master)

**Creating Spells:**
1. Select glyphs from the "Glyph Selection" box
2. Choose modifiers to enhance your spell effects
3. Adjust Range Increase, Range Type, and Quicken as needed
4. Click **APPLY** to generate your spell visualization and cost summary

**Parameters:**
- **Range Increase:** Multiplies the range (e.g., 1 = 2x range, 2 = 3x range)
- **Range Type Change:** Upgrades range type (Point → Beam → Cone → Radial)
- **Quicken:** Reduces AP cost at the expense of energy
        """)

# ====================== GLYPH DICTIONARY VIEW ====================== #
if view_mode == "Glyph Dictionary": 
    pdf_path = "Glyph_Dictionary(tobeupdated).pdf" 
    render_pdf_as_images(pdf_path)
    st.stop()

# ====================== SPELL CASTER VIEW ====================== #
# Setup domain and book mappings
domain_to_section = {
    "All": set(range(1, 7)),
    "Ley": 6,
    "End": 1,
    "Death": 2,
    "Witchcraft": 3,
    "Shamanism": 4,
    "Druidism": 5,
}

Book_list = {
    "All Books": set(range(1, 5)),
    "Book of Glyphs (Standard)": 1,
    "Book of Scrolls (WIP)": 2,
    "Carnecarta (WIP)": 3,
    "Book of Phlegmancy (WIP)": 4
}

range_dict = {
    1: "self", 2: "touch", 5: "5 ft", 10: "10 ft", 15: "15 ft", 20: "20 ft",
    25: "25 ft", 30: "30 ft", 35: "35 ft", 40: "40 ft", 45: "45 ft", 50: "50 ft",
    55: "55 ft", 60: "60 ft", 100: "100 ft", 120: "120 ft", 150: "150 ft",
    200: "200 ft", 250: "250 ft", 300: "300 ft", 350: "350 ft", 400: "400 ft",
    450: "450 ft", 500: "500 ft"
}

rt_dict = {1: "self", 2: "touch", 3: "point", 4: "beam", 5: "cone", 6: "radial"}
all_glyphs = list(words_dict.keys())

# ====================== CONTROL PANELS ====================== #
st.markdown("### Spell Configuration")

# Top row: Filters
filter_col1, filter_col2, filter_col3 = st.columns(3, gap="medium")

with filter_col1:
    st.markdown("**Books**")
    chosen_books = st.multiselect(
        "Books (Filter Glyphs):",
        options=list(Book_list.keys()),
        default=["All Books"],
        key="book_filter",
        label_visibility="collapsed"
    )

with filter_col2:
    st.markdown("**Domain**")
    chosen_domain = st.selectbox(
        "Domain (Filter Glyphs):",
        options=list(domain_to_section.keys()),
        index=0,
        key="domain_filter",
        label_visibility="collapsed"
    )

with filter_col3:
    st.markdown("**Mastery**")
    mastery_cols = st.columns(3)
    with mastery_cols[0]:
        novice_on = st.checkbox("Novice", value=True, key="mastery_novice")
    with mastery_cols[1]:
        skilled_on = st.checkbox("Skilled", value=True, key="mastery_adept")
    with mastery_cols[2]:
        master_on = st.checkbox("Master", value=True, key="mastery_master")

# Process filters
selected_book_ids = set()
for book in chosen_books:
    val = Book_list.get(book)
    if isinstance(val, set):
        selected_book_ids |= val
    else:
        selected_book_ids.add(val)

selected_section = domain_to_section[chosen_domain]
selected_mastery = set()
if novice_on:
    selected_mastery.add("Novice")
if skilled_on:
    selected_mastery.add("Adept")
if master_on:
    selected_mastery.add("Master")

# Filter glyphs
filtered_glyphs = []
for g in all_glyphs:
    glyph = words_dict[g]
    book_ok = "All Books" in chosen_books or glyph.get("book") in selected_book_ids
    
    if chosen_domain == "All":
        domain_ok = True
    elif isinstance(selected_section, (set, list)):
        domain_ok = glyph.get("section") in selected_section
    else:
        domain_ok = glyph.get("section") == selected_section

    mastery_ok = not selected_mastery or glyph.get("mastery") in selected_mastery

    if book_ok and domain_ok and mastery_ok:
        filtered_glyphs.append(g)

display_options = sorted(set(filtered_glyphs) | set(st.session_state.get("selected_glyphs", [])))

# Second row: Glyph selection and modifiers
glyph_col, modifier_col = st.columns([2, 1], gap="medium")

with glyph_col:
    st.markdown("**Select Glyphs**")
    glyph_list = st.multiselect(
        "Select Glyphs",
        options=display_options,
        default=st.session_state.get("selected_glyphs", []),
        key="glyph_selector",
        label_visibility="collapsed"
    )

with modifier_col:
    st.markdown("**Modifiers**")
    mods_list = st.multiselect(
        "Select Modifiers",
        options=list(mod_dict.keys()),
        default=[],
        label_visibility="collapsed"
    )

# Update selected glyphs and reset spell_applied flag if glyphs changed
if set(glyph_list) != set(st.session_state.get("selected_glyphs", [])):
    st.session_state["spell_applied"] = False
st.session_state["selected_glyphs"] = glyph_list

# Third row: Spell parameters
st.markdown("**Spell Parameters**")
param_col1, param_col2, param_col3, param_col4 = st.columns(4, gap="medium")

with param_col1:
    range_inc = st.number_input("Range Increase", min_value=0, value=0, label_visibility="visible")

with param_col2:
    range_type = st.number_input("Range Type Change", min_value=0, value=0, label_visibility="visible")

with param_col3:
    quicken_val = st.number_input("Quicken", min_value=0, value=0, label_visibility="visible")

with param_col4:
    apply_button = st.button("✨ APPLY", use_container_width=True, type="primary")

# ====================== GLYPH DETAILS PANEL ====================== #
if not st.session_state.get("spell_applied", False):
    st.markdown("---")

    detail_col, empty_col = st.columns([12, 3])

    with detail_col:
        st.markdown("**📋 Selected Glyphs**")
        
        if glyph_list:
            # Create columns for each glyph (max 4 per row)
            cols_per_row = 4
            for i in range(0, len(glyph_list), cols_per_row):
                cols = st.columns(min(cols_per_row, len(glyph_list) - i))
                for j, col in enumerate(cols):
                    if i + j < len(glyph_list):
                        glyph_name = glyph_list[i + j]
                        data = words_dict.get(glyph_name, {})
                        raw_range = data.get("range")
                        raw_range_type = data.get("rt")
                        ap = data.get("AP")
                        charge = data.get("level")
                        
                        range_text = range_dict.get(raw_range, "None")
                        range_type_text = rt_dict.get(raw_range_type, "None")
                        
                        with col:
                            with st.container(border=True):
                                st.markdown(f"**{glyph_name}**")
                                st.write(f"Charges: {charge}")
                                st.write(f"AP: {ap}")
                                st.write(f"Range: {range_text}")
                                st.write(f"Range Type: {range_type_text}")
                                st.caption(f"Effects: *{data.get('comment', '—')}*")
        else:
            st.info("Select glyphs to view details")

# ====================== SPELL GENERATION ====================== #
if apply_button:
    st.session_state["spell_applied"] = True
    if not glyph_list:
        st.warning("Please select at least one glyph.")
    else:
        st.markdown("---")
        st.markdown("## ✨ Spell Visualization")
        
        # Generate spell
        fig, output_text, df = draw_atom_words_from_dict(
            words_list=glyph_list,
            words_dict=words_dict,
            modifiers_dict=mod_dict,
            modifiers_to_apply=mods_list,
            quicken=quicken_val,
            range_increase_input=range_inc,
            range_type_change=range_type
        )
        
        # Display cost summary and visualization side by side
        summary_col, viz_col = st.columns([1, 1.5], gap="medium")
        
        with summary_col:
            st.markdown("### 📊 Cost Summary")
            
            # Split output into main summary and extras
            if "---EXTRAS---" in output_text:
                main_summary, extras_section = output_text.split("---EXTRAS---", 1)
            else:
                main_summary = output_text
                extras_section = ""
            
            # Display main cost summary
            with st.container(border=True):
                lines = main_summary.strip().split('\n')
                for line in lines:
                    if line.strip():
                        st.write(line)
            
            # Display extras section if it exists
            if extras_section.strip():
                st.markdown("#### Extras")
                with st.container(border=True):
                    lines = extras_section.strip().split('\n')
                    for line in lines:
                        if line.strip():
                            st.write(line)
        
        with viz_col:
            st.pyplot(fig)
        
        st.markdown("---")
        
        # Display detailed breakdown below
        st.markdown("### 📋 Detailed Breakdown")
        st.write(df.to_html(classes="styled-table", index=False), unsafe_allow_html=True)
