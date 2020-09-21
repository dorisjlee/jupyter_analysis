# jupyter_analysis

This is an exploratory data analysis project on the sample set from Adam Rule's Corpus of jupyter notebooks. In this project, we filter the sample set for notebooks we are interested in, categorize notebooks cells and lines based on a taxonomy developed, and visualize the transitions from one category to another within notebooks. The project then attempts to cluster these notebook time series to search for trends.

## Using Notebook Filter on Sample Corpus
1. Download sample corpus from https://library.ucsd.edu/dc/object/bb2733859v
2. Unzip download
3. Move download folder (should be called "sample_data") to same directory as this repository. "jupyter_analysis" and "sample_data" should be in the same directory.
4. Change into directory "jupyter_analysis" with `cd jupyter_analysis`
5. Run `python notebookFilter.py` or `python3 notebookFilter.py` depending on python version
6. Filtered notebooks will be in directory titled "filteredSample" that is in the directory also containing "jupyter_analysis" and "sample_data."

## Working with the Analysis Notebooks
First, run `1-FunctionFrequency.ipynb` to view some general information to classify all notebooks by line or cell as well as view general distribution information. The notebooks will generate `NotebookCategoryInfo.csv` which is used by the next notebook.

Next, run `2-HeatMapClustering.ipynb` to walk through the cluster feature generation process as well as classify the notebooks. The notebook will generate `FeaturesAndLabels.csv` which is used by the following notebook.

Finally, `ClusterVisualization.ipynb` will help visualize the notebooks in clusters. 

## Next steps
I began a manual analysis of notebooks in order to improve categorization accuracy which can be found in the `ManuallyAnalyzedNotebooks` folder. The main takeaway was that the other category could be better classified and broken down in categories of finer granularity such as `other (declaration)` or `other (control)`. I made these implementation changes in `notebookFilter.py` but the analysis notebooks don't look into this yet as some visualization changes would need to be made too. Hopefully, better classification would lead to better analysis of clusters.

## More Details
Please refer to `JupterMiningSummary.pdf` for more detail on the objective of the project as well as what was accomplished in the analysis notebooks.

## Acknowledgements
This project was made possible by Doris Lee's advising and collaboration. Thanks also to Aditya Paremeswaran, Stephen Macke, Andrew Head, and Doris Xin for their advising and weekly feeback on the progress.