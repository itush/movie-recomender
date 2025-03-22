import nbformat
from nbformat.v4 import new_notebook

# Create a new notebook
nb = new_notebook()

# Write the notebook to a file
with open("notebooks/data_exploration.ipynb", "w") as f:
    nbformat.write(nb, f)

print("Jupyter Notebook 'notebooks/data_exploration.ipynb' created successfully.")
