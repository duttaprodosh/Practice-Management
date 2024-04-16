import pymysql

########   DB CONNECT  #####
def connect():
    connection = pymysql.connect(host='127.0.0.1', port=3306, database='baseballdb', user='root', password='root', cursorclass=pymysql.cursors.DictCursor)
    return connection
