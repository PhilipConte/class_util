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
CLASS_UTIL_SECRET_KEY=super_secure_tm
DATABASE_URL=postgres://postgres:temp@db/class_util_db
POSTGRES_PASSWORD=temp
" > .env
```

### Sections
3. `mkdir data`
1. Download distributions [here](https://udc.aie.vt.edu/irdata/data/Grade)
3. Place 'Grade Distribution.csv' in ./data/
4. Run ```docker-compose exec web python manage.py load_section_data```

### Pathways
1. See [pathways_scraper](https://github.com/PhilipConte/pathways_scraper) to get or create areas.json
2. Copy areas.json to ./data/
3. Run ```docker-compose exec web python manage.py load_pathways```

### Build and Start
Build and start the containers with ```docker-compose up -d```
