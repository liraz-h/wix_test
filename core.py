import requests
import json
import time
import csv
from connection_config import connect_to_db
import os


def get_data_from_api():
    # get the data for each city from the API, using the city_configuration_data file, coordinates used as input
    with open('city_configuration_data.json', 'r') as f:
        config = json.load(f)
    for key, val in config.items():
        latitude = val['latitude']
        longitude = val['longitude']
        url = 'http://api.open-notify.org/iss-pass.json?lat=' + str(latitude) + '&lon=' + str(longitude) + '&n=50'
        r = requests.get(url)
        r_dict = r.json()
        response = r_dict['response']

    # insert the output data from the API into a table in MYSQL, row for each city and appearance
    # convert risetime to UTC
        for res in response:
            risetime = res['risetime']
            risetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(risetime))
            duration = res['duration']
            sql = """INSERT INTO orbital_data_liraz_hayat (city, risetime, duration) VALUES (%s, %s, %s)"""
            orbital_row = (key, risetime, duration)
            cursor.execute(sql, orbital_row)
            cnx.commit()


def create_procedure():
    # delete old procedure if exists
    cursor.execute("""DROP PROCEDURE IF EXISTS city_stats_liraz_hayat;""")
    cnx.commit()

    # create a procedure for average appearances per city
    cursor.execute("""CREATE PROCEDURE city_stats_liraz_hayat()
                        SELECT city, AVG(cnt_appears) AS avg_cnt_appears
                        FROM (
                            SELECT city, DATE(risetime) AS date_risetime, count(*) AS cnt_appears
                            FROM orbital_data_liraz_hayat
                            GROUP BY city, date_risetime) AS tbl
                        GROUP BY city;""")
    cnx.commit()


def save_results_to_csv():
    # delete csv file if exists
    if os.path.exists("procedure_results.csv"):
        os.remove("procedure_results.csv")

    # call the procedure and save the results to a csv file
    cursor.callproc('city_stats_liraz_hayat')
    res_dict = {}
    for result in cursor.stored_results():
        results = result.fetchall()
        # converting the results of the procedure from tuple to dictionary
        for row in results:
            res_dict[row[0]] = float(row[1])  # decimal to float
    csv_columns = ['City', 'Average_Count_Appears']
    try:
        with open('procedure_results.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_columns)
            for key, value in res_dict.items():
                writer.writerow([key, value])
    except:
        print("Cant create a csv file")


if __name__ == '__main__':
    # get connection details from a private file
    cnx = connect_to_db()  # connect to DB using mysql.connector.connect
    cursor = cnx.cursor()

    get_data_from_api()
    create_procedure()
    save_results_to_csv()
