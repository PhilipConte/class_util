# class_util
website containing a collection of tools related to classes

[Click here to check it out!](https://class-util.herokuapp.com)

## distributions
A tool to view (Virginia Tech) grade distributions

*note: This project is not affiliated wih Virginia Tech in any way*

## Dev Usage
Start the server by running `python manage.py runserver`

You can get started by navigating to [127.0.0.1:8000](http://127.0.0.1:8000/)

## Dev Setup
1. See [Installation](#installation)
2. See [Sections](#Sections)
3. See [Pathways](#pathways)

### Installation
Requires Python 3
```bash
# Clone the repository
git clone https://github.com/PhilipConte/class_util && cd class_util

# Set up the virtual environment
python3 -m venv env
```

Copy the following values into env/bin/activate
```bash
export CLASS_UTIL_SECRET_KEY="437n29c384xdz8t4z53itgukwszrenhtvgcukzsejhrdgn"
export CLASS_UTIL_DEBUG="1"
export CLASS_UTIL_ALLOWED_HOSTS="localhost,127.0.0.1"
```

Setup Django
```bash
# Activate the virtual environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Django
python manage.py runserver

# Migrate DB
python manage.py migrate
```

### Sections
CSVs should be labeled in the format YYYY_SEMESTER.csv  
ie: fall 2018 would be 2018_fall.csv

valid semester names:
1. spring
1. summer1
1. summer2
1. fall
1. winter

(you can add your override the defaults in  the `SEMESTER_DICT` constant defined in `load_section_data.py`)
1. Download distributions [here](https://irweb.ir.vt.edu/webtest/Authenticated/GradeDistribution.aspx)
2. Rename them as described above
3. Place the CSVs in /distributions/data/
4. Run ```python manage.py load_section_data```

### Pathways
1. See [pathways_scraper](https://github.com/PhilipConte/pathways_scraper) to create areas.json
2. Copy areas.json to /distributions/data/
3. Run ```python manage.py load_pathways```
