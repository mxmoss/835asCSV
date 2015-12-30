# Description:
# Extract 835 status codes from the wpc-edi website and store as CSV
#
# eg
# <tr class="prod_set current" style="display: table-row;">
#   <td class="code">1</td>
#   <td class="description">Deductible Amount
#     <span class="dates"><br>Start: 01/01/1995</span>
#   </td>
# </tr>
#
# Initial version: 11/03/2015
#
from bs4 import BeautifulSoup

import urllib.request		# this for python 3 and later
import requests

# 835 status codes published online by WPC
myURL = "www.wpc-edi.com/reference/codelists/healthcare/claim-adjustment-reason-codes/"
CSV_OUT = "'{0}', '{1}'"

page = urllib.request.urlopen("http://"+myURL)
soup = BeautifulSoup(page, "html.parser")

# Extract HTML for  <tr class="prod_set current"
rows = soup.find_all('tr',{'class':'prod_set current'})
# put into a python list
data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]

# Output as CSV. Make sure to double-quote single quotes
print("//automatically from www.wpc-edi.com Claim Adjustment Reason Codes ASC X12 External Code Source 139 ")

for item in data:
  #truncate before any "Notes"
  if item[1][0].find('Note:') > 0 :
    print(CSV_OUT.format(item[0][0], item[1][0].replace("'", "''")[:item[1][0].find('Note:')]))
  else:
    print(CSV_OUT.format(item[0][0], item[1][0].replace("'", "''")))
