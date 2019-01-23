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

4. Once this is done, cd into the parent class_util folder and run ```docker-compose exec web python manage.py load_section_data```

### Usage
The containers can be started with `docker-compose start`

You can get started by navigating to [127.0.0.1:8000](http://127.0.0.1:8000/)

## Installation
Requires Docker and docker-compose
```bash
# Clone the repository
git clone https://github.com/PhilipConte/class_util
cd class_util

# Build and start the containers
docker-compose up -d
```
