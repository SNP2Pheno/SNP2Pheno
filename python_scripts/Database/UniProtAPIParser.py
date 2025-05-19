import sqlite3
import json

from urllib.request import urlopen

class UniProtParser:
    def __init__(self, file):
        self.db = sqlite3.connect(file)
        self.cursor = self.db.cursor()

    def get_diseases(self, rs_ID):
        url = f"https://rest.uniprot.org/uniprotkb/search?query=(xref:dbsnp-{rs_ID})"
        request = urlopen(url).read().decode("utf-8")
        data = json.loads(request)
        disease_ids = list()

        if 'results' in data and data['results']:
            for result in data['results']:
                if 'comments' in result and result['comments']:
                    for comment in result['comments']:
                        if comment.get('commentType') == 'DISEASE':
                            disease_id = comment.get('disease', {}).get('diseaseId')
                            print(comment)
                            if disease_id:
                                disease_ids.append(disease_id)
        return disease_ids

    def get_rs_IDs(self):
        self.cursor.execute("SELECT rs_ID FROM SNP_TABLE")
        return [row[0] for row in self.cursor.fetchall()]

    def run(self):
        rs_IDs = self.get_rs_IDs()
        for rs_ID in rs_IDs:
            diseases = self.get_diseases(rs_ID)
            for disease in diseases:
                pass

if __name__ == "__main__":
    parser = UniProtParser("SNP2Pheno.db")
    parser.get_diseases("rs33950507")