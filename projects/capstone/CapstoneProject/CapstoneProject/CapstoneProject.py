import urllib
import re
def main():
    url = "https://finance.yahoo.com/quote/{}/profile?p={}".format("ABEV3.SA","ABEV3.SA")
    f = urllib.urlopen(url)
    htmlPage = f.read()
    sector = re.search("\"sector\":\"(.*?)\"",htmlPage)
    industry = re.search("\"industry\":\"(.*?)\"",htmlPage)
    if(sector):
        print sector.group(1)
    if(industry):
        print industry.group(1)

if  __name__ =='__main__': main() 
