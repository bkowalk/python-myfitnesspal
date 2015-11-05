from __future__ import print_function
from datetime import datetime as dt
from datetime import timedelta as td
import argparse
import myfitnesspal
import MySQLdb

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", type=str, help="MyFitnessPal username (string)")
    parser.add_argument("password", type=str, help="MyFitnessPal password (string)")
    args = parser.parse_args()

    client = myfitnesspal.Client(args.username, args.password)

    today = dt.today()-td(hours=24)
    print("Report as of", today.date())
    day = client.get_date(today)

    print("Calories:", day.totals.get('calories'))
    print("Breakfast:", day.meals[0].totals.get('calories'))
    print("Lunch:", day.meals[1].totals.get('calories'))
    print("Dinner:", day.meals[2].totals.get('calories'))
    print("Snacks:", day.meals[3].totals.get('calories'))
    print("Weight:", client.get_measurements('Weight',today.date()).get(today.date()))
    print("Exercise:", client.get_exercise(today.date()))

    try:
        con = MySQLdb.connect(user='root',passwd='pantalones', db='scoreboard')
        cur=con.cursor()
        cur.execute("INSERT INTO scorechart VALUES (null,'bkowalk','5-10-15',5,10,15,20,25,30,182.5)")
        cur.execute("select * from scorechart")
        print ("result:",cur.fetchone())
        con.commit()
        con.close()
    except:
        print("Error %d: %s" % (e.args[0], e.args[1]))
