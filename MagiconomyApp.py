import streamlit as st
import matplotlib.pyplot as plt
from atomwords import draw_atom_words_from_dict  # your plotting function
import glyphdict
import modsdict
import pandas as pd

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
    background-color: #4CAF50;
    color: white;
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

# --- Sidebar Inputs ---
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

