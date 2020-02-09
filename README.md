# class_util
A tool to view Virginia Tech grade distributions

[Click here to check it out!](http://distributions.pconte.me)


*note: This project is not affiliated wih Virginia Tech in any way*

## Dev Usage
Start the containers with `docker-compose start`

Navigate to [127.0.0.1:8000](http://127.0.0.1:8000/)

## Installation
Requires Docker and docker-compose
```bash
# Clone the repository
git clone https://github.com/PhilipConte/class_util
cd class_util
mkdir data
echo "CLASS_UTIL_ALLOWED_HOSTS=localhost,127.0.0.1
CLASS_UTIL_DEBUG=1
CLASS_UTIL_SECRET_KEY=super_secure_tm" > .env
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
4. Run ```docker-compose exec web python manage.py load_section_data```

### Pathways
1. See [pathways_scraper](https://github.com/PhilipConte/pathways_scraper) to create areas.json
2. Copy areas.json to /distributions/data/
3. Run ```docker-compose exec web python manage.py load_pathways```

### Build and Start
Build and start the containers with ```docker-compose up -d```
