import psycopg2
conn = psycopg2.connect(database = 'job_portal',user = 'postgres',
	password = "postgres", port = '5432',host = '127.0.0.1')
cur = conn.cursor()
company_name= "data_list[0]"
mobile = 456789
email = "data_list[2]"
password = "data_list[3]"
dataStoreQuery = """INSERT INTO recruiter (company_name, mobile, email, password) values('{}',{},'{}','{}')""".format(company_name, mobile, email, password)
query = "INSERT INTO recruiter (company_name, mobile, email, password) VALUES (%s,%s,%s,%s) RETURNING id;"
io = cur.execute(query, (company_name, mobile, email, password))
rec_id = cur.fetchone()[0]
print(io)
print(rec_id)
cur.close()
conn.commit()
conn.close()