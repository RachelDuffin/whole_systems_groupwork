gene_ids = [3161, 3175, 3179, 3163, 3165, 3005, 3173, 2689, 1347, 3157]
fixed_gene_ids = [7170, 7169, 88, 7138, 4625, 4620, 89, 3741, 58]

from hpo import HPOApi

hpo = HPOApi()

gene_searches = [hpo.gene_search(id) for id in fixed_gene_ids]

disease_terms = hpo.disease_search(255995)




print(gene_searches)