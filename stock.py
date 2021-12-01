import pandas as pd

from playwright.sync_api import sync_playwright 
from bs4 import BeautifulSoup

class Stock(object):
    line_item_code = {}
    income_statement = {}
    balance_sheet = {}
    cash_flows = {}

    def __init__(self, symbol=""):
        url = "https://investors.sgx.com/_security-types/stocks/%s" % symbol

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.on("response", lambda response: self.process_response(response))
            page.goto(url, wait_until="networkidle", timeout=90000)
            browser.close()

    def process_response(self, response):
        if 'Fundamentals' in response.url:
            soup = BeautifulSoup(response.body(), 'lxml')
            financialstatements = soup.find('financialstatements')
            if financialstatements:
                self.get_line_item_code(financialstatements)
                self.get_annual_reports(financialstatements)
    
    def get_line_item_code(self, financialstatements):
        coamap = financialstatements.find('coamap')
        mapitems = coamap.find_all('mapitem')
        
        for mapitem in mapitems:
            self.line_item_code[mapitem.get('coaitem')] = mapitem.text
            statement_type = mapitem.get('statementtype')
            if statement_type == 'INC':
                self.income_statement[mapitem.text] = []
            if statement_type == 'BAL':
                self.balance_sheet[mapitem.text] = []
            if statement_type == 'CAS':
                self.cash_flows[mapitem.text] = []

    def get_annual_reports(self, financialstatements):
        annualperiods = financialstatements.find('annualperiods')
        fiscalperiods = annualperiods.find_all('fiscalperiod')
        fiscalyears = [fiscalperiod.get('fiscalyear') for fiscalperiod in fiscalperiods]
        
        for fiscalperiod in fiscalperiods:    
            statements = fiscalperiod.find_all('statement')

            for statement in statements:
                statement_type = statement.get('type')
                lineitems = statement.find_all('lineitem')
                
                for lineitem in lineitems:
                    line_item_label = self.line_item_code[lineitem.get('coacode')]
                    
                    if statement_type == 'INC':
                        self.income_statement[line_item_label].append(lineitem.text)
                    
                    if statement_type == 'BAL':
                        self.balance_sheet[line_item_label].append(lineitem.text)
                    
                    if statement_type == 'CAS':
                        self.cash_flows[line_item_label].append(lineitem.text)

        self.income_statement = pd.DataFrame.from_dict(self.income_statement, orient='index', columns=fiscalyears)
        self.balance_sheet = pd.DataFrame.from_dict(self.balance_sheet, orient='index', columns=fiscalyears)
        self.cash_flows = pd.DataFrame.from_dict(self.cash_flows, orient='index', columns=fiscalyears)