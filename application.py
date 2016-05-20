import os
import flask
import MySQLdb

application = flask.Flask(__name__)
application.debug = True

@application.route('/')
def hello_world():
  return "Hello world cform!"

@application.route('/env')
def env():
  envs = "Environments: <br>"
  for key in os.environ.keys():
    envs = envs + "%s: %s<br>" % (key,os.environ[key])

  return envs

@application.route('/score')
def score():
  storage = Storage()
  storage.populate()
  score = storage.score()
  return "Hello world, %d!" % score

class Storage():
  def __init__(self):
    self.db = MySQLdb.connect(
      user   = os.getenv('MYSQL_USERNAME'),
      passwd = os.getenv('MYSQL_PASSWORD'),
      db     = os.getenv('MYSQL_INSTANCE_NAME'),
      host   = os.getenv('MYSQL_PORT_3306_TCP_ADDR'),
      port   = int(os.getenv('MYSQL_PORT_3306_TCP_PORT'))
    )

    cur = self.db.cursor()
    cur.execute("DROP TABLE IF EXISTS scores")
    cur.execute("CREATE TABLE scores(score INT)")

  def populate(self):
    cur = self.db.cursor()
    sql = "INSERT INTO scores(score) VALUES(1234)"

    try:
      # execute SQL inside a transaction
      cur.execute(sql)
      self.db.commit()
    except:
      # rollback if neccessary
      self.db.rollback()

  def score(self):
    cur = self.db.cursor()
    cur.execute("SELECT * FROM scores")
    row = cur.fetchone()
    return row[0]

if __name__ == "__main__":
  application.run(host='0.0.0.0', port=3000)
