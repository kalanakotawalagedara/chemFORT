# 1. Write the main app file
%%writefile app.py
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw

st.title("Molecule Sketcher Deployment")
smiles = st.text_input("Enter SMILES:", "c1ccccc1")
if smiles:
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        st.image(Draw.MolToImage(mol))

# 2. Write the requirements file (CRITICAL for Streamlit Cloud)
%%writefile requirements.txt
streamlit
rdkit

