#Change the value of included variables to their original, or what they would be
#if you start the program for the first time
def initialize():
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global c1, c2
    global deactivated
    #the above globals are set to their initial values (down below),
    #so that when you initialize/reset your code, balance, last_month/day,
    #last_country and deactivated status are reset
    cur_balance_owing_intst = 0.0
    cur_balance_owing_recent = 0.0

    last_update_day, last_update_month = 0, 0
    last_country = None
    last_country2 = None
    deactivated = False

#Compare the day1 with day2 and month1 with month2, check if equal, then check
#if first date (day1, month1) is later than (day2, month2). If so, return False,
#else return True (day1 ==day2 or later).
def date_same_or_later(day1, month1, day2, month2):
    if day1 == day2 and month1 == month2:
        return True
    elif month1 > month2:
        return False
    elif month2 == month1 and day1 > day2:
        return False
    else:
        return True

#checks to see if all 3 country names are different, meaning the card should
#be deactivated and return error
def all_three_different(c1, c2, c3):
    global deactivated #f all 3 countries are different it changes to True,
    #global changes that variable in the other fnc too
    if c1 != None and c2 != None and c1 != c2 and c2 != c3 and c1 != c3:
        deactivated = True
        return True
    else:
        return False
#If last_update_month != month, calculate interest: check if the new month is
#the next month from last_update_month, if so cur_balance_owing_intst is just 1.05x
#then update the cur_balance_owing_recent and cur_balance_owing_intst
#if the month gap is larger than 1, calculate interest on the current cur_balance_owing_recent
#then do interest again but including the cur_balance_owing_recent moved into intst
def interest_calculator(last_day_parameter, last_month_parameter, day, month):
    global last_update_day, last_update_month
    global cur_balance_owing_intst, cur_balance_owing_recent
    #globals the balances and the last updated month, as they need to be found
    #for use in the function that the interest_calculator function is nested in
    if last_update_month != month:
        if month == last_update_month + 1:
            cur_balance_owing_intst *= 1.05
            cur_balance_owing_intst += cur_balance_owing_recent
            cur_balance_owing_recent = 0
        elif month > last_update_month:
            if cur_balance_owing_intst != 0:
                cur_balance_owing_intst *= (1.05)
            cur_balance_owing_intst += cur_balance_owing_recent
            cur_balance_owing_recent = 0
            cur_balance_owing_intst *= 1.05**(month-last_update_month - 1)
    else:
        return None

#Run all_three_different, then check if deactivated or date is mismatched. If so
#return error. If not, then run interest_calculator and update variables.
def purchase(amount, day, month, country):
    global deactivated
    global last_country, last_country2
    global last_update_day, last_update_month
    global cur_balance_owing_recent
    #update the above variables, for other functions such as amount_owed
    all_three_different(last_country, last_country2, country)
    if deactivated or date_same_or_later (
    last_update_day, last_update_month, day, month) == False:
        return "error"
    if date_same_or_later(
    last_update_day, last_update_month, day, month
    ) == True and all_three_different(
    last_country,last_country2,country) == False:
        interest_calculator(last_update_day, last_update_month, day, month)
        last_update_day = day
        last_update_month = month
        last_country = last_country2
        last_country2 = country
        cur_balance_owing_recent += amount

#check if the date is mismatched with date_same_or_later, if not, then update
#the day and month for future operations, while returning the total balance
#(cur_balance_owing_recent + cur_balance_owing_intst), if the date is mismatched
#return error
def amount_owed(day, month):
    global last_update_day, last_update_month
    #updates the day and month when you check the account balance
    if date_same_or_later(last_update_day, last_update_month, day, month):
        interest_calculator(last_update_day, last_update_month, day, month)
        last_update_day = day
        last_update_month = month
        return cur_balance_owing_recent + cur_balance_owing_intst
    else:
        return "error"

#Check if the date is mistmatched, if so return error. If not, then calculate
#interest with interest_calculator, then update the date. Check which account to
#pay first, if the cur_balance_owing_intst is 0, just pay off cur_balance_owing_recent
#if the balance goes into negatives, return error. If cur_balance_owing_intst >0
#then pay off that account first, before taking the remainder to pay off
#cur_balance_owing_recent
def pay_bill(amount, day, month):
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    #update the month and day with last_update_day/month, then update
    #cur_balance_owing_intst and cur_balance_owing_recent for future operations
    if date_same_or_later(last_update_day, last_update_month, day, month):
        interest_calculator(last_update_day, last_update_month, day, month)
        last_update_day = day
        last_update_month = month
        if cur_balance_owing_intst != 0:
            if cur_balance_owing_intst < amount:
                if cur_balance_owing_recent - (amount - cur_balance_owing_intst) < 0:
                    return "error"
                else:
                    cur_balance_owing_recent -= (amount - cur_balance_owing_intst)
                cur_balance_owing_intst = 0
            else:
                cur_balance_owing_intst -=amount
        else:
            if (cur_balance_owing_recent -amount) < 0:
               return "error"
            else:
                cur_balance_owing_recent -= amount
    else:
        return "error"

initialize()

# if __name__ == "__main__":
#     print ("TEST 1") #check for payments/interest calculation
#     purchase(50, 1, 1, "Canada") #50
#     purchase(50, 2, 1, "Canada") #50
#     print("Now owing:", amount_owed(1, 2))  #100
#     print("Now owing:", amount_owed(1,3)) #100 x 1.05 = 105
#     pay_bill(105, 2,3)#-105-105
#     print("Now owing:", amount_owed(2,3))#105-105 = 0
#
#     initialize()
#     print("TEST 2") #check for deactivation through countries
#     purchase(100,1,1,"Canada")
#     print("Now owing:", amount_owed(1, 1)) #100
#     purchase(1000, 5,1,"Argentina")
#     print("Now owing:", amount_owed(5, 1)) #1100
#     print(purchase(10000000000,19,1,"South Africa")) #error
#     print("Now owing:", amount_owed(20, 1)) #1100 - no change
#
#     initialize()
#     print("TEST 3") #paying off intst balance, then recent balance
#     purchase(20, 1,1, "Canada")
#     print("Now owing:", amount_owed(1,1))#20
#     print("Now owing:", amount_owed(2,5))#20 * 1.025 **3, interest on 2,3,4 months
#     purchase(20,10,5,"Canada") #23.1525 +20
#     print("Now owing:", amount_owed(25,5))
#     pay_bill(40,28,5)
#     print("Now owing:", amount_owed(30,5)) #pay off intst balance, leaves (43.1525-40) left in recent bal
#
#     initialize()
#     print("TEST 4")#what if you pay too much money?
#     purchase(50, 1, 1, "Canada")
#     print("Now owing:", amount_owed(1,1)) #50
#     purchase(50, 5, 4, "Canada")
#     print("Now owing:", amount_owed(5,4)) #50 + 50 * 1.05**2
#     pay_bill(110, 5,4) #should be an error
#     print("Now owing:", amount_owed(8,4))
#
#     initialize()
#     print("TEST 5") #if date is earlier than last update
#     purchase(50, 21, 1, "Canada")
#     print("Now owing:", amount_owed(21,1)) #50
#     purchase(50,10,1, "Germany")
#     print("Now owing:", amount_owed(10,1)) #error
#
#     initialize()
#     print("TEST 6") #two different countries, one same country, then another different country
#     purchase(50, 1, 1, "Canada") #50
#     print("Now owing:", amount_owed(1,1))#50
#     purchase(50, 2, 1, "India")
#     print("Now owing:", amount_owed(2,1))#50
#     purchase(50,5,1,"India")
#     print("Now owing:", amount_owed(5,1))#150
#     purchase(20, 20, 1, "France")
#     print("Now owing:", amount_owed(20,1))#170
#     purchase(35, 25, 1, "Jamaica")
#     print("Now owing:", amount_owed(25,1)) #170 still - error
#
#     initialize()
#     print("TEST 7") #not fully paying off account
#     purchase(50,1,1,"Canada")
#     print("Now owing:", amount_owed(5,10)) #50 * 1.05**8
#     purchase(20,6,10, "Korea")
#     pay_bill(70,7,10)
#     print("Now owing:", amount_owed(7,10)) #73.87 - 70 + 20