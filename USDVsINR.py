import pandas
import time
import os
import sys
import requests
import datetime
from bs4 import BeautifulSoup


class ReadData():
    def ReadData(self, url):
        print("1")
        self.url = url
        # use direct link in pandas
        self.HTMLData = requests.get(url)
        self.soup = BeautifulSoup(self.HTMLData.content, 'html.parser')
        # uccResultAmount is unique in entire file
        self.FindSpanField = self.soup.find_all('span', {'class': 'uccResultAmount'})
        self.FinalVal = [span.get_text() for span in self.FindSpanField][0]
        print(str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")), self.FinalVal)
        return (str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")), self.FinalVal)


class WriteDataToFile():
    def WriteDataToFile(self, FileName, Row):
        print("2")
        self.FileName = FileName
        self.Row = Row[0] + ',"' + Row[1] + ''

        with open(self.FileName, 'a') as File:
            File.write(self.Row + '\n')


def main():
    FIleName = 'USDVsINR.csv'
    # Please change the below two parameter to c, Because it will be same till market opens
    IntervalTimeInMins = 1
    WindowTimeInMins = 10

    IntervalTimeInMins = IntervalTimeInMins * 60
    WindowTimeInMins = WindowTimeInMins * 60
    # url = 'https://www.xe.com/'
    url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=INR'
    # using direct link as website has static address
    Ob_ReadData = ReadData()

    while (IntervalTimeInMins <= WindowTimeInMins):
        print("inside loop")
        Row = Ob_ReadData.ReadData(url)

        Ob_WriteDataToCSV = WriteDataToFile()
        Ob_WriteDataToCSV.WriteDataToFile(FIleName, Row)
        # sleep for Interval
        time.sleep(IntervalTimeInMins)
        IntervalTimeInMins += IntervalTimeInMins

    if (os.path.exists(FIleName)):
        # readfile into pandas DF
        df = pandas.read_table(FIleName, header=None, sep=',', names=['DateTime', 'INRvsUSD'], parse_dates=True)
        print(df.head())
        print(df.dtypes)
        # draw graph
        df.set_index('DateTime', inplace=True)

        df.plot()
    else:
        print("File wan't created, Exiting from the program")
        exit(1)


if __name__ == '__main__':
    main()