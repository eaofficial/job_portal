import psycopg2
conn = psycopg2.connect(database = 'job_portal',user = 'postgres',
	password = "postgres", port = '5432',host = '127.0.0.1')
cur = conn.cursor()

#create_recruiter = """Create table recruiter (id SERIAL,company_name varchar(50), email varchar(20), mobile INT, password varchar(20))"""
#cur.execute(create_recruiter)
create_seeker = """Create table seeker (seeker_id SERIAL,name varchar(50), email varchar(20), gender varchar(10), mobile INT, password varchar(20))"""

create_jobs = """CREATE TABLE jobs (job_id SERIAL, title varchar(30), description varchar(200), company_name varchar(100), recruiter_id int)"""

create_applications = """CREATE TABLE applications (id SERIAL, seeker_id int, job_id int)"""

#cur.execute(create_seeker)
cur.execute(create_jobs)
cur.execute(create_applications)
cur.close()
conn.commit()
conn.close()

"INSERT INTO ACCOUNTS (company_name, mobile, email, password) VALUES (%s,%s,%s,%s)", (company_name, mobile, email, password))