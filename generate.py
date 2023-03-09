"""
WIP:
Functionality (planned): Get sensor data from database and generate report
with graphs.
So far only creates one graph. 
Plan is to integrate with this repo: "https://github.com/rushithkaru/Aws_telemetry"
"""

from fpdf import FPDF
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime as dt
import creds
print(os.environ.get("timedb"))

def get_data(device,start,end):
    

    df = pd.DataFrame(columns=['DateTime','sensor_id','temp','cpu'])
    CONNECTION = creds.con_string

    with psycopg2.connect(CONNECTION) as conn:
            cursor = conn.cursor()
            start = dt.date(2023,3,7) 
            print(start.__class__)
            next = start + dt.date.resolution
            query = "SELECT * FROM sensor_data WHERE time > '%s/%s/%s' AND sensor_id = %s;" % (start.year,start.month,start.day,str(device))
            
            print(query)
            cursor.execute(query)
            count = 0
            tableData = cursor.fetchall()
            data = []
            for ind in tableData:
                 data.append({'DateTime' : ind[0], 'sensor_id' : ind[1],'temp' : ind[2],'cpu' : ind[3]})

            df = pd.DataFrame.from_records(data)
            cursor.close()

    return df
    

def create_graphs(device,start,end):
      
        df = get_data(device,start,end)
        print(pd.to_datetime(df['DateTime'][0]))
    
        fig, ax = plt.subplots(figsize = (15, 7))

        sns.lineplot(ax = ax, x='DateTime', y='temp', data=df).set_title('Title')

        plt.xlabel('DateTime')
        plt.ylabel('Magnitude (Mw)')
        #plt.show()       
        plt.savefig('graphs/trial2.png')
        create_report()


def create_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=12)
    pdf.cell(txt="hello world")
    pdf.image('graphs/trial2.png', x=50, y=100, w=50, h=50)
    pdf.output("reports/hello_world.pdf")

if __name__ == "__main__":
    
    start = dt.date(2023,3,7) 
    end = dt.date(2023,3,10)
    create_graphs(2,start,end)