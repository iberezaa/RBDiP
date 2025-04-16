from flask import Flask, render_template, request, jsonify
import psycopg2
import requests
import re
import os
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

def get_db_connection():
    db_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vacancies (
        id VARCHAR(255) PRIMARY KEY,
        title TEXT,
        snippet TEXT,
        requirement TEXT,
        salary TEXT,
        url TEXT
    )
    ''')

    # Индексы — для ускорения WHERE, GROUP BY, ORDER BY
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_title ON vacancies(title)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_salary ON vacancies(salary)')

    conn.commit()
    cursor.close()
    return conn

def get_vacancies(profession, page=0, per_page=20):
    url = "https://api.hh.ru/vacancies"
    params = {'text': profession, 'page': page, 'per_page': per_page}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def clean_text(text):
    return re.sub(r'<[^>]+>', '', text or '')

def parse_vacancies(data):
    vacancies = []
    for item in data['items']:
        salary = item['salary']
        if salary:
            if salary['currency'] != 'RUR':
                continue
            if salary['from'] and salary['to']:
                salary_str = f"{salary['from']}-{salary['to']} RUR"
            elif salary['from']:
                salary_str = f"{salary['from']} RUR"
            elif salary['to']:
                salary_str = f"{salary['to']} RUR"
            else:
                salary_str = 'Не указана'
        else:
            salary_str = 'Не указана'

        vacancies.append({
            'id': item['id'],
            'title': clean_text(item['name']),
            'snippet': clean_text(item['snippet'].get('responsibility')),
            'requirement': clean_text(item['snippet'].get('requirement')),
            'salary': salary_str,
            'url': item['alternate_url']
        })
    return vacancies

def save_to_db(vacancies, conn):
    cursor = conn.cursor()
    insert_query = '''
    INSERT INTO vacancies (id, title, snippet, requirement, salary, url)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO UPDATE SET
    title = EXCLUDED.title,
    snippet = EXCLUDED.snippet,
    requirement = EXCLUDED.requirement,
    salary = EXCLUDED.salary,
    url = EXCLUDED.url
    '''
    for vacancy in vacancies:
        cursor.execute(insert_query, (
            vacancy['id'],
            vacancy['title'],
            vacancy['snippet'],
            vacancy['requirement'],
            vacancy['salary'],
            vacancy['url']
        ))
    conn.commit()
    cursor.close()

def salary_to_numeric(salary_str):
    if isinstance(salary_str, int):
        return salary_str
    if salary_str == 'Не указана':
        return 0
    try:
        parts = salary_str.replace('RUR', '').strip().split('-')
        if len(parts) == 2:
            return (int(parts[0]) + int(parts[1])) // 2
        return int(parts[0])
    except Exception:
        return 0

@app.route('/', methods=['GET', 'POST'])
def index():
    vacancies = []
    profession = ''
    num_vacancies = 0

    if request.method == 'POST':
        profession = request.form['profession']
        num_pages = int(request.form.get('num_pages', 5))
        conn = get_db_connection()

        all_vacancies = []
        for page in range(num_pages):
            data = get_vacancies(profession, page=page)
            parsed = parse_vacancies(data)
            all_vacancies.extend(parsed)

        save_to_db(all_vacancies, conn)
        conn.close()

        vacancies = all_vacancies
        num_vacancies = len(vacancies)

    return render_template('index.html', vacancies=vacancies, profession=profession, num_vacancies=num_vacancies)

@app.route('/sort_vacancies', methods=['POST'])
def sort_vacancies():
    vacancies = request.json['vacancies']
    sort_by_salary = request.json['sort_by_salary']
    sorted_vacancies = sorted(vacancies, key=lambda x: salary_to_numeric(x['salary']), reverse=(sort_by_salary == 'desc'))
    return jsonify(sorted_vacancies)

@app.route('/all_vacancies')
def all_vacancies():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id, title, snippet, requirement, salary, url FROM vacancies')
    vacancies = cursor.fetchall()

    cursor.execute('SELECT COUNT(*) FROM vacancies')
    vacancy_count = cursor.fetchone()[0]

    cursor.execute("""
    EXPLAIN ANALYZE 
    SELECT title, salary 
    FROM vacancies 
    WHERE salary <> 'Не указана' 
    AND salary LIKE '%RUR%' 
    ORDER BY title
""")


    cursor.execute('''
    SELECT title, ROUND(AVG(
        CASE
            WHEN salary LIKE '%-%' THEN
                (CAST(split_part(salary, '-', 1) AS bigint) + CAST(split_part(split_part(salary, '-', 2), ' ', 1) AS bigint)) / 2
            ELSE CAST(regexp_replace(salary, '[^0-9]', '', 'g') AS bigint)
        END
    )) AS average_salary
    FROM vacancies
    WHERE salary <> 'Не указана' AND salary LIKE '%RUR%'
    GROUP BY title
    ORDER BY average_salary DESC
    LIMIT 3
    ''')
    top_salaries = [{'name': row[0], 'average_salary': int(row[1])} for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return render_template('all_vacancies.html', vacancies=vacancies, vacancy_count=vacancy_count, top_salaries=top_salaries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
