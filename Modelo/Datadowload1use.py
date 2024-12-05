import pandas as pd
from Bio import SeqIO, Entrez

#importamos datos de NCBI con entrez

Entrez.email = 'jahacieljunior@gmail.com'

filtrosagro = '"Agrobacterium"[Organism] AND cds[Feature] NOT rRNA[Feature] NOT tRNA[Feature] AND 1:10000[SLEN]'
filtroshuman = '"Homo sapiens"[Organism] AND RefSeqGene[Keyword] AND 1:50000[SLEN]'
filtroecoli = '"Escherichia coli"[Organism] AND cds[Feature] NOT rRNA[Feature] NOT tRNA[Feature] AND 00000000001[SLEN] : 00000010000[SLEN]'
handle = Entrez.esearch(db="nucleotide", term=filtroecoli, retmax=500)
record = Entrez.read(handle)
ids = record["IdList"]

print(f"Se encontraron {len(ids)} secuencias")

fasta_handle = Entrez.efetch(db="nucleotide", id=ids, rettype="fasta", retmode="text")
fasta_data = fasta_handle.read()

with open('fastaEcoli.fasta', 'w') as agr:
    agr.write(fasta_data)


