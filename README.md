# Analysis of changes between versions of scientific papers published on arXiv
Many scientific papers change over time in order to correct mistakes after peer-reviews or to modify metadata. The aim of this project is to find such papers on arXiv, analyse changes between their versions, find the most common ones and see how they may differ based on the subject of the paper.

## General approach
Kaggle [provides](https://www.kaggle.com/datasets/Cornell-University/arxiv) a JSON file that contains metadata describing the entire arXiv corpus. This will be used to find papers with more than one version and to group them based on subject, date of publication on arXiv etc. (the processed metadata of these papers is saved in `papers.csv`).

A subset of the aforementioned papers will be fed to [GROBID](https://github.com/kermitt2/grobid) in order to convert them to [TEI](https://tei-c.org/) (a format of XML designed to describe scientific papers).

These XML files will then be compared based on a number of metrics.

## Setup
1. Clone the repository (the Python client of GROBID is used as a submodule so the `--recurse-submodules` flag is necessary):
```bash
git clone --recurse-submodules https://github.com/andcov/multi-versioned_arxiv_papers
```
If you forgot the `--recurse-submodules` flag when cloning, use the follwoing command:
```bash
git submodule update --init
```

2. Install the Python dependencies described in `requirements.txt` (you may want to use a virtual environemnt such as [virtualenv](https://virtualenv.pypa.io/en/latest/)):
```bash
pip install -r requirements.txt
```

3. Setup the GROBID Python client:
```bash
cd grobid_client_python
python3 setup.py install
```

4. Unzip `papers.zip` (it contains `papers.csv`):
```bash
unzip papers.zip
```

**Warning!** In order to keep the repository at a resonable size, the original Kaggle dataset is not included. If you wish to alter the pre-processing phase, you may want to [download](https://www.kaggle.com/datasets/Cornell-University/arxiv) it.

5. [Install](https://grobid.readthedocs.io/en/latest/Install-Grobid/) and [run](https://grobid.readthedocs.io/en/latest/Grobid-service/) GROBID.

6. Depending on where you run GROBID, you may need to change the server and port attributes in `grobid_python_config.json`.

7. Start a Jupyter client:
```bash
jupyter notebook
```
or a JupyterLab client:
```bash
jupyter lab
```

After this you should be able to run any of the scripts from the repo.

## Thanks
Thank you to arXiv for use of its open access interoperability.

