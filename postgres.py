# create table 
import psycopg2

conn = psycopg2.connect(database="dunhe", user="postgres", password="yxfhalan", host="192.168.40.91", port="5432")
print("Opened database successfully")

cur = conn.cursor()

                
cur.execute('''CREATE TABLE space_ds.FoundationLog\
       (ID  serial  PRIMARY KEY     NOT NULL, \
       No  integer,\
       tablename  integer,\
      proc integer   );''')   

   
print("Table created successfully")

conn.commit()
conn.close()



