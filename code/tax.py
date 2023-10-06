import numpy as np, matplotlib.pyplot as plt, csv, os
from itertools import zip_longest

dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

salary_max = 150000.00
salary = np.arange(1.00,salary_max,0.01)
salary_freq = 2 # Monthly=2 or Weekly=1
salary_list, loan_list, tax_list, ni_list, untaxed_list, loss_list, monthly_list = [],[],[],[],[],[],[]
low_tax, med_tax, high_tax = 12570.00, 50270.00, 125140.00
low_wni, high_wni = 242.00, 967.00
low_mni, high_mni = 1048.00, 4189.00
ug_thresh, pg_thresh = 27295.00, 21000.00

# Open CSV File
filename = (dir+"/results/Analysis.csv")
f = open(filename, "w+")
headers = ['Salary','Loan','Taxed','NI','Untaxed','Loss','Monthly']
with open(filename, mode='a') as data:
        datawriter = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL); datawriter.writerow(headers)

for i in salary:
# i = Salary
# Plan 2 UG & PG Student Loan Calculations
    if i <= pg_thresh:
        stu_loan = 0.00
    elif i >= pg_thresh+1.00:
        stu_loan = i * 0.06
        
    if i >= ug_thresh+1.00:
        stu_loan = i * (0.09 + 0.06)
        
    k = i - stu_loan
# National Insurance Calculations
    ini_weekly, ini_monthly = (i/52), (i/12)
    ni_weekly, ni_monthly = (k/52), (k/12)
    if (ini_weekly <= low_wni) or (ini_monthly <= low_mni):
        wni, mni = 0.00, 0.00
    elif (ini_weekly >= low_wni+1.00) or (ini_monthly >= low_mni+1.00):
        wni = (ni_weekly-low_wni) * 0.12
        mni = (ni_monthly-low_mni) * 0.12
        if (ini_weekly >= high_wni+1.00) or (ini_monthly >= high_mni+1):
            wni = ((ni_weekly-high_wni) * 0.02) + (((ni_weekly-(ni_weekly-high_wni))-low_wni) * 0.12)
            mni = ((ni_monthly-high_mni) * 0.02) + (((ni_monthly-(ni_monthly-high_mni))-low_mni) * 0.12)
                
    if salary_freq == 1:
        ni = wni
    elif salary_freq == 2:
        ni = mni
        
# UK Income Tax Calculations
    if i <= low_tax:
        taxed = 0.00
    elif (i >= low_tax+1.00) and (i <= med_tax):
        taxed = (k-low_tax) * 0.2       
    elif (i >= med_tax+1.00) and (i <= high_tax):
        taxed = ((k-med_tax) * 0.4) + (((k-(k-med_tax))-low_tax) * 0.2)
    elif (i >= high_tax+1.00):
        taxed = ((k-high_tax) * 0.45) + (((k-(k-high_tax))-med_tax) * 0.4) + ((((k-(k-high_tax))-(k-(k-med_tax))-low_tax)) * 0.2)
# Other Calculations
    tl = (stu_loan + taxed + ni)                
    untaxed = i - tl
    loss = (tl/i)*100
    monthly = untaxed/12

# Make New Lists
    salary_list.append(i); loan_list.append(stu_loan); tax_list.append(taxed); ni_list.append(ni); untaxed_list.append(untaxed); loss_list.append(loss); monthly_list.append(monthly)
    
# Append CSV File
    y = [i,untaxed,taxed,ni,stu_loan,loss,monthly]
    with open(filename, mode='a') as data:
        datawriter = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL); datawriter.writerow(y)
    # Loop End
    print(f"Salary: {i}/{salary_max}", end="\r")
f.close()
plt.figure()
plt.plot(salary,untaxed_list,label="Untaxed")
plt.plot(salary,tax_list,'r',label="Taxed")
plt.plot(salary,loan_list,'g',label="Loan")
plt.plot(salary,ni_list,'p',label="NI")
plt.legend(loc="best"); plt.xlabel("Salary",labelpad=0.5); plt.ylabel("Value",labelpad=0.5)
plt.savefig(dir+"/results/Tax.png",dpi=1000)
plt.close()
plt.figure()
plt.plot(salary,loss_list,label="Loss")
plt.legend(loc="best"); plt.xlabel("Salary",labelpad=0.5); plt.ylabel("Loss Percentage",labelpad=0.5)
plt.savefig(dir+"/results/Loss_Tax.png",dpi=1000)
plt.close()