# jupyter_analysis

This is an exploratory data analysis project on the sample set from Adam Rule's Corpus of jupyter notebooks. In this project, we filter the sample set for notebooks we are interested in, categorize notebooks cells and lines based on a taxonomy developed, and visualize the transitions from one category to another within notebooks. The project then attempts to cluster these notebook time series to search for trends.

Using Notebook Filter on Sample Corpus
1. Download sample corpus from https://library.ucsd.edu/dc/object/bb2733859v
2. Unzip download
3. Move download folder (should be called "sample_data") to same directory as this repository. "jupyter_analysis" and "sample_data" should be in the same directory.
4. Change into directory "jupyter_analysis" with `cd jupyter_analysis`
5. Run `python notebookFilter.py` or `python3 notebookFilter.py` depending on python version
6. Filtered notebooks will be in directory titled "filteredSample" that is in the directory also containing "jupyter_analysis" and "sample_data." 