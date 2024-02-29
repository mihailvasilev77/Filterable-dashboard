# Filterable dashboard web application
This is a project that features a dashboard of data taken from a csv file with the function of filtering based on the fields in the file. Its main logic is handled by Flask, Python while the front-end is written on HTML, CSS and JavaScript. Used modules are: flask, pandas, plotly, json. They can be found in the requirements.txt file.

## Table of Contents
+ [Technologies](#Technologies)
+ [Folder Structure](#fs)
+ [Installation](#Installation)
+ [Running](#Running)

## Technologies
- Python
- Flask
- JavaScript
- HTML
- CSS

## Folder Structure <a name="fs"></a>
The project should look like this
```
my_app/
  data/
    act.csv
    deact.csv
    wfm.csv
  one_filter/
    templates/
      index.html
    one_filter.py
  static/
    navbar.css
    script.js
    styles.css
  README.md
  app.py
  requirements.txt
  xlsx_to_csv.py
```

## Installation
```bash
git clone https://github.com/mihailvasilev77/Filterable-dashboard.git
pip install -r requirements.txt
```
or

```bash
git clone https://github.com/mihailvasilev77/Filterable-dashboard.git
py -m pip install -r requirements.txt
```

## Running
After cloning the github repo, navigate to the folder, open cmd in the directory and run this command:
```bash
py app.py
```
or
```bash
python3 app.py
```
After running the python script, the server is hosted locally and you can access the site on http://localhost:5000/ or http://127.0.0.1:5000/
