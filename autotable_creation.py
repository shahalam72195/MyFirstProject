import sqlite3
con_obj=sqlite3.connect(database='bank.sqlite')  #cwd
cur_obj=con_obj.cursor()
try:
    cur_obj.execute('''create table users(
                    users_acno integer primary key autoincrement,
                    users_pass text,
                    users_name text,
                    users_mob text,
                    users_email text,
                    users_bal float,
                    users_adhar text,
                    users_opendate text)
                ''')

    cur_obj.execute('''create table txn(
                    txn_id integer primary key autoincrement,
                    txn_acno int,
                    txn_type text,
                    txn_date text,
                    txn_amt float,
                    txn_updatebal float)
                ''')
    print('tables created')
except:
    pass
con_obj.close()