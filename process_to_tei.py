from grobid_client.grobid_client import GrobidClient

# folder with input papers (!!! must add '/' at the end)
input_path = './papers/math/'
# folder where the output XML files will be saved (!!! must add '/' at the end)
output_path = './papers/math_tei/'

# you may need to change the config based on where you host Grobid, the number of threads available etc. (https://grobid.readthedocs.io/en/latest/) 
client = GrobidClient(config_path='./grobid_python_config.json')

# !!! this will reprocess any file that is already in `output_path` (bacause of `force=True`)
# you may want to change `n` based on the number of threads available on the server running Grobid (https://grobid.readthedocs.io/en/latest/) 
client.process('processFulltextDocument', input_path, output=output_path, consolidate_citations=False, tei_coordinates=False, force=True, n=7)
