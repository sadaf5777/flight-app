import mysql.connector
import os
import pandas as pd
class DB:
    def __init__ (self):
       
# connect to database server
        try:
            self.conn=mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = os.getenv("MYSQL_PASSWORD"),  # Verify if this is correct; try your actual password if set
            database = 'flights',
            port = 3307)
            self.mycursor=self.conn.cursor()
            print("connecton established")
            
        except:
             print('Error connecting to MySQL')
    def fetch_city_names (self):
        
        self.mycursor.execute("""
                            SELECT Source FROM `flights`.`cleaned_flights.csv`
                            UNION
                            SELECT Destination FROM `flights`.`cleaned_flights.csv`
                              """)
        data=self.mycursor.fetchall()
        all_cities=[]
        for city in data :
            all_cities.append(city[0])
        return all_cities
    

    def fetch_source_destination (self,source,destination):
        self.mycursor.execute("""SELECT * FROM `flights`.`cleaned_flights.csv`
                              WHERE Source='{}' AND Destination='{}'
                             """.format(source,destination))
        data=self.mycursor.fetchall()
        return pd.DataFrame(data,columns=["Airline","date_of_journey","source","destination","route","dep_time","duration","total_stop","price"])
    

    def fetch_ailline_frequency (self):
        airlines=[]
        frequency=[]
        self.mycursor.execute("""
                              SELECT Airline , COUNT(*) FROM `flights`.`cleaned_flights.csv`
                              GROUP BY Airline 
                              """)
        data=self.mycursor.fetchall()
        for comb in data:
            airlines.append(comb[0])
            frequency.append(comb[1])
        return airlines,frequency
    
    def bussiest_airport (self):
        self.mycursor.execute("""
                                SELECT SOURCE,COUNT(*) FROM (SELECT Source FROM `flights`.`cleaned_flights.csv`
                                UNION ALL
                                SELECT Destination FROM `flights`.`cleaned_flights.csv`) t1
                                GROUP BY Source
                                ORDER BY COUNT(*) DESC""")
        data=self.mycursor.fetchall()
        return data
    

    
    def daily_number_of_flights(self):
        days=[]
        count=[]
        self.mycursor.execute("""
                              SELECT Date_of_Journey, COUNT(*) FROM `flights`.`cleaned_flights.csv`
                              GROUP BY Date_of_Journey
                              """)
        data=self.mycursor.fetchall()
        return data
    
    def airlines_avg_price (self):
        self.mycursor.execute("""SELECT Airline , round(avg(Price)) FROM `flights`.`cleaned_flights.csv`
                              GROUP BY Airline 
                              ORDER BY  round(avg(Price)) DESC """)
        data=self.mycursor.fetchall()
        
        return data 

    def stop_varies_price (self):
        self.mycursor.execute("""
                               select airline , Total_stops,avg(Price) from `flights`.`cleaned_flights.csv`
                                GROUP BY airline , Total_stops
                                ORDER BY avg(Price) DESC""")
        data=self.mycursor.fetchall()
        return data



bd=DB()

print(bd.fetch_source_destination("Banglore", "Delhi"))
print(bd.fetch_ailline_frequency())
print(bd.bussiest_airport())
print(bd.daily_number_of_flights())
print(bd.airlines_avg_price())
print(bd.stop_varies_price())



