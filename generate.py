"""
Functionality (not implemented): Get sensor data from database and generate report
with graphs.

"""

from fpdf import FPDF
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import os
print(os.environ.get("timedb"))

def get_data():
    

    df = pd.DataFrame(columns=['DateTime','sensor_id','temp','cpu'])

    with psycopg2.connect(CONNECTION) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM sensor_data WHERE sensor_id = 3;"
            cursor.execute(query)
            count = 0
            tableData = cursor.fetchall()
            data = []
            for ind in tableData:
                 data.append({'DateTime' : ind[0], 'sensor_id' : ind[1],'temp' : ind[2],'cpu' : ind[3]})

            df = pd.DataFrame.from_records(data)
            cursor.close()
    print(pd.to_datetime(df['DateTime'][0]))
    df['date'] = pd.to_datetime(df['DateTime'])

    fig = plt.figure()
    # Plot the temperature data
    plt.plot(df['date'], df['temp'])

    # Set the x-axis label and format
    plt.xlabel('Date')
    plt.xticks(rotation=45, ha='right')

    # Set the y-axis label
    plt.ylabel('Temperature')

    # Set the title of the plot
    plt.title('Temperature Data')
    plt.savefig('graphs/trial.png')
    #plt.show()
    

def create_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=12)
    pdf.cell(txt="hello world")
    pdf.image('graphs/trial.png', x=50, y=100, w=50, h=50)
    pdf.output("reports/hello_world.pdf")

if __name__ == "__main__":
    get_data()
    create_report()