import json
import sys
import re
from urllib import urlopen
from bs4 import BeautifulSoup

# to get data programmatically:
#optionsUrl = 'http://finance.yahoo.com/q/op?s=AAPL+Options'
#optionsPage = urlopen(optionsUrl)
#s = optionsPage.read()
#print s
#fhandle = open("aapl.dat", "w")
#fhandle.write(s)
#close(fhandle)

def contract(item):
  item_string = str(item)
  contract_symbol = re.findall(r"([A-Z]+)\d.*[CP]", item_string)
  contract_date = re.findall("[A-Z]+(\d+)[CP]", item_string )
  contract_type =  re.findall("[A-Z]+\d+([CP])", item_string)
  constract_price = re.findall("[A-Z]+\d+[CP](\d+)", item_string)
  return {"Symbol":contract_symbol[0], \
          "Date": contract_date[0], \
          "Type": contract_type[0], \
          "Strike": float(int(constract_price[0]))/10.0 }


def contractAsJson(filename):

  filehandle = open(filename)
  optionsPageText = filehandle.read()
  soupText = BeautifulSoup(optionsPageText)

  strike_dates = soupText.select('a')  # re.compile('.*')})
  dateUrls = []
  for kid in strike_dates:
    if re.search(r"s=[A-Z]+&amp;m=", str(kid)):
      aDate = re.findall("[\"](.*)[\"]", str(kid))
      dateUrls.append("http://finance.yahoo.com" + aDate[0])
  
  curr_price_bs = soupText.findAll(attrs={'class':'time_rtq_ticker'})
  currPrice = 0.0
  for kid in curr_price_bs[0]:
    price = re.findall("\d+\.\d+", str(kid))
    currPrice = float(price[0])
  
  optionsTable = []
  # yfnc_h is in the money
  # yfnc_tabledata1 is out of the money

  # first, in the money calls  
  for y in soupText.findAll( attrs={'class': "yfnc_h", 'nowrap': ''}):
    if "nowrap" in str(y): #and re.match("[A-Z]+\d+([C])", str(y)):
        if re.match("[A-Z]+\d+([C])", [x.text for x in y.parent.contents][1]):
            optionsTable.append( [x.text for x in y.parent.contents] )

  # now, out of the money calls
  for y in soupText.findAll( attrs={'class': "yfnc_tabledata1", 'nowrap': ''}):
      if "nowrap" in str(y):
        if re.match("[A-Z]+\d+([C])", [x.text for x in y.parent.contents][1]):
            optionsTable.append( [x.text for x in y.parent.contents] )

  # now, out of the money puts
  for y in soupText.findAll( attrs={'class': "yfnc_tabledata1", 'nowrap': ''}):
      if "nowrap" in str(y):
        if re.match("[A-Z]+\d+([P])", [x.text for x in y.parent.contents][1]):
            optionsTable.append( [x.text for x in y.parent.contents] )

  # now, in the  money puts
  for y in soupText.findAll( attrs={'class': "yfnc_h", 'nowrap': ''}):
      if "nowrap" in str(y):
        if re.match("[A-Z]+\d+([P])", [x.text for x in y.parent.contents][1]):
            optionsTable.append( [x.text for x in y.parent.contents] )

  optionQuotes = []
  for item in optionsTable:
    if len(item) == 8:
      data = contract(item)
      data["Strike"] = item[0]
      data["Last"] = item[2]
      data["Change"] = item[3]
      data["Bid"] = item[4]
      data["Ask"] = item[5]
      data["Vol"] = item[6]
      data["Open"] = item[7]

      optionQuotes.append(data)

  # sort is stable, so if there's a tie on open interest, we keep existing order, which is what
  # was specified
  optionQuotes.sort(lambda x, y: 1 if (int(x["Open"].replace(",", "")) < int(y["Open"].replace(",", "" ))) \
                            else -1 if (int(x["Open"].replace(",", "")) > int(y["Open"].replace(",", "" ))) \
                            else 0 )
  
  jsonQuoteData = json.dumps({"currPrice":currPrice, "dateUrls":dateUrls, "optionQuotes":optionQuotes}, sort_keys=True, indent=4, separators=(',', ': '))
  
  return jsonQuoteData


filehandle = open("f.dat")
optionsPageText = filehandle.read()
soup = BeautifulSoup(optionsPageText)

#print soup.title
#print soup.a
alinks = soup.find_all('a')
for link in alinks:
  #if re.search("/q/op\?s=F&amp;m", str(link)):
  #  print str(link)
  if re.search("F140816C00009000", str(link)):
    #print str(link)
    #print str(link.parent)
    #print str(link.parent.parent)
    for s in link.parent.parent.contents:  
      print str(s)
