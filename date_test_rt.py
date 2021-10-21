from datetime import date, datetime, timedelta
import csv
import random
import time

class WRITE:
    def __init__(self):
        #self.count=0
        self.tgl_temp=0
        self.w=0
    def write_csv(self, step):
        self.step = step
        while True:
            with open('./static/sensor_hour_rt.csv', mode='a'):
                with open('./static/sensor_hour_rt.csv', mode='r+', newline='') as file:
                    #print(f"count: {self.count}")
                    reader = csv.reader(file, delimiter=",")
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                    self.tgl = datetime.now().replace(microsecond=0)
                    header = ['tgl','temp','hum','power','energy']
                    rng1 = round(random.uniform(0,10),3)
                    rng2 = round(random.uniform(0,50),3)
                    rng3 = round(random.uniform(0,100),3)
                    
                    if self.tgl.day != self.tgl_temp:
                        print("energy reset")
                        self.w = 0
                    self.tgl_temp = self.tgl.day
                    print(f"{self.tgl}")
                    # cumulative energy
                    '''
                    hour = f"{tgl.hour}:{tgl.minute}:{tgl.second}"
                    if hour == '0:0:0':
                        w = 0
                    '''
                    self.w = round(self.w + rng3/(3600/self.step), 3)
                    #w = round(w + rng3, 2)
                    row = [self.tgl, rng1, rng2, rng3, self.w]

                    #way to write to csv file
                    #print(enumerate(reader))
                    rowcount = sum(1 for num in reader)     #row count
                    if rowcount == 0:
                        writer.writerow(header)
                        print('header written, row count:',rowcount)
                    writer.writerow(row)
                    print("row written, row count",rowcount)

                    time.sleep(self.step)
                    #time.sleep(step)

if __name__=="__main__":
    print("date sampling")
    go=WRITE()
    go.write_csv(5)