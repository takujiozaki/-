import sqlite3
import csv

# DBを定義
db = 'exam.sqlite'
# 接続
connection = sqlite3.connect(db)

# カーソルを生成
cursor = connection.cursor()
sql = 'create table staff (id INTEGER PRIMARY KEY, name varchar(50), gender varchar(2), age INTEGER, blood varchar(2))'
try:
    # make staff table
    cursor.execute("DROP TABLE IF EXISTS staff")
    cursor.execute(sql)
    with open('staff.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            sql = "insert into staff(id, name, gender,age,blood) values ({0},'{1}','{2}',{3},'{4}')"
            sql = sql.format(row[0], row[1], row[2], row[3], row[4])
            cursor.execute(sql)

    # make gender table
    cursor.execute("DROP TABLE IF EXISTS gender")
    cursor.execute("CREATE TABLE gender (suf char(1), name text)")
    cursor.execute("INSERT INTO gender VALUES('f','女性')")
    cursor.execute("INSERT INTO gender VALUES('m','男性')")

    cursor.execute(
        'select staff.id, '
        'staff.name, '
        'staff.age, '
        'gender.name, '
        'staff.blood '
        'from staff join gender '
        'on staff.gender = gender.suf '
        'order by staff.age')
    # 表を取得
    fetch_all = cursor.fetchall()
    # 出力パターン
    output1 = '{}\t{}\t{}\t{}\t{}'
    output2 = '{}\t{}\t{}歳\t{}\t{}型'
    # 見出し
    print(output1.format('#', '氏名', '年齢', '性別', '血液型'))
    print('----------------------------------')
    for data in fetch_all:
        print(output2.format(data[0], data[1], data[2], data[3], data[4]))
except sqlite3.Error as e:
    print(e.args[0])

connection.commit()
connection.close()
