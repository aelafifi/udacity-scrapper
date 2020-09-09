# Udacity Scrapper

This is a scraping tool for Udacity courses. It doesn't download the course resources,
instead, it downloads the entire content of the course contents (videos refs, notes, instructor notes, ..etc)
and create a similar structure on the target speficied directory on your local machine.

## How To Use

```
# Clone it
git clone https://github.com/aelafifi/udacity-scrapper.git

# Install it
cd udacity-scrapper
pip install ./

# Use it
mkdir TARGET_DIR
udacity COURSE_ID -o TARGET_DIR -u USERNAME_OR_EMAIL -p PASSWORD
```
