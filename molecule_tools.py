import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors
import io
from streamlit_ketcher import st_ketcher
from PIL import Image

def smiles_converter_tab():
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
            st.image(img, caption="2D Structure", width=350)
            st.success("Molecule rendered successfully!")

            # 2D to 3D conversion option
            st.markdown("---")
            st.subheader("Convert to 3D Structure")
            if st.button("Generate 3D Structure (SDF) and Visualize"):
                try:
                    from rdkit.Chem import AllChem
                    import py3Dmol
                    mol3d = Chem.AddHs(mol)
                    AllChem.EmbedMolecule(mol3d, AllChem.ETKDG())
                    AllChem.UFFOptimizeMolecule(mol3d)
                    sdf_block = Chem.MolToMolBlock(mol3d)
                    st.success("3D structure generated!")
                    st.download_button(
                        label="Download 3D SDF",
                        data=sdf_block,
                        file_name="structure3d.sdf",
                        mime="chemical/x-mdl-sdfile"
                    )
                    # 3D visualization
                    st.markdown("**3D Structure Visualization:**")
                    view = py3Dmol.view(width=400, height=350)
                    view.addModel(sdf_block, 'sdf')
                    view.setStyle({'stick': {}})
                    view.setBackgroundColor('white')
                    view.zoomTo()
                    view_html = view._make_html()
                    st.components.v1.html(view_html, height=370, width=420)
                except Exception as e:
                    st.error(f"3D conversion or visualization failed: {str(e)}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    if img_bytes:
        st.download_button(
            label="Download PNG",
            data=img_bytes,
            file_name="structure.png",
            mime="image/png"
        )

def molecule_sketcher_tab():
    st.header("Interactive Molecule Sketcher")
    st.markdown("Draw your molecule below. The canonical SMILES and basic properties will be displayed in real time.")
    sketch_smiles = st_ketcher(
        height=400,
        value=""
    )
    smiles_out = ""
    mol2 = None
    if sketch_smiles:
        try:
            mol2 = Chem.MolFromSmiles(sketch_smiles)
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
        logp = Descriptors.MolLogP(mol2)
        st.markdown(f"**Molecular Weight:** {mw:.2f} g/mol")
        st.markdown(f"**Formula:** {formula}")
        st.markdown(f"**LogP:** {logp:.2f}")
