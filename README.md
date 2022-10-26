# ArXiv preprints version analysis
Many scientific papers change over time in order to correct mistakes, address peer review comments, or to modify metadata. The aim of this project is to identify such papers on arXiv, analyse changes between their versions, find the most common ones and see how they may differ based on the subject of the paper.

#### Table of contents
* [General approach](https://github.com/andcov/arXiv_preprints_version_analysis#general-approach)
* [Setup](https://github.com/andcov/arXiv_preprints_version_analysis#setup)
* [Documentation & Design Decisions](https://github.com/andcov/arXiv_preprints_version_analysis#documentation--design-decisions)
	* [Preprocess & Pre-analyse](https://github.com/andcov/arXiv_preprints_version_analysis#preprocess--pre-analyse)
	* [Download & Process](https://github.com/andcov/arXiv_preprints_version_analysis#download--process)
	* [Analyse](https://github.com/andcov/arXiv_preprints_version_analysis#analyse)
		* [Words and tokens](https://github.com/andcov/arXiv_preprints_version_analysis#words-and-tokens)
		* [NaN values](https://github.com/andcov/arXiv_preprints_version_analysis#nan-values)
* [Acknowledgements](https://github.com/andcov/arXiv_preprints_version_analysis#acknowledgements)


## General approach
Kaggle [provides](https://www.kaggle.com/datasets/Cornell-University/arxiv) a Json file that contains metadata describing the entire arXiv corpus. This will be used to find papers with more than one version and to group them based on subject, date of publication on arXiv etc.

A subset of the aforementioned papers will be fed to [GROBID](https://github.com/kermitt2/grobid) in order to convert them to [TEI](https://tei-c.org/) (a format of XML designed to describe scientific papers).

These XML files will then be compared based on a number of features.

# Setup
1. Clone the repository (the Python client of GROBID is used as a submodule so the `--recurse-submodules` flag is necessary):
```bash
git clone --recurse-submodules https://github.com/andcov/arXiv_preprints_version_analysis
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

4. Unzip `papers.zip` (it contains CSVs describing the papers):
```bash
unzip papers.zip
```

**Warning!** In order to keep the repository at a reasonable size, the original Kaggle dataset is not included. If you wish to alter the pre-processing phase, you may want to [download](https://www.kaggle.com/datasets/Cornell-University/arxiv) it.

5. [Install](https://grobid.readthedocs.io/en/latest/Install-Grobid/) and [run](https://grobid.readthedocs.io/en/latest/Grobid-service/) GROBID.

6. Depending on where you run GROBID, you may need to change the attributes in `grobid_python_config.json`.

7. Start a Jupyter client:
```bash
jupyter notebook
```
or a JupyterLab client:
```bash
jupyter lab
```

After this you should be able to run any of the scripts from the repo.

# Documentation & Design Decisions
The project was split into four main phases:
1. **Preprocess** - download and parse the Kaggle Json file
2. **Pre-analyse** - analyse the arXiv corpus and decide which papers to keep and which to discard
3. **Download & Process** - download the PDFs decided upon in the previous step and process them using Grobid
4. **Analyse** - extract a number of features from the TEI files

During these phases, decisions had to be made about which papers to take into account and about how to structure the papers' metadata.

## Preprocess & Pre-analyse
Only papers with at least 2 and up to 4 versions where saved. The majority of papers with multiple versions fit in this category:

![](/images/total_versions_hist.png)

For similar reasons, only physics, mathematics and computer science papers were considered: 

![](/images/categories_bar.png)

It also became apparent that some papers are registered in multiple different categories, but this is not a significant sample of the corpus:

![](/images/venn.png)


Each version of each paper is stored as a separate entry in a DataFrame (usually called `papers` in the Jupyter Notebooks; equivalent to the `papers.csv` file). This made comparing consecutive versions very easy later on in the process.

Initially, the DataFrame has these columns extracted from the Kaggle corpus:
 * `title`
 * `id` - arXiv id
 * `categories` - [arXiv categories](https://arxiv.org/category_taxonomy) (e.g. hep-ph, math.CO, cs.CG)
 * `version` - the current version
 * `total_versions` - number of versions associated with this paper
 * `date` - when this particular version was uploaded to arXiv

The papers are then split into three DataFrames (with corresponding CSVs), one for each of the main categories.

## Download & Process
Due to practical considerations, only 4000 papers form each of the three main categories were studied, amounting to over 28.000 different versions.

We attempted to download 28724 versions. However, this was not wholly a straightforward process as some papers are removed after a while by the author. When requesting such a paper from arXiv you do not get a PDF, but an HTML page explaining the situation. Also, some papers take a long time to load, so arXiv sends an HTML page instead. In addition, Grobid failed to process some papers.

In the end, the second phase resulted in 24758 valid papers with their corresponding TEI files.

## Analyse
A number of features were then computed:
* `title` - title of the version (may differ from one version to another)
* `delta_time` - interval of time between the previous version and this one
* `is_pdf` - True if this version is a Pdf, False otherwise
* `grobid` - True if Grobid managed to process this version, False otherwise
* `pages` - number of pages
* `delta_pages` - difference in the number of pages between this version and the previous one
* `tokens_cnt` - number of tokens in this version
* `delta_tokens_cnt` - difference in the number of tokens between this version and the previous one
* `token_density` - number of tokens per page
* `words_cnt` - number of words in this version
* `added_words_cnt` - number of words added from the previous version
* `removed_words_cnt` - number of words removed from the previous version
* `relative_added_words` - number of added words divided by the number of words from **this version**
* `relative_removed_words` - number of removed words divided by the number of words **from the previous version**
* `ref_cnt` - number of references
* `delta_ref_cnt` - difference in the number of references between this version and the previous one
* `authors_cnt` - number of authors
* `delta_authors_cnt` - difference in the number of authors between this version and the previous one
* `figures_cnt` - number of figures
* `delta_figures_cnt` - difference in the number of figures between this version and the previous one
* `figures_density` - number of figures per page
* `title_changed` - True if the previous version has a different title
* `abstract_changed` - True if abstract differs compared to the previous version

### Words and tokens
**Important:** A distinction must be made between words and tokens. From now on, tokens will be referring to all of the words that constitute a paper, while words will indicate the unique tokens that appear in a paper  (e.g. ”he is tall and he is short” consists of 7 tokens and 5 words)

When computing any of the features related to words or tokens, what constitutes a token is a simple Regex expression `\p{L}{2,}` (two or more Unicode characters; Unicode characters were used instead of ASCII in order to incorporate other languages and alphabets). More advanced NLP techniques were considered, but due to the size of the corpus these were impractical. This simplicity may, however, not be and issue, as scientific papers use a formal register which is suitable for this kind of segmentation.

### NaN values
One of these fields may be equal to NaN or NaT if:
* it is the first version, so the delta values could not be computed as there is no previous version to compare to.
* `is_pdf` is False; in this case, the vast majority of the values cannot be extracted.
* `grobid` is False; in this case, any value that should have been extracted from the TEI file will be NaN.
* values in the TEI file are missing

There is one exception to the cases mentioned above in relation to the title. If the title of a version cannot be extracted from the TEI file, or if this file does not exist, the original title from the Kaggle corpus will be used.

# Acknowledgements
This work has been done as part of an internship at TU Wien, Faculty of Informatics, Institute for Software Systems Engineering under the attentive guidance of Florina Piroi.

Thank you to arXiv for use of its open access interoperability.

Thank you to Grobid for it's open source software.
