# Owkin use case
## Document
You can find in the file **owkin_use_case.pdf** my textuals answers and documentation about the use case
## Assets
You can find aready generated assets from code in the folder **curation-output/generated**

**Step 1** generates **dataset_description.json** 

**Step 2** generates **quality_assessment.json** 

**Step 3** generates **is_empty.png**, **is_format_not_compliant.png**, **rules.png**

**Step 4** generates **dataset_with_better_quality.csv**

## Code

### Make sure you are running python3.10
 ```console
$ python3 --version
```
### Go to the code folder 
 ```console
$ cd data-curation
```
### Install dependencies 
 ```console
$ pip install -r requirements.txt
```
### Install code 
 ```console
$ pip install .
```
### Run test
 ```console
$ pytest
```
### Run step 1
 ```console
$ python3 data_curation/description/run.py --dataset-path ../input-data/fake_dataset.csv --output-directory ../curation-output/ 
```
 ```console
$ ls ../curation-output/dataset_description.json 
```
### Run step 2
 ```console
$ python3 data_curation/quality/run.py --dataset-path ../input-data/fake_dataset.csv --output-directory ../curation-output/
```
 ```console
$ ls ../curation-output/quality_assessment.json 
```
### Run step 3
 ```console
$ python3 data_curation/dashboard/run.py --dataset-quality-assessment-path ../curation-output/quality_assessment.json --output-directory ../curation-output/
```
 ```console
$ ls ../curation-output/is_empty.png ../curation-output/is_format_not_compliant.png ../curation-output/rules.png
```
### Run step 4
 ```console
$ python3 data_curation/curation/run.py --dataset-path ../input-data/fake_dataset.csv --smoking-history-referential-path ../input-data/smoking_history_referential.csv --output-directory ../curation-output/
```
 ```console
$ ls ../curation-output/dataset_with_better_quality.csv
```
