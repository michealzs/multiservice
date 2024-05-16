import requests
from bs4 import BeautifulSoup


# Make the user agent and other headers dynamic

class StockScraper:
    def __init__(self, stock):
        self.stock = stock
        self.hurl = f'https://finance.yahoo.com/quote/{stock}/history?p={stock}'
        self.url = f'https://finance.yahoo.com/quote/{stock}/key-statistics?p={stock}'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47'
        }
        self.temp = {}

    def val(self, x):
        return self.lindex[x].string

    def scrape_stock_data(self):
        page = requests.get(self.url, headers=self.headers)
        soup_html = BeautifulSoup(page.text, 'html.parser')
        td = soup_html.find_all('td')
        c = 0

        for x in td:
            s = x.strings
            for r in s:
                xstring = str(r)
                if xstring == "Beta (5Y Monthly)":
                    self.xindex = td.index(x)
                    print(self.xindex)
                if xstring == "Levered Free Cash Flow":
                    self.yindex = td.index(x)
                    print(self.yindex)

        pp = [
            "Beta (5Y Monthly)", "52-Week Change", "S&P500 52-Week Change",
            "52 Week High", "52 Week Low", "50-Day Moving Average",
            "200-Day Moving Average", "Avg Vol (3 month)", "Shares Outstanding",
            "Most Recent Quarter", "Profit Margin", "Operating Margin",
            "Return on Assets", "Return on Equity", "Revenue",
            "Revenue Per Share", "80.50%", "Gross Profit", "Total Cash",
            "Total Debt", "Book Value Per Share", "Operating Cash Flow"
        ]

        self.lindex = td[self.xindex:self.yindex]

        for ind in self.lindex:
            strindex = ind.strings
            si = self.lindex.index(ind) + 1
            for strin in strindex:
                for p in pp:
                    xs = str(strin)
                    if len(xs) > 1:
                        if xs == "(ttm)":
                            continue
                        elif xs == "(yoy)":
                            continue
                        elif xs == "(mrq)":
                            continue
                        elif xs == p:
                            self.temp[p] = self.val(si)

        hd = soup_html.find("div", id="quote-market-notice")
        self.temp["market time"] = hd.string
        self.temp["symbol"] = self.stock

        soup_sym = soup_html.find_all('fin-streamer')

        for q in soup_sym:
            fiv = soup_sym[-5].get_text()
            print("=====><======", q.get_text())
            print(q.get_text(), "<==================> text")
            if fiv:
                self.temp["price"] = soup_sym[-5].get_text()
                self.temp["market_change"] = soup_sym[-4].get_text()
                self.temp["market_change_percent"] = soup_sym[-3].get_text()
            else:
                self.temp["price"] = soup_sym[-4].get_text()
                self.temp["market_change"] = soup_sym[-3].get_text()
                self.temp["market_change_percent"] = soup_sym[-2].get_text()

        hh = soup_html.find("div", id="quote-header-info")
        for h in hh.strings:
            if c == 0:
                self.temp["name"] = h
                c += 1
            elif c == 1:
                break

        hpage = requests.get(self.hurl, headers=self.headers)
        hsoup_html = BeautifulSoup(hpage.text, 'html.parser')
        tdt = hsoup_html.find_all('td')

        for x in tdt[:7]:
            self.temp["day_date"] = tdt[0].get_text()
            self.temp["day_open"] = tdt[1].get_text()
            self.temp["day_high"] = tdt[2].get_text()
            self.temp["day_low"] = tdt[3].get_text()
            self.temp["day_close"] = tdt[4].get_text()
            self.temp["day_volume"] = tdt[6].get_text()

        for x in tdt:
            self.temp["previous_date"] = tdt[7].get_text()
            self.temp["previous_open"] = tdt[8].get_text()
            self.temp["previous_high"] = tdt[9].get_text()
            self.temp["previous_low"] = tdt[10].get_text()
            self.temp["previous_close"] = tdt[11].get_text()
            self.temp["previous_volume"] = tdt[13].get_text()

        return self.temp


# Usage
#scraper = StockScraper('TSLA')
#stock_data = scraper.scrape_stock_data()
#print(stock_data)
