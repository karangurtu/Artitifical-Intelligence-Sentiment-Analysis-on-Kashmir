#!/usr/bin/env python
# Python version 2.7.6

from fpdf import FPDF, HTMLMixin
import datetime
import time

csv_in = "twitter-out.csv"
pdf_out = "twitter-out.pdf"
title = "Trading Summary - 2015"
subject = "Subject"
author = "Author"
keywords = "Keywords"
creator = "Creator"

def format_currency(value):
   if value < 0:
     results = '${:,.2f}'.format(value)
     value = "(" + results.replace("-","") + ")"
   else:
     value =  '${:,.2f}'.format(value)
   return value

header = """
<table align="center" width="100%">
<thead><tr>
<th width="5%">#</th><th width="9%">Date</th><th width="6%">Buy/Sell</th>
<th width="4%">QTY</th><th width="25%">Security</th><th width="6%">Price</th>
<th width="9%">Debit</th><th width="9%">Credit</th><th width="10%">Commission</th>
<th width="16%">Total Amount</th>
</tr></thead>
"""

footer_commission = 0
footer_debit = 0
footer_credit = 0
footer_total_amount = 0
counter = 1
split = ","
join_r = "</td><td align=\"right\">"
join = "</td><td>"
html_out = ""

for line in reversed(list(open(csv_in))):
   if len(line.strip()) != 0 :
     line = line.strip()
     column = line.split(split)
     if column[2] == "Buy" or column[2] == "Sell" or column[2] == "Expired":
       row_counter = '{0:04d}'.format(counter)
       transaction_date = column[0]
       buy_sell = column[2]
       qty = column[5]
       security = column[4]
       price = column[6]
       if price == "":
         price = "0"
       total_amount = column[8]
       currency = column[9]
       transaction_date = (datetime.datetime.strptime\
         (transaction_date, "%Y-%m-%d").strftime("%a %b %d"))
       qty = abs(int(qty))
       price = float(price)
       total_amount = float(total_amount)
       amount = qty * price * 100
       amount = int(amount)

       abs_total_amount = abs(float(total_amount))
       if column[8] >= "0" and  column[8] <= "1":
         commission = 0
       else:
         commission = abs(abs_total_amount - amount)
       if total_amount <= 1:
         debit = amount
         credit = 0
       else:
         debit = 0
         credit = amount
       if debit > abs_total_amount:
         credit = debit
         commission = debit
         debit = 0

       footer_debit = (footer_debit + debit)
       footer_credit = (footer_credit + credit)
       footer_commission = (footer_commission + commission)
       footer_total_amount = (footer_total_amount + total_amount)

       qty = str(abs(qty))
       price = format_currency(price)
       debit = format_currency(debit)
       credit = format_currency(credit)

       if debit == "$0.00":
         debit = " "
       if credit == "$0.00":
         credit = " "
       commission = format_currency(commission)
       if commission == "0":
         commission = ""
       total_amount = format_currency(total_amount)
       counter = counter + 1
       mod = counter % 2
       if mod == 1:
         bgcolor = "<tr bgcolor=\"#FFFFFF\"><td>"
         fcolor = "<tr bgcolor=\"#E1E1E1\"><td>"
       else:
         bgcolor = "<tr bgcolor=\"#E1E1E1\"><td>"
         fcolor = "<tr bgcolor=\"#FFFFFF\"><td>"

       if "(" in total_amount:
         neg_pos = join_r + "<red>" + total_amount + " " + currency + "<black>"
       else:
         neg_pos = join_r + total_amount + " " + currency

       if counter == 1000:
         over_flow = "<tr></tr>\n" * 10
       else:
         over_flow = ""

       row = (bgcolor + row_counter + join + transaction_date + join + buy_sell + join \
         + qty + join + security + join_r + price + join_r + debit + join_r + credit + join_r \
         + commission + neg_pos + "</td></tr>\n" + over_flow)

       print row_counter
       html_out = html_out + row

pl = (footer_debit + footer_commission)
pl_percent = ((footer_credit - (pl)) / pl * 100)
pl_debit = format_currency(pl)
pl_debit = "(" + pl_debit + ")"
f_debit = format_currency(footer_debit)
f_credit = format_currency(footer_credit)
f_commission = format_currency(footer_commission)
f_total_amount = format_currency(footer_total_amount)
pl_percent = '{:.2f}'.format(pl_percent)

td = "<td> </td>"
tdr = "<td align=\"right\"><b>"
usd = " USD</b></td></tr>\n"
a = td + td + td + td + tdr
b = "</b></td>" + tdr
c = td * 10
d = td * 7

if "(" in f_total_amount:
   pl_percent = "(" + pl_percent + "%)</b></td>"
   n_s = "<red>" + pl_percent + tdr + f_total_amount + usd + "<black>"
   n_s = n_s.replace("-","")
   ns = "<red><td></td>" + tdr + f_total_amount + usd + "<black>"
else:
   n_s = pl_percent + "% </b></td>" + tdr + f_total_amount + usd
   ns = "<td></td>" + tdr + f_total_amount + usd

f1 = (fcolor + a + "Subtotal:</b></td>" + td + tdr + f_debit + b + f_credit + b \
   + f_commission + tdr + ns)
f2 = ("<tr>" + c + "</tr>\n")
f3 = ("<tr>" + d + tdr + "Total Debit:</b></td>" + td + tdr + "<red>" + pl_debit + usd + "<black>")
f4 = ("<tr>" + d + tdr + "Total Credit:</b></td>" + td + tdr + f_credit + usd)
f5 = ("<tr>" + d + tdr + "P/L:</b></td>" + tdr + n_s)

footer = f1 + f2 + f2 + f3 + f4 + f5 + f2 + f2 + "</tbody></table>"
html = header + html_out + footer

class MyFPDF(FPDF, HTMLMixin):
   def footer(this):
     this.set_y(-25)  #-25
     this.set_font('Arial','I',10)
     this.set_text_color(0,0,0)
     this.cell(0,10,'PAGE %s OF {nb}' % this.page_no(),0,0,'C')

pdf=MyFPDF('P','mm','letter')
pdf.set_top_margin(margin=18)  #18
pdf.set_auto_page_break(True, 27) #27
pdf.add_page()
pdf.alias_nb_pages()
pdf.set_font("Arial", style="B", size=14)
pdf.cell(200, 5,'Your Broker', ln=1)
pdf.set_font("Arial", size=12)
pdf.cell(200, 5,'Trading Summary for 2015', ln=1)
pdf.cell(200, 5,'Account No: ########', ln=1)
pdf.cell(200, 5,'SIN: ########', ln=1)
pdf.cell(200, 5,'Phone: 1 (888) ######', ln=1)
pdf.cell(200, 5,' ', ln=1)
pdf.set_font("Arial", style="B", size=14)
pdf.cell(200, 5,'John Doe Smith', ln=1)
pdf.set_font("Arial", size=12)
pdf.cell(200, 5,'1234 Main Street', ln=1)
pdf.cell(200, 5,'Sin City 55416', ln=1)
pdf.cell(200, 5,'Phone: ########', ln=1)
pdf.cell(200,5,'Email: ######@gmail.com',0,1)
pdf.set_title(title)
pdf.set_subject(subject)
pdf.set_author(author)
pdf.set_keywords(keywords)
pdf.set_creator(creator)
pdf.write_html(html)
pdf.output(pdf_out)

input("\n\nPress the Enter key to exit.")