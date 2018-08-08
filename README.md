# class_util
website containing a collection of tools related to classes

## distributions
A tool to view (Virginia Tech) grade distributions

*note: This project is not affiliated wih Virginia Tech and as such does not host any distributions. Prospective users must provide them themselves*

With that being said, if you have a PID login to access VT's single sign-on service, you can download distributions [here](https://irweb.ir.vt.edu/webtest/Authenticated/GradeDistribution.aspx)

### Setup
1. See: [Installation](#installation)

2. CSVs should be labeled in the format YYYY_SEMESTER.csv  
    ie: fall 2018 would be 2018_fall.csv
    valid semester names:

    1. spring
    1. summer1
    1. summer2
    1. fall
    1. winter

    you can add your override the defaults in  the `SEMESTER_DICT` constant defined in `load_section_data.py`

3. The Desired CSVs should be placed in the /distributions/data folder.

4. Once this is done, cd into the parent class_util folder and run ```python manage.py load_section_data```

### Usage
With the server running, you can get started by navigating to [127.0.0.1:8000](http://127.0.0.1:8000/)

## Installation
Requires Python 3, pip, and preferably virtualenv
```bash
# Clone the repository
git clone https://github.com/PhilipConte/class_util
cd class_util

# Using virtualenv is recommended but not required
virtualenv env
source env/bin/activate # *nix
# OR
env\Scripts\activate # Windows

# Install packages
pip install -r requirements.txt

# Start the server
python manage.py runserver

# Migrate (note: server needs to be run at least once prior to migration)
python manage.py makemigrations
python manage.py migrate
```
