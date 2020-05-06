# class_util
A tool to view Virginia Tech grade distributions. [Check it out](http://distributions.pconte.me)!

*note: This project is not affiliated wih Virginia Tech in any way*

## Developers
### Installation
```bash
git clone https://github.com/PhilipConte/class_util
cd class_util
mkdir data
echo "
CLASS_UTIL_ALLOWED_HOSTS=*
CLASS_UTIL_DEBUG=1
CLASS_UTIL_SECRET_KEY=super_secure_tm
DATABASE_URL=postgres://postgres:temp@db/class_util_db
POSTGRES_PASSWORD=temp
" > .env
docker-compose up -d
```

1. Get [distributions](https://udc.aie.vt.edu/irdata/data/Grade)
    1. Place 'Grade Distribution.csv' in ./data/
    1. `docker-compose exec web python manage.py load_sections`

1. Get [pathways](https://github.com/PhilipConte/pathways_scraper)
    1. Place areas.json in ./data/
    1. `docker-compose exec web python manage.py load_pathways`

### Usage
Run `docker-compose start` and navigate to [127.0.0.1:8000](http://127.0.0.1:8000/)
