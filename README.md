# class_util
website containing a collection of tools related to classes

### Installation
Requires Python 3, pip, and preferably virtualenv
```bash
# Clone the repository
git clone https://github.com/PhilipConte/class_util
cd class_util

#install packages
virtualenv env
source env/bin/activate
pip install -r requirements.txt

#start the server
python manage.py runserver

#migrate
python manage.py makemigrations
python manage.py migrate
```
## distributions
A tool to view (Virginia Tech) grade distributions

*note: This project is not affiliated wih Virginia Tech and as such does not host any distributions. Prospective users must provide them themselves*

With that being said, if you have a PID login to access VT's single sign-on service, you can download distributions [here](https://irweb.ir.vt.edu/webtest/Authenticated/GradeDistribution.aspx)

### Setup
CSVs should be labeled in the format [fall/spring]YYYY.csv.  
ie: fall 2017 would be fall2017.csv

The Desired CSVs should be placed in the class_util/distributions/data folder.
Once this is done, cd into the parent class_util folder and run ```python manage.py load_section_data```

*note: the server needs to have been run at least once and migrations must be made and applied before loading*

The website to view the database is WIP. However, you can always use tools like the great [DB Browser for SQLite](https://sqlitebrowser.org/) to view the data (in the distributions_section table) in the db.sqlite3 file in the root of the project.

### Usage
With the server running, you can navigate to the following pages:

| link          | Description | Example |
| ------------- | ------------- | ------------- |
| 127.0.0.1:8000  | a table of all imported sections  | |
| 127.0.0.1:8000/course/dddd+####  | all sections of course number '####' in department of abbreviation 'dddd'  | 127.0.0.1:8000/course/math+2204 = all math 2204 sections |
