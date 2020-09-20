"""
 Contains services that help parse the ipynb notebooks and store the useful
 information into a next list of dictionaries which can be turned into a dataframe 
 and written to a csv.
Author: Jerry Song (jerrysong1324)
"""
import glob
import json
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup


# Helper to create data structure to store functions and categories
def makeNestedDict(categories):
    for category, functions in categories.items():
        fnCounts = {}
        for fn in functions:
            fnCounts[fn] = 0
        categories[category] = fnCounts
        
createFns = ["read", "DataFrame", "Series", "copy"]
cleaningFns = ["isnull", "drop", "fill", "replace", "rename", "astype", "set_index", 
                   "loc","iloc", "index", "reset_index","astype", "query"]
printFns = ["head", "tail", "shape", "info", "describe", "value", "columns", "print"]
plotFns=["plot", "plotting"]
groupFns = ["group", "apply", "sort", "pivot"]
joinFns= ["append", "concat", "join"]
statsFns = ["describe", "mean", "corr", "max", "min", "median", "std", "sum"]

pandasFns = {"create":createFns, "cleaning":cleaningFns, "print":printFns, 
            "plot":plotFns, "group":groupFns, "join":joinFns, "stats":statsFns}
makeNestedDict(pandasFns)

preprocessingPackages = ['preprocessing', 'impute', 'feature_extraction', 'feature_selection', 'decomposition', 'discriminant_analysis', 
                       'random_projection', 'compose']
modelPackages = ['cluster', 'naive_bayes', 'svm', 
                         'neural_network', 'ensemble', 'dummy', 'gaussian_process', 
                        'manifold', 'mixture', 'multiclass', 'multioutput', 'neighbors', 
                         'semi_supervised', 'tree']
postprocessingPackages = ['covariance', 'metrics', 'inspection', 'model_selection']

sklearnPackages = {'preprocessing': preprocessingPackages, 'model': modelPackages, 'postprocessing': postprocessingPackages}


sklearnFns = {'preprocessing': [], 'model': [], 'postprocessing': []}

matplotlibFns = {"plot": {}}

def parseSkLearn():
    URL = 'https://scikit-learn.org/stable/modules/classes.html#'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='module-sklearn.base')
    keys = sklearnFns.keys()
    for key in keys:
        packages = sklearnPackages[key]
        for package in packages:
            idStr = 'module-sklearn.' + package
            results = soup.find(id=idStr)
            keyWords = results.find_all('tr', class_='row-odd')
            keyWords2 = results.find_all('tr', class_='row-even')
            keyWords.extend(keyWords2)
            for keyWord in keyWords:
                match = re.search(r"\.([\.\w]*)", keyWord.text)
                sklearnFns[key].append(match.group(1))
    makeNestedDict(sklearnFns)

parseSkLearn()


def getCategory(package, function):
    """
    Returns to category the function belongs to. Returns 'other' if the package or 
    function is not found.

    @param package: string package name e.g. 'pandas'
    @param function: string function anme e.g. drop
    @return: string of cateogry
    """
    if package == 'matplotlib':
        return 'plot'
    packageDictionary = {}
    if package == 'pandas':
        packageDictionary = pandasFns
    elif package == 'sklearn':
        packageDictionary = sklearnFns
    for key, val in packageDictionary.items():
        if function in val:
            return key
    return 'other'

# Helper to obtain list of notebooks to parse
def readNbs(filtered):
    nbNames = glob.glob("../../analyzableNotebooks/*.ipynb")
    if filtered:
        nbNames = glob.glob("../../filteredSample/*.ipynb")
    return nbNames

# Helper to find the matplotlib prefix package was imported as
def parsePrefix(text):
    matplotlibPrefix = ""
    m = re.search('^\s*import matplotlib\S* as (\S+)', text)
    if m:
        matplotlibPrefix = m.group(1)
    else:
        m = re.search('^\s*from matplotlib\S* import.*a?s? (\S+)', text)
        if m:
            matplotlibPrefix = m.group(1)
            if matplotlibPrefix == '*':
                m = re.search('^\s*from (matplotlib\S*) import', text)
                if m:
                    matplotlibPrefix = m.group(1)

        else:
            m = re.search('^\s*import (matplotlib\S*)', text)
            if m:
                matplotlibPrefix = m.group(1)
    return matplotlibPrefix

def analyzeFrequency(packages, filtered=True, analyzeLines=True):
    """
    Parses list of notebooks and searches for presence of package functions stored in packageDicts. Writes results to a csv.

    @param packageDicts: list of packages to analyze
    @param filtered: if True, search only through packages that satisfy filtered criteria, else search through all notebooks
    @param analyzeLines: if True, seach notebooks line by line, else seach cell by cell 
    @return: Return list of nested dictionary containing packages's categories->functions->counts, dictionary of linesPerCell, and codeCellsPerNB
    """
    nbNames = readNbs(filtered)
    packageDicts = {}
    if 'pandas' in packages:
        packageDicts['pandas'] = pandasFns
    if 'sklearn' in packages:
        packageDicts['sklearn'] = sklearnFns
    if 'matplotlib' in packages:
        packageDicts['matplotlib'] = matplotlibFns
    meta = []
    linesPerCell = {}
    codeCellsPerNB = {}
    totalNotebooks = len(nbNames)
    print("Searching " + str(totalNotebooks) + " notebooks for keywords...")
    for nbName in nbNames: 
        nb_json = json.load(open(nbName))
        name = re.findall('nb_\d+', nbName)[0]
        cellCount = 0
        matplotlibPrefix = None
        
        for cell in nb_json["cells"]:
            if cell['cell_type'] == 'code':
                cellSourceStr = "".join(cell["source"])
                
                if analyzeLines:
                    cellSourceStr = cellSourceStr.splitlines()
                    lineCount = len(cellSourceStr)
                    linesPerCell[name + " cell " + str(cellCount)] = lineCount
                else:
                    cellSourceStr = [cellSourceStr]
                
                lineCount = 1
                for text in cellSourceStr:
                    categoryName = 'other'
                   
                    ## New Cateogry Logic for 'other' 
                    ## Uncomment after fixing corresponding graph logic in nbVis.py
                
                    # if 'import' in text: 
                    #     categoryName = 'other (import)'
                    # if 'def' in text: 
                    #     categoryName = 'other (function declaration)'
                    # if '=' in text: 
                    #     categoryName = 'other (variable declaration)'
                    # controlHeuristics = ['if', 'elif', 'else' 'while', 'for', 'break', 'return', 'continue', 'del']
                    # for s in controlHeuristics: 
                    #     if s in text:
                    #         categoryName = 'other (compute)'
                    # computeHeuristics = ['np.', '+', '-', '*', '/']
                    # for s in computeHeuristics: 
                    #     if s in text:
                    #         categoryName = 'other (compute)' 
                    
                    if 'matplotlib' in packages:
                        if matplotlibPrefix and (matplotlibPrefix+'.' in text or matplotlibPrefix+'(' in text):
                                categoryName = 'plot'
                        elif 'import matplotlib' in text or 'from matplotlib' in text:
                            matplotlibPrefix = parsePrefix(text)
                    for packageName, fnCounts in packageDicts.items():
                        for category, fnCount in fnCounts.items():
                            for fn in fnCount.keys():
                                # text is just whole cell if not analyzing lines, else it is every line
                                if "."+fn in text or fn+'(' in text:
                                    fnCount[fn] += 1
                                    categoryName = category
                    lineCount += 1
                    entry = [name, cell['execution_count'], lineCount, categoryName, text]
                    meta.append(entry)
                                    
                cellCount += 1
        codeCellsPerNB[name] = cellCount

    print("Parsed " + str(sum(codeCellsPerNB.values())) + " cells")
    if analyzeLines:
        print("Parsed " + str(sum(linesPerCell.values())) + " lines")
    df = pd.DataFrame(meta, columns=['name', 'cell', 'line', 'category', 'text'])
    df.to_csv("NotebookCategoryInfo.csv")
    return packageDicts, linesPerCell, codeCellsPerNB
