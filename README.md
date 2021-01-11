# Find healthy products, using OpenFoodFacts API.

---


## What is this program for ?

Find healthier substitutes to a food product. A program that would interact with the Open Food Facts database to retrieve foods, 
compare them and offer the user a healthier alternative to the food they want.

___


### *Install Python*

- Python 3.8
  > Install Python : https://www.python.org/downloads/
  
  > Python Documentation : https://www.python.org/doc/

### *MySQL & MySQL Workbench*

- MySQL 8
  > Install MySQL : https://dev.mysql.com/downloads/mysql
  
  > MySQl documentation : https://dev.mysql.com/doc/

  > Install MySQL Workbench : https://dev.mysql.com/downloads/workbench/
### *Virtualenv*

- **Install** : pip3 install virtualenv 
- **Create Virtualenv folder in the project** : virtualenv -p python3 env
- **Activate Virtualenv** : source env/bin/activate

### *Requirements*

- mysql-connector-python
  > Documentation : https://dev.mysql.com/doc/connector-python/en/
- requests 
  > Documentation : https://pypi.org/project/requests/2.7.0/
- flake8 
  > Documentation : https://flake8.pycqa.org/en/latest/


### *Install the program*

- **Download or Clone the project** : https://github.com/LekishviliRati/P5_OpenFoodFacts.git
- **Install requirements** : pip install -r requirements.txt
- **Install and activate Virtualenv**
- **Run** : main.py


### *Key Features*

- Create empty database.
- Fill the database.
- Display categories.
- Select a category.
- Display popular not healthy products of the selected category.
- Select a product and display available substitutes.
- Select a healthier substitute and display information about it.
- Save or not chosen substitute in favorite list.
- Display favorite list.
- Reset favorite list.
- Reset database.
