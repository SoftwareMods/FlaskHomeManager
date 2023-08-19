# Flask Home Manager
## Initial Setup
By default a python environment is setup for you under serve.sh with the following, modify as desired
```
source ../virtual_env/Scripts/activate
```
Before running serve.sh run the above line, then:
```
bash /path/to/install.sh
```
To start the application call serve.sh
```
/path/to/serve.sh
```
To start the application IN DEBUG MODE call debug_serve.sh
```
/path/to/debug_serve.sh
```
In your browser, navigate to localhost:8081 (or whatever port you have defined in serve.sh)
![home_management_homepage](https://github.com/SoftwareMods/FlaskHomeManager/assets/7725472/8ae6814d-c4f1-4dfb-98a2-b31e51adf396)



### Chores
	Assignees
 Add / View / Update list of available assignees for chore assignment<br>
 The options for chore difficutly are defined in data/chores/diff.json as:<br>
 <ul>
	 <li>1 - Trivial</li>
	 <li>2 - Easy</li>
	 <li>3 - Moderate</li>
	 <li>4 - Hard</li>
 </ul>
 The difficulty is multiplied by the difficulty payout amount (defined on new Settings page) and added to assignee bank on chore completion.
 
 ![home_management_assignees](https://github.com/SoftwareMods/FlaskHomeManager/assets/7725472/52e5b532-8521-4c82-ad26-809809dcc3b6)

 
 	Add Chore
 Add / View / Update list of chores<br>
 ![home_management_new_chore](https://github.com/SoftwareMods/FlaskHomeManager/assets/7725472/c5660720-c0df-4e6a-b1c9-a42745d32496)

	
 	View Chores
 View chores that are due today based on frequency of chore and last completed date<br>
 ![home_management_chores_todo](https://github.com/SoftwareMods/FlaskHomeManager/assets/7725472/ae47f62d-b02d-4c70-84bc-1a99108465e4)


### Tasks
Add / Delete / Update list of single completion tasks<br>
![home_management_tasks](https://github.com/SoftwareMods/FlaskHomeManager/assets/7725472/f952ce4d-195a-4469-b31e-510871b7aae4)


### Shopping
Add / Delete / Update list of items needing purchased<br>
![home_management_shopping](https://github.com/SoftwareMods/FlaskHomeManager/assets/7725472/a434c92e-c3bd-487f-85b8-abe1f87e3f77)


### Bills
Add / Delete / Update list of bills to be managed<br>
![home_management_bills](https://github.com/SoftwareMods/FlaskHomeManager/assets/7725472/156580b2-14c1-45f9-8492-496bddbdc2ac)


### School
Future development

### Study
Add subjects for study with questions and index style cards to review
![home_management_study_index](https://github.com/SoftwareMods/FlaskHomeManager/assets/7725472/d914e179-15d0-458f-8363-32e4a670e335)
![home_management_study_review](https://github.com/SoftwareMods/FlaskHomeManager/assets/7725472/c9664030-8d84-4c14-bd7f-601bf22ec0bf)

### Journal
Add / View journal entries
![home_management_study_journal_add](https://github.com/SoftwareMods/FlaskHomeManager/assets/7725472/568b5886-e822-4d6b-9813-1b708222afbf)
![home_management_study_journal_list](https://github.com/SoftwareMods/FlaskHomeManager/assets/7725472/31376298-e9f0-4f43-b29e-acfec67648b8)



### Development
List of font awesome icons available for future development
![home_management_study_dev](https://github.com/SoftwareMods/FlaskHomeManager/assets/7725472/324f7378-aea2-4c75-ba44-db99c30fcd0d)

