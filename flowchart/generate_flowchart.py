import os
from graphviz import Digraph

# Ensure the Graphviz executable is in the PATH
os.environ["PATH"] += r";C:\Program Files\Graphviz\bin"

# Define output directory and ensure it exists
output_dir = 'flowchart'
os.makedirs(output_dir, exist_ok=True)

# Initialize the Digraph object
dot = Digraph(comment='Multi-Agent Workflow for AI Use Cases')

# Add nodes for each component in the architecture
dot.node('A', 'User Input (Company & Industry)')
dot.node('B', 'Market Research Findings')
dot.node('C', 'Proposed Use Cases')
dot.node('D', 'Resource Links')
dot.node('E', 'Download CSV')
dot.node('F', 'Display Results (Streamlit)')

# Add edges to define the workflow
dot.edge('A', 'B', 'User Input sent to Research Agent')
dot.edge('B', 'C', 'Research Findings provided')
dot.edge('C', 'D', 'Proposed Use Cases generated')
dot.edge('D', 'E', 'Resource Links provided')
dot.edge('E', 'F', 'CSV file downloaded and results displayed')

# Save the architecture as an image in PNG format
output_path = os.path.join(output_dir, 'architecture')
dot.render(output_path, format='png')  # Saves as architecture.png
print(f"Flowchart saved to {output_path}.png")