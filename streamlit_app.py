

import streamlit as st
from molecule_tools import smiles_converter_tab, molecule_sketcher_tab

st.set_page_config(
    page_title="chemFORT",
    layout="wide",
    page_icon="🧪"  # Atom/chemistry emoji as favicon
)

st.markdown("""
# chemFORT: Molecular Design Suite
Welcome to **chemFORT**, your professional cheminformatics toolkit.
""")

tabs = st.tabs(["SMILES Converter", "Molecule Sketcher"])

with tabs[0]:
    smiles_converter_tab()

with tabs[1]:
    molecule_sketcher_tab()

