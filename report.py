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
    print("Fetching report for " + args.username + "as of" + today.date() + "...")
    day = client.get_date(today)

    calories = day.totals.get('calories')
    breakfast = day.meals[0].totals.get('calories')
    lunch = day.meals[1].totals.get('calories')
    dinner = day.meals[2].totals.get('calories')
    snacks = day.meals[3].totals.get('calories')
    weight = client.get_measurements('Weight',today.date()).get(today.date())
    exercise = client.get_exercise(today.date())

    print("Calories:", calories)
    print("Breakfast:", breakfast)
    print("Lunch:", lunch)
    print("Dinner:", dinner)
    print("Snacks:", snacks)
    print("Weight:", weight)
    print("Exercise:", exercise)
    print("Submitting to DB");

    try:
        con = MySQLdb.connect(user='root', passwd='pantalones', db='scoreboard')
        cur = con.cursor()
        cur.execute("INSERT INTO scorechart "
            + "VALUES (null,\""
            + args.username + "\",\""
            + today.date() + "\","
            + calories + ","
            + breakfast + ","
            + lunch + ","
            + dinner + ","
            + snacks + ","
            + exercise + ","
            + weight)")
        con.commit()
        con.close()
        print("Successfully submitted.");
    except:
        print("Error %d: %s" % (e.args[0], e.args[1]))
