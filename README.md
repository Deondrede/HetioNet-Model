# HetioNet-Model
A model of HetioNet's biomedical knowledge network which consists of genes, compounds and diseases from a database.

+ `utils.py` initializes the and returns the database

+ `diseases-mongo.py` consists of the code necessary to read the code from the tsv files and establishes the collections

+ `query1.py` asks for a user given disease ID and returns its name, the drugs that can treat or palliate it, the genes that cause the diesase and where it occurs in a single query
