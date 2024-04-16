from app import db, app
from app.db_connect  import connect

def get_teams():
    conn = connect()
    with conn.cursor() as cur :
        sql = f'Select team_id, team_name, team_mascot from team order by team_name'
        cur.execute(sql)
        return cur.fetchall()

def get_practices():
    conn = connect()
    with conn.cursor() as cur:
        sql = f'Select p.practice_id, t.team_id, t.team_name, p.practice_length, date(p.practice_date) as practice_date ' \
                'from team t, practice p where t.team_id = p.team_id order by team_name'
        cur.execute(sql)
        return cur.fetchall()

def get_practice(practice_id):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'Select p.practice_id, t.team_id, t.team_name as team_name, p.practice_length as practice_length, date(p.practice_date) as practice_date ' \
                'from team t, practice p where t.team_id = p.team_id and p.practice_id = %s order by team_name'
        cur.execute(sql, str(practice_id))
        return cur.fetchall()
def get_team_name(team_id):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'Select t.team_id, t.team_name as team_name ' \
                'from team t where t.team_id = %s order by team_name'
        cur.execute(sql, str(team_id))
        return cur.fetchall()