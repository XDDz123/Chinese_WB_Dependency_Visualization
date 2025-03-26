# Chinese WB Dependency Visualization
This repository hosts code for the visualization interface that accompanies the paper: <b>Exploring Chinese Dependency Parsing Across Word Segmentation Strategies</b> by Yige Chen, Zelong Li, Changbing Yang, Cindy Zhang, Amandisa Cady,
Ai Ka Lee, Zejiao Zeng, and Jungyeul Park.

## Program requirements
Install the following:
- [Python](https://www.python.org/) (latest version recommend)
- [Flask](https://flask.palletsprojects.com/en/stable/installation/)
- [Stanza](https://stanfordnlp.github.io/stanza/)

## Instructions
1. Download trained models from [LINK HERE TBD](). 
2. Create a folder named <b>models</b>. Extract the downloaded trained models zip file, then place all contents <em>as is</em> within the <b>models</b> directory.
   Your directory should resemble the following:
      ```
      project
      │   ...    
      │
      └───models
      │   └───UD_Chinese-GSDSimp
      │   │   └───UD_Chinese-GSDSimp
      │   │   └───UD_Chinese-GSDSimp_model
      │   │   │   └───saved_models
      │   │   │   │   └───depparse
      │   │   │   │   │   zh-hans_gsdsimp_electra-large_parser.pt
      │   │   │   │   └───pos
      │   │   │   │   └───lemma
      │   │   │   │   └───tokenize
      │   └───UD_Chinese-GSDPKU
      │   ...
      ```
3.     python backend.py
      Run the python file to start the flask server. Initial loading times should be expected to be slow due to stanza downloading resources.
      For optimal performance, CUDA is recommended.
   
## UI
### Description 
The visualization interface consists of the following components:
- Text Box: where users can type in their sentences.
- Model Selection Checkboxes: "check" the corresponding checkbox to generate dependency visualizations with the selected model.
- View By Selection Menu: the UI provides two different views, one grouped by sentences, the other models.
  
After inputting sentences and selecting thier choice of models & views, simply press the submit button to generate the visualizations.
### UI Sample
<img src="https://github.com/user-attachments/assets/7e40fbe4-e433-4a62-a524-050983abb7d8" alt="drawing" width="80%"/>

## Acknowledgements
This visualization interface generates dependency visualizations with the help of [brat rapid annotation tool](https://brat.nlplab.org/).  
Portions of the html page (marked in code) and contents of the <b>/static</b> folder were sourced from the introduction page of the [universal dependencies website](https://universaldependencies.org/introduction.html).
