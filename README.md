# Extract_ID_card
This repository aim to extract information in new Vietnamese ID card. 

This model return a dictionary with information in this keys {'id', 'name', 'date', 'sex', 'residence', 'nationality', 'place of origin'}. 

# Installation
Install the required python library, recommend using anaconda enviroment python >= 3.8 to avoid conflict. 
```
$ pip install -r requirements.txt
```

## Usage
Download weight in this link 
```
https://drive.google.com/file/d/1z56nLqdLhvvHI14M8r5GGo7ANIaA34TL/view?usp=drive_link
```
In file ```config.py``` replace path of weights.

Replace your MySql database information if you want to connect to db when you deploy in your local server.

Run file ```main.py``` if you only want to test model and return result.

Run file ```deploy.py``` if you want to deploy to server.

## Notice
This repository is for studying purpose only. Pull requests are welcome. 

If you have any questions or advices to improve the model, please contact me via ```dungop12345@gmail.com``` 
