import pymysql
import random
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Mysql insert 100,000 scripts demo")

    parser.add_argument("--host", default='localhost',
                        help="User host")
    parser.add_argument("--user", default='root',
                        help="User name")
    parser.add_argument("--password", default='123456',
                        help="User password")
    parser.add_argument("--port", default=3306,
                        help="Connection port")
    parser.add_argument("--dbname", default='Student',
                        help="User database")

    return parser.parse_args()


def insert(args):
    conn = pymysql.connect(host=args.host, user=args.user, password=args.password, port=args.port, db=args.dbname)
    cursor = conn.cursor()
    # excute 100,000 insert script
    for i in range(1,100000):
        data = cursor.execute(f"insert into userinfo (user_id,username,gender,age,c_id) values('{i}','user{i}','男','{random.randint(18,80)}','{random.randint(1,20)}');")
        print(f"Insert {i}: {data}")
    conn.commit()

    cursor.close()


if __name__ == "__main__":
    args = parse_args()
    insert(args)

