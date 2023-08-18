# Flask Home Manager
## Initial Setup
By default a python environment is setup for you under serve.sh with the following, modify as desired
```
python3 -m venv ../virtual_env
source ../virtual_env/Scripts/activate
```
Before running serve.sh run these lines the above lines, then:
```
pip install flask
pip install flask_talisman
pip install cryptography
pip install waitress
```
To start the application call serve.sh
```
/path/to/serve.sh
```
In your browser, navigate to localhost:8081 (or whatever port you have defined in serve.sh)
![home_management_homepage](https://github.com/SoftwareMods/FlaskHomeManager/assets/7725472/887bd144-d51a-4a6a-8393-9f4b4a98543b)
### Chores
	Assignees
 Add / View / Update list of available assignees for chore assignment
 
 	Add Chore
 Add / View / Update list of chores
	
 	View Chores
 View chores that are due today based on frequency of chore and last completed date

### Tasks

### Shopping

### Bills

### School

### Study

### Journal

### Development

