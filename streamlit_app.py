
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors
import io
from streamlit_ketcher import st_ketcher
from PIL import Image

st.set_page_config(
	page_title="chemFORT: Molecular Design Suite",
	layout="wide",
	page_icon="🧪"  # Atom/chemistry emoji as favicon
)

st.markdown("""
# chemFORT: Molecular Design Suite
Welcome to **chemFORT**, your professional cheminformatics toolkit for molecular design and visualization.
""")

tabs = st.tabs(["SMILES Converter", "Molecule Sketcher"])

# --- Tab 1: SMILES to Structure ---
with tabs[0]:
	st.header("SMILES to Structure Converter")
	st.markdown("Enter a valid SMILES string to visualize the molecule and download its 2D structure as a PNG.")
	smiles = st.text_input("SMILES Input", placeholder="e.g. C1=CC=CC=C1 (Benzene)")
	mol = None
	img_bytes = None
	if smiles:
		try:
			mol = Chem.MolFromSmiles(smiles)
			if mol is None:
				raise ValueError("Invalid SMILES string.")
			img = Draw.MolToImage(mol, size=(350, 350), kekulize=True)
			buf = io.BytesIO()
			img.save(buf, format="PNG")
			img_bytes = buf.getvalue()
			st.image(img, caption="2D Structure", use_column_width=False)
			st.success("Molecule rendered successfully!")
		except Exception as e:
			st.error(f"Error: {str(e)}")
	if img_bytes:
		st.download_button(
			label="Download PNG",
			data=img_bytes,
			file_name="structure.png",
			mime="image/png"
		)

# --- Tab 2: Molecule Sketcher ---
with tabs[1]:
	st.header("Interactive Molecule Sketcher")
	st.markdown("Draw your molecule below. The canonical SMILES and basic properties will be displayed in real time.")
	molblock = st_ketcher(
		label="Draw Molecule",
		height=400,
		width=600,
		value=""
	)
	smiles_out = ""
	mol2 = None
	if molblock:
		try:
			mol2 = Chem.MolFromMolBlock(molblock)
			if mol2 is None:
				raise ValueError("Invalid molecule drawing.")
			smiles_out = Chem.MolToSmiles(mol2, canonical=True)
			st.success("Molecule parsed successfully!")
		except Exception as e:
			st.error(f"Error: {str(e)}")
	else:
		st.info("Draw a molecule to get started.")

	st.subheader("SMILES Output")
	st.code(smiles_out or "", language="txt")

	if mol2:
		mw = Descriptors.MolWt(mol2)
		formula = Chem.rdMolDescriptors.CalcMolFormula(mol2)
		st.markdown(f"**Molecular Weight:** {mw:.2f} g/mol")
		st.markdown(f"**Formula:** {formula}")

