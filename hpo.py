import requests
import json 

class TermCategory():
    def __init__(self, label, terms):
        self.label = label
        self.terms = terms


class Gene():
    def __init__(self, gene_id, gene_symbol, terms = None, diseases = None):
        self.gene_id = gene_id
        self.gene_symbol = gene_symbol
        self.terms = terms
        self.diseases = diseases

class Term():
    def __init__(self, ontology_id, name, definition, frequency=None, onset=None, sources=None):
        self.ontology_id = ontology_id
        self.name = name
        self.definition = definition
        self.frequency = frequency
        self.onset = onset
        self.sources = sources

class Disease():
    def __init__(self, disease_id, disease_name, db_id, db, gene_assoc = None, terms = None):
        self.disease_id = disease_id
        self.disease_name = disease_name
        self.db_id = db_id
        self.db = db
        self.gene_assoc = gene_assoc
        self.terms = terms

class HPOApi():
    url_base = "https://hpo.jax.org/api/hpo/"

    def gene_search(self, entrez_gene_id):
        get = requests.get(f"{self.url_base}gene/{entrez_gene_id}")
        response = json.loads(get.content)
        
        if response.get('message'):
            raise ValueError(f"{response['error']}: {response['message']}")

        terms = [
            Term(
            ontology_id = term['ontologyId'], 
            name = term['name'], 
            definition=term['definition']) 
            for term in response['termAssoc']
        ]

        diseases = [
            Disease(
                disease_id = disease['diseaseId'],
                disease_name=disease['diseaseName'],
                db_id=disease['dbId'],
                db=disease['db']
            ) 
            for disease in response['diseaseAssoc']
        ]

        gene = Gene(
            gene_id = response['gene']['entrezGeneId'],
            gene_symbol=response['gene']['entrezGeneSymbol'],
            terms=terms,
            diseases=diseases
        )

        return gene

    def disease_search(self, id):
        get = requests.get(f"{self.url_base}disease/{id}")
        response = json.loads(get.content)
        
        if response.get('message'):
            raise ValueError(f"{response['error']}: {response['message']}")

        genes = [
            Gene(
                gene_id = gene['entrezGeneId'], 
                gene_symbol = gene['entrezGeneSymbol']
            ) for gene in response['geneAssoc']
        ]

        terms = [
            TermCategory(
                category['catLabel'],
                [Term(term['ontologyId'], term['name'], term['definition'], term['frequency'], term['onset'], term['sources']) for term in category['terms']]
            ) for category in response['catTermsMap']
        ]


        disease = Disease(
            disease_id = response['disease']['diseaseId'],
            disease_name=response['disease']['diseaseName'],
            db_id=response['disease']['dbId'],
            db=response['disease']['db'],
            gene_assoc=genes,
            terms=terms
        )

        return disease

    
