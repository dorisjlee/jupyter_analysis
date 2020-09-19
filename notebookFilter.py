"""
Script to copy notebooks containing/excluding keywords 
Authors: Doris Lee (dorisjlee), Jerry Song (jerrysong1324)
"""

import glob
import json
import os
import shutil

# Gets names of all files ending in .ipynb
nbNames = glob.glob("../sample_data/data/notebooks/*.ipynb")

excludeWords = ["homework", "lecture", "assignment", "introduction to"]

print("Searching " + str(len(nbNames)) + " notebooks for keywords...")
nbNameList = []
nbNamePassLst = []
nbNamePassInOrderLst = []
for nbName in nbNames: 
    excludeFlag = True # true if doen not contain any of the exclude words
    containsFlag = False # true if contains words we want
    executionIncreasingFlag = True
    try: 
        nb_json = json.load(open(nbName))
        # Uncomment if you want to watch progress
        # print("Reading " + str(nbName))
        if ("cells" in nb_json): # check if cell field exist
            nbNameList.append(nbName)
            NcodeCell = len(list(c['source'] for c in nb_json["cells"] if c['cell_type'] == 'code'))
            if NcodeCell> 10: # Filters by number of code cells
                prev = 0 # Used to keep track of strictly incresing execution order
                for cell in nb_json["cells"]: # Filters by keywords
                    if cell['cell_type'] == 'code':
                        if cell['execution_count'] == None or cell['execution_count'] < prev:
                            executionIncreasingFlag = False
                            break
                        prev = cell['execution_count']

                    cellSourceStr = "".join(cell["source"]).lower()
                    if excludeFlag: # Boolean logic to short circuit
                        for word in excludeWords:
                            if word in cellSourceStr:
                                excludeFlag = False
                                break

                    # Boolean logic to short circuit 
                    if excludeFlag and not containsFlag and \
                        (("import pandas" in cellSourceStr ) or ("from pandas" in cellSourceStr )) and \
                            (("import matplotlib" in cellSourceStr ) or ("from matplotlib" in cellSourceStr )):
                            containsFlag = True
                    
        else:
            # Uncomment if you want to see notebooks that have no cells
            # print(str(nbName) + " has no cells")
            pass
        if containsFlag and excludeFlag:
            nbNamePassLst.append(nbName)
            if executionIncreasingFlag:
                nbNamePassInOrderLst.append(nbName)

    except:
        # Uncomment if you want to see notebooks that cannot be read
        # print(str(nbName) + " cannot be read")
        pass

# Creates analyzableNotebooks folder in the same directory that holds 'sample_data'
print("Making analyzableNotebooks folder...")
cwd = os.getcwd()
dir = os.path.join(cwd, "..", "analyzableNotebooks")
if not os.path.exists(dir):
    os.mkdir(dir)
else:
    print("Error: analyzableNotebooks folder already exists. Please remove and try again.")
    exit()

# Copies selected notebooks over to filteredSample folder
print("Copying analyable notebooks...")
for fpath in nbNameList: 
    fname = fpath.split("/")[-1]
    shutil.copy(fpath,"../analyzableNotebooks/"+fname)
print("Done, found " + str(len(nbNameList)) + " notebooks to be analyzed")


# Creates filteredSample folder in the same directory that holds 'sample_data'
print("Making filteredSample folder...")
cwd = os.getcwd()
dir = os.path.join(cwd, "..", "filteredSample")
if not os.path.exists(dir):
    os.mkdir(dir)
else:
    print("Error: filteredSample folder already exists. Please remove and try again.")
    exit()
    
# Copies selected notebooks over to filteredSample folder
print("Copying filtered notebooks...")
for fpath in nbNamePassLst: 
    fname = fpath.split("/")[-1]
    shutil.copy(fpath,"../filteredSample/"+fname)
print("Done, found " + str(len(nbNamePassLst)) + " matching your criteria")

# Creates filteredOrderedSample folder in the same directory that holds 'sample_data'
print("Making filteredOrderedSample folder...")
cwd = os.getcwd()
dir = os.path.join(cwd, "..", "filteredOrderedSample")
if not os.path.exists(dir):
    os.mkdir(dir)
else:
    print("Error: filteredOrderedSample folder already exists. Please remove and try again.")
    exit()
    
# Copies selected notebooks over to filteredOrderedSample folder
print("Copying filtered and ordered notebooks...")
for fpath in nbNamePassInOrderLst: 
    fname = fpath.split("/")[-1]
    shutil.copy(fpath,"../filteredOrderedSample/"+fname)
print("Done, found " + str(len(nbNamePassInOrderLst)) + " matching your criteria and executed in order")
