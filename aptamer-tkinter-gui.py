import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import random
from Bio.SeqUtils import gc_fraction

def generate_aptamer(length=40, gc_target=0.5, tolerance=0.05):
    bases = ["A", "T", "G", "C"]
    sequence = ''.join(random.choices(bases, k=length))
    while abs(gc_fraction(sequence) - gc_target) > tolerance:
        sequence = ''.join(random.choices(bases, k=length))
    return sequence

def generate_aptamers_for_protein(protein_sequence, num_aptamers=15, min_length=20, max_length=80, gc_target=0.5):
    aptamer_candidates = []

    for _ in range(num_aptamers):
        length = random.randint(min_length, max_length)
        aptamer_seq = generate_aptamer(length, gc_target)
        gc_content = gc_fraction(aptamer_seq) * 100
        aptamer_candidates.append({
            "sequence": aptamer_seq,
            "gc_content": gc_content
        })

    return sorted(aptamer_candidates, key=lambda x: x['gc_content'], reverse=True)

def generate_aptamers():
    protein_sequence = protein_entry.get("1.0", tk.END).strip()
    
    if not protein_sequence:
        messagebox.showerror("Error", "Please enter a protein sequence")
        return
    
    try:
        aptamer_results = generate_aptamers_for_protein(protein_sequence)
        
        # Clear previous results
        for i in tree.get_children():
            tree.delete(i)
        
        # Display results in treeview
        for idx, aptamer in enumerate(aptamer_results, 1):
            tree.insert("", "end", values=(idx, aptamer['sequence'], f"{aptamer['gc_content']:.2f}%"))
    
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create main window with modern style
root = tk.Tk()
root.title("Aptamer Generator")
root.geometry("700x600")
root.configure(bg='#f0f0f0')

# Style configuration
style = ttk.Style()
style.theme_use('clam')  # Modern theme
style.configure("TLabel", background='#f0f0f0', font=('Arial', 10))
style.configure("TButton", font=('Arial', 10))
style.configure("Treeview", 
    background="#f0f0f0",
    foreground="black",
    rowheight=25,
    fieldbackground="#f0f0f0"
)
style.map('Treeview', 
    background=[('selected', '#4a6984')],
    foreground=[('selected', 'white')]
)

# Protein Sequence Input Frame
input_frame = ttk.Frame(root)
input_frame.pack(padx=10, pady=10, fill='x')

input_label = ttk.Label(input_frame, text="Enter Protein Sequence:")
input_label.pack(side='top', anchor='w')

protein_entry = scrolledtext.ScrolledText(input_frame, height=6, width=80, 
    font=('Courier', 10), wrap=tk.WORD)
protein_entry.pack(fill='x')

# Generate Button
generate_button = ttk.Button(input_frame, text="Generate Aptamers", command=generate_aptamers)
generate_button.pack(pady=5)

# Results Treeview
results_label = ttk.Label(root, text="Generated Aptamers:", font=('Arial', 12, 'bold'))
results_label.pack(padx=10, anchor='w')

tree = ttk.Treeview(root, columns=('Number', 'Sequence', 'GC Content'), show='headings')
tree.heading('Number', text='No.')
tree.heading('Sequence', text='Aptamer Sequence')
tree.heading('GC Content', text='GC Content')
tree.column('Number', width=50, anchor='center')
tree.column('Sequence', width=400)
tree.column('GC Content', width=100, anchor='center')
tree.pack(padx=10, fill='both', expand=True)

# Scrollbar for Treeview
scrollbar = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side='right', fill='y')

root.mainloop()
