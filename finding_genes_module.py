import pandas as pd
import numpy as np

def finding_overlapping_genes(SGD_database, gene,gene_start,gene_end,gene_chromosome):
    overlapping_genes_temp = SGD_database.loc[(SGD_database['Chromosome'] == gene_chromosome) & (((SGD_database['Start'] <= gene_start) & (SGD_database['End'] >= gene_start)) |\
                                    ((SGD_database['End'] >= gene_end) & (SGD_database['Start'] <= gene_end)) |\
                                    ((SGD_database['Start'] >= gene_start) & (SGD_database['End'] <= gene_end))|\
                                    (SGD_database['Start'] <= gene_start) & (SGD_database['End'] >= gene_end)) & (SGD_database['Systematic Name'] != gene)].reset_index()
    overlapping_genes_temp['Direction'] = "NaN"
    overlapping_genes = overlapping_genes_temp[['Systematic Name', 'Standard Name','Description','Direction']].copy() 
    overlapping_genes.insert(0, "Searched gene", gene)
    overlapping_genes.insert(1, "Method", "Overlapping")
    return overlapping_genes
    

def info_genes(SGD_database, gene, column):
    #getting the information about the wanted gene - start, end and which chromosome
    gene_start = SGD_database[SGD_database[column] == gene]["Start"].values[0]
    gene_end = SGD_database[SGD_database[column] == gene]["End"].values[0]
    gene_chromosome = SGD_database[SGD_database[column] == gene]["Chromosome"].values[0]
    return gene_start, gene_end, gene_chromosome
    
    
def list_of_nearest_genes(SGD_database, gene,gene_start,gene_end,gene_chromosome):   
    SGD_database['upstream'] = np.where(((SGD_database['Chromosome'] == gene_chromosome) & (SGD_database['Systematic Name'] != gene) & (SGD_database['Start'] >= gene_start)), (SGD_database['Start'] - gene_start).abs(), np.nan)
    SGD_database['downstream'] = np.where(((SGD_database['Chromosome'] == gene_chromosome) & (SGD_database['Systematic Name'] != gene) & (SGD_database['End'] <= gene_end)), (SGD_database['End'] - gene_end).abs(), np.nan)
    upstream_temp = SGD_database.nsmallest(5, 'upstream').sort_values(by='upstream', ascending=True).reset_index()
    downstream_temp = SGD_database.nsmallest(5, 'downstream').sort_values(by='downstream', ascending=False).reset_index()
    upstream_temp['Direction'] = "Upstream"  
    downstream_temp['Direction'] = "Downstream"  
    Linkage_upstream = upstream_temp[['Systematic Name', 'Standard Name','Description','Direction']].copy()
    Linkage_downstream = downstream_temp[['Systematic Name', 'Standard Name','Description','Direction']].copy()  
    Linkage_temp = [Linkage_upstream, Linkage_downstream]
    Linkage = pd.concat(Linkage_temp).drop_duplicates(subset=['Systematic Name'])
    Linkage.insert(0, "Searched gene", gene)
    Linkage.insert(1, "Method", "Linkage")
    return(Linkage)