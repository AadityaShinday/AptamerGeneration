import random
import streamlit as st
from Bio.SeqUtils import gc_fraction

# Function to generate a single aptamer sequence
def generate_aptamer(length=40, gc_target=0.5, tolerance=0.05):
    bases = ["A", "T", "G", "C"]
    sequence = ''.join(random.choices(bases, k=length))
    while abs(gc_fraction(sequence) - gc_target) > tolerance:
        sequence = ''.join(random.choices(bases, k=length))
    return sequence

# Function to generate multiple aptamers for a given protein
def generate_aptamers_for_protein(protein_sequence, num_aptamers=15, min_length=20, max_length=40):
    aptamers = []
    for _ in range(num_aptamers):
        length = random.randint(min_length, max_length)
        aptamer = generate_aptamer(length=length, gc_target=0.5, tolerance=0.05)
        aptamers.append(aptamer)
    return aptamers

# Streamlit GUI
st.title("Aptamer Generator")

# Inputs
protein_sequence = st.text_area("Enter Protein Sequence", value="", height=100)
num_aptamers = st.number_input("Number of Aptamers", min_value=1, max_value=100, value=15, step=1)
min_length = st.number_input("Minimum Length of Aptamer", min_value=10, max_value=100, value=20, step=1)
max_length = st.number_input("Maximum Length of Aptamer", min_value=10, max_value=100, value=40, step=1)

# Generate Aptamers
if st.button("Generate Aptamers"):
    if protein_sequence:
        aptamers = generate_aptamers_for_protein(protein_sequence, num_aptamers, min_length, max_length)
        st.success(f"Generated {len(aptamers)} Aptamers!")
        for i, aptamer in enumerate(aptamers, 1):
            st.text(f"Aptamer {i}: {aptamer}")
    else:
        st.error("Please enter a valid protein sequence.")

