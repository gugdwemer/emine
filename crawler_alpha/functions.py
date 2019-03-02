def writetodb(param):
    import pymysql as mysql
    import warnings
    warnings.filterwarnings('ignore')

    # Connect to the database
    connection = mysql.connect(host='localhost',
                               user='root',
                               password='',
                               charset='utf8mb4')

    connection.cursor().execute('create database IF NOT EXISTS twitter_crawler')
    connection.cursor().execute('use twitter_crawler')

    try:
        with connection.cursor() as cursor:
            # Create tweets table if not exist
            sql = """CREATE TABLE IF NOT EXISTS tweets (
                            id INT NOT NULL AUTO_INCREMENT,
                            user_id CHAR(200),
                            user_avatar CHAR(200),
                            username CHAR(200),
                            fullname CHAR(200),
                            tweet_text CHAR(200),
                            tweet_id CHAR(200),
                            date_time CHAR(200),
                            comment_count CHAR(200),
                            retweet_count CHAR(200),
                            like_count CHAR(200),
                            PRIMARY KEY (ID)
                        )"""
            cursor.execute(sql)
            connection.commit()

            sql = "INSERT INTO tweets(user_id, user_avatar, username, fullname, tweet_text, tweet_id, date_time, comment_count, retweet_count, like_count)" \
                  " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor.execute(sql, (param['User id'],
                                 param['User avatar'],
                                 param['Username'],
                                 param['User Fullname'],
                                 param['Tweet text'],
                                 param['Tweet id'],
                                 param['Datetime'],
                                 param['Comment count'],
                                 param['Retweet count'],
                                 param['Like count']))
            connection.commit()

    finally:
        connection.close()
