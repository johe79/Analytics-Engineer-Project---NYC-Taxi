# ~/nyc_taxi_dbt/clean_sources.py
import codecs
import os

filepath = 'packages.yml'

if not os.path.exists(filepath):
    print(f"Error: File not found at {filepath}")
    exit(1)

try:
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned_content = content.replace(u'\xa0', u' ')

    with codecs.open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"Successfully cleaned non-standard spaces in {filepath}")

except Exception as e:
    print(f"An error occurred while cleaning the file: {e}")