from hpo import HPOApi
from unittest import TestCase


class TestHPO(TestCase):
    def test_hpo(self):
        hp = HPOApi()
        gene = hp.gene_search(6389)
        print(gene)
    
    def test_omim(self):
        hp = HPOApi()
        disease = hp.disease_search(154700)

