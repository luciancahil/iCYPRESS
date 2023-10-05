# iCYPRESSS

## What is iCYPRESS?
iCYPRESS stands for identifying CYtokine PREdictors of diSeaSE.

It is a graph neural network library that analyzes gene expression data in the context of cytokine cellular networks.

## Install
To Install iCYPRESS, make sure that you are in a conda environement with python 3.9. Then, install the following libraries using these exact commands.


````
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cpuonly -c pytorch
conda install pyg -c pyg
conda install pytorch-scatter -c pyg
conda install pytorch-sparse -c pyg
pip install pytorch_lightning
pip install iCypress
````
## Testing

To make sure that all packages are installed properly try the following program:

````
from iCYPRESS import Cypress
from iCYPRESS.CytokinesDataSet import CytokinesDataSet

cyp = Cypress.Cypress()
cyp.train()
````


## Custom Data

To use this library on your own custom data, you will need two csv files: a patients file, and an eset file.

The eset file should be structured like so:

|"             "|  "gene_sym" |"GSM989153"  |"GSM989154" |"GSM989155" |
| ------------- |-------------| -----       | ---        | ---        |
| "1"           | "A1CF"      | 3.967147246 |3.967147248 |3.96714725  |
| "2"           | "A2M"       | 4.669213864 |4.669213567 |4.669213628 |
| "3"           | "A2ML1"     | 4.140074251 |4.140074246 |4.140074286 |


The top should include every patient who's data you wish to analyze, the 2nd collumn should contain 5h3 name of every gene you have data on, and the numbers represent the gene readings.

Meanwhile, the patients file should be structured like so:
|         |   |
|---------|---|
|GSM989161|0  |
|GSM989162|0  |
|GSM989163|0  |
|GSM989164|0  |
|GSM989165|0  |
|GSM989166|0  |
|GSM989167|1  |
|GSM989168|1  |
|GSM989169|1  |
|GSM989170|1  |
|GSM989171|1  |
|GSM989172|1  |
|GSM989173|1  |
|GSM989174|1  |
|GSM989175|1  |

Where the left collumn contains all the names of your patients, and the right collumn contains their classification.

It is very important that every patient that appears in your patients file also appears in the top row of your eset file and vice versa. Otherwise, the library will raise an error.

Once you've prepared both files and placed them into the directory as your main python file, run the following program, switching "eset.csv" and "patients.csv" with the actual names of your eset and patients file respecively.


````
from iCYPRESS import Cypress
from iCYPRESS.CytokinesDataSet import CytokinesDataSet

cyp = Cypress.Cypress(patients = "patients.csv", eset="GSE40240_eset.csv")
cyp.train('CCL1')
````


## Customization

There are two main ways you can change the way the libary analyzes your data: cytokine choice and hyper paramameters:

### Cytokines

There are 70 different cytokines that this network can use to build the Graph in its Graph Neural Network.

The example above uses CCL1, but you can also use CCL2, CD70, or many others.

You can get a list of supported cytokines by calling the method Cypress.Cypress(get_cyto_list) in your main file. To try running the model with every avilable cytokine, use the code below. Be warned, the program will take a while to execute.

```
from iCYPRESS import Cypress
from iCYPRESS.CytokinesDataSet import CytokinesDataSet

cyto_list = Cypress.Cypress.get_cyto_list()
cyp = Cypress.Cypress(patients = "patients.csv", eset="GSE40240_eset.csv", active_cyto_list = cyto_list)

for cyto in cyto_list:
  cyp.train(cyto)
```

If you want to run it with just a subset of cytokines, make cyto_list a string array containing only the cytokines you want to run on.

### Hyperparameterization

Hyperparameters are the parameters that control the structure of the code and training regiment. A brief breakdown of what each of them below.

|Hyperparameter       | Description  |
|---------------------|--------------|
| batch_size          | How many elements are in each training batch. If batch_size is set to 80, each batch will contain at most 80 elements
| eval_period         | How often the neural network evaluates itself on the training data. If set to 20, it will evaluate itself every 20 epochs.
| layers_pre_mp       | How many layers the network will run before the message passing stage.
| layers_mp           | How many rounds of message passing the network will do.
| layers_post_mp      | How many layers after the message passing stage will exist in the neural network.
| dim_inner           | The number of neurons in each hidden layer.
| max_epoch           | How many epochs the training stage will go through.


If you want to try having hyperparameters different from the default, pass the hyperparameter you want to change along with a value into the constructor. For example, to set max_epoch to 500, use the following code:

```
from iCYPRESS import Cypress
from iCYPRESS.CytokinesDataSet import CytokinesDataSet

cyto_list = Cypress.Cypress.get_cyto_list()
cyp = Cypress.Cypress(patients = "patients.csv", eset="GSE40240_eset.csv", max_epoch = 500)
```

## Quick start options

### repo setup on HPC (UBC ARC Sockeye)
* clone repo to project and scratch folders
```
module load git
export ALLOC=st-allocation-code
mkdir /arc/project/$ALLOC/$USER/
cd /arc/project/$ALLOC/$USER/
git clone https://github.com/CompBio-Lab/geomx2rna.git
cd geomx2rna/

mkdir /scratch/$ALLOC/$USER
cd /scratch/$ALLOC/$USER
git clone https://github.com/CompBio-Lab/geomx2rna.git
cd geomx2rna/
```
