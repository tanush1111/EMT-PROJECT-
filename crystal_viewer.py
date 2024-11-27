import streamlit as st
from pymatgen.core import Structure
from pymatgen.ext.matproj import MPRester
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

API_KEY = "kt5VIRCG30P6LyJHuJTg0nBBzeunZt7i"

st.set_page_config(
    page_title="3D Crystal Structure Viewer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    h1 {
        color: #4CAF50;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .stSidebar {
        background: linear-gradient(to top, #006d77, #83c5be);
        color: white;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        font-size: 16px;
        padding: 10px 20px;
        border: none;
        cursor: pointer;
    }
    .stTextInput input {
        background-color: #222;
        color: white;
        border: 1px solid #4CAF50;
    }
    .stTextInput label {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("✨ 3D Crystal Structure Viewer")
st.markdown(
    """
    Visualize crystal structures in 3D and explore material properties with ease!  
    """
)

st.sidebar.header("🔍 Input")
st.sidebar.markdown("Enter the Material ID below to visualize its crystal structure.")
material_id = st.sidebar.text_input(
    "Enter Material ID (e.g., mp-66 for Silicon)", value="mp-1227340", key="material_input"
)

material_list = [
    "mp-53: Graphene",
    "mp-66: Silicon",
    "mp-1234: Silicon Carbide (SiC)",
    "mp-12729: Lithium Cobalt Oxide (LiCoO2)",
    "mp-1285: Barium Titanate (BaTiO3)",
    "mp-149: Aluminum Oxide (Al2O3)",
    "mp-256: Copper (Cu)",
    "mp-100: Graphite (C)"
]

st.sidebar.subheader("🔎 Available Materials")
for material in material_list:
    st.sidebar.markdown(f"- {material}")

with MPRester(API_KEY) as m:
    try:
        structure = m.get_structure_by_material_id(material_id)
        st.sidebar.success("✅ Material fetched successfully!")
    except Exception as e:
        st.sidebar.error(f"❌ Error fetching material: {e}")
        st.stop()

st.header(f"🔬 Properties of Material: *{material_id}*")
st.write(f"📋 Formula**: {structure.formula}")
st.write(f"📐 Lattice Parameters (a, b, c): {structure.lattice.abc}")
st.write(f"📏 Lattice Angles (α, β, γ): {structure.lattice.angles}")
st.write(f"🏛 Space Group**: {structure.get_space_group_info()}")
st.write(f"🧪 Composition**: {structure.composition}")

def plot_3d_structure(structure):
    atoms = structure.cart_coords
    species = structure.species
    fig = go.Figure()

    color_map = {'C': 'red', 'O': 'blue', 'Si': 'green', 'H': 'yellow'}
    
    for i, atom in enumerate(atoms):
        fig.add_trace(go.Scatter3d(
            x=[atom[0]], y=[atom[1]], z=[atom[2]],
            mode='markers+text',
            marker=dict(size=10, color=color_map.get(str(species[i]), 'gray'), opacity=0.8),
            text=str(species[i]),
            textposition="top center"
        ))

    lattice = structure.lattice.matrix
    for i in range(3):
        for j in range(3):
            start = lattice[i]
            end = lattice[j]
            fig.add_trace(go.Scatter3d(
                x=[start[0], end[0]], y=[start[1], end[1]], z=[start[2], end[2]],
                mode='lines',
                line=dict(color='blue', width=2)
            ))

    fig.update_layout(
        scene=dict(
            xaxis_title="X-Axis",
            yaxis_title="Y-Axis",
            zaxis_title="Z-Axis",
            xaxis=dict(showbackground=True, backgroundcolor="rgb(240,240,240)"),
            yaxis=dict(showbackground=True, backgroundcolor="rgb(240,240,240)"),
            zaxis=dict(showbackground=True, backgroundcolor="rgb(240,240,240)"),
            aspectmode='data'
        ),
        title="3D Crystal Structure",
        title_font=dict(size=20, color="#4CAF50"),
        margin=dict(l=0, r=0, b=0, t=30),
    )
    return fig

st.subheader("📊 3D Visualization")
st.plotly_chart(plot_3d_structure(structure), use_container_width=True)

st.subheader("🖼 2D Lattice Projection")
fig, ax = plt.subplots(figsize=(8, 6))
colors = {'C': 'red', 'O': 'blue', 'Si': 'green', 'H': 'yellow'}
for site in structure.sites:
    x, y, z = site.frac_coords
    ax.scatter(x, y, s=100, label=str(site.specie), alpha=0.7, edgecolor='black', color=colors.get(str(site.specie), 'gray'))

ax.set_title("2D Lattice Projection", fontsize=16, color="#4CAF50")
ax.set_xlabel("Fractional Coordinate X", fontsize=14)
ax.set_ylabel("Fractional Coordinate Y", fontsize=14)
ax.grid(color="lightgray", linestyle="--", linewidth=0.5)
ax.legend(fontsize=10, loc="upper right", bbox_to_anchor=(1.4, 1.0))
st.pyplot(fig)