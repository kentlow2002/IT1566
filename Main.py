import User as u
import Order as o
import Report as r
import Product as p
import shelve
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from ReportForms import CreateReportForm
from UserForms import CreateUserForm, UserLogInForm


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET","POST"])
def login():
    userLogInForm = UserLogInForm(request.form)
    if request.method == 'POST' and userLogInForm.validate():
        usersDict = {}
        db = shelve.open('Users.db', 'r')
        try:
            usersDict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        try:
            usernameValid = 0
            passwordValid = 0
            for i,j in usersDict.items():
                if userLogInForm.username.data == j.getUsername():
                    usernameValid = 1
                if j.loginCheck(userLogInForm.password.data) == 1:
                    passwordValid = 1

            if passwordValid == 1 and usernameValid == 1:
                return redirect(url_for("buyerIndex"))

        except:
            print("ERROR")

        return redirect(url_for("logout"))
    return render_template('login.html', form=userLogInForm)

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/signup',methods=["GET","POST"])
def signUp():
    createUserForm = CreateUserForm(request.form)
    if request.method == 'POST' and createUserForm.validate():
        usersDict = {}
        db = shelve.open('Users.db', 'c')
        try:
            usersDict = db['Users']
            count = len(usersDict)
        except:
            print("Error in retrieving Users from storage.db.")
            count = 0
        if createUserForm.type.data == "B":
            user = u.Buyer(createUserForm.username.data,createUserForm.email.data, createUserForm.password.data, createUserForm.type.data, count)
        else:
            user = u.Seller(createUserForm.username.data,createUserForm.email.data, createUserForm.password.data, createUserForm.type.data, count)
        usersDict[user.getID()] = user
        db['Users'] = usersDict
        # Test codes
        '''usersDict = db['Users']
        user = usersDict[user.get_userID()]
        print(user.get_firstName(), user.get_lastName(), "was stored in shelve successfully with userID =", user.get_userID())
        db.close()'''
        return redirect(url_for("signedUp"))
    return render_template('signup.html', form=createUserForm)

@app.route('/signedup')
def signedUp():
    return render_template('signedup.html')

@app.route('/userEdit')
def userEdit():
    return render_template('userEdit.html')

@app.route('/buyer/index')
def buyerIndex():
    return render_template('buyerIndex.html')


# staff

# whatever the person doing staff


# reports
@app.route('/staff')
def reportsIndex():
    dailyDict = {}
    db = shelve.open("reportsStorage.db", "c")
    try:
        dailyDict = db["Daily"]
        dailyList = []
        for key in dailyDict:
            report = dailyDict.get(key)
            dailyList.append(report)
    except:
        print("Error in retrieving Daily Records.")
        dailyList = []
    finally:
        db.close()

    monthlyDict = {}
    db = shelve.open("reportsStorage.db", "c")
    try:
        monthlyDict = db["Monthly"]
        monthlyList = []
        for key in monthlyDict:
            report = monthlyDict.get(key)
            monthlyList.append(report)
    except:
        print("Error in retrieving Monthly Records.")
        monthlyList = []
    finally:
        db.close()

    yearlyDict = {}
    db = shelve.open("reportsStorage.db", "c")
    try:
        yearlyDict = db["Yearly"]
        yearlyList = []
        for key in yearlyDict:
            report = yearlyDict.get(key)
            yearlyList.append(report)
    except:
        print("Error in retrieving Yearly Records.")
        yearlyList = []
    finally:
        db.close()

    return render_template('reportsIndex.html', dailyCount=len(dailyList), monthlyCount=len(monthlyList), yearlyCount=len(yearlyList))

@app.route('/staff/create-report', methods=["GET", "POST"])
def reportsCreate():
    createReportForm = CreateReportForm(request.form)
    if request.method == "POST" and createReportForm.validate():
        reportDict = {}
        db = shelve.open("reportsStorage.db", "c")
        try:
            if createReportForm.type.data == "D":
                reportDict = db["Daily"]
            elif createReportForm.type.data == "M":
                reportDict = db["Monthly"]
            else:
                reportDict = db["Yearly"]
        except:
            print("Error in retrieving Reports from storage.db.")


        def dateValidator(dateToValidate):
            date = dateToValidate.split("/")
            if len(date) == 3:
                if int(date[0]) > 31:
                    date[0] = "31"
                if int(date[1]) > 12:
                    date[1] = "12"

                if len(date[0]) == 1:
                    date[0] = "0" + date[0]
                if len(date[1]) == 1:
                    date[1] = "0" + date[1]

                if datetime.strptime("/".join(date), '%d/%m/%Y'):
                    if createReportForm.type.data == "D":
                        date = "/".join(date)
                    elif createReportForm.type.data == "M":
                        del date[0]
                        date = "/".join(date)
                    else:
                        date = date[2]
            elif len(date) == 2:
                if int(date[0]) > 12:
                    date[0] = "12"

                if len(date[0]) == 1:
                    date[0] = "0" + date[0]

                if datetime.strptime("/".join(date), '%m/%Y'):
                    if createReportForm.type.data == "M":
                        date = "/".join(date)
                    else:
                        date = date[2]
            elif len(date) == 1:
                if datetime.strptime("/".join(date), '%Y'):
                    date = date[0]
            return date

        formDate = createReportForm.day.data + "/" + createReportForm.month.data + "/" + createReportForm.year.data
        correctedDate = dateValidator(formDate)
        transaction = open("test.txt", "r")
        if createReportForm.type.data == "D":
            productCount = 0
            productPrice = 0
            for line in transaction:
                list = line.split(", ")
                if dateValidator(list[0]) == correctedDate:
                    productCount += int(list[2])
                    productPrice += float(list[3])
            report = r.Report(createReportForm.type.data, correctedDate, productCount, productPrice)
            reportDict[correctedDate] = report
            db["Daily"] = reportDict

        elif createReportForm.type.data == "M":
            productCount = 0
            productPrice = 0
            for line in transaction:
                list = line.split(", ")
                if dateValidator(list[0]) == correctedDate:
                    productCount += int(list[2])
                    productPrice += float(list[3])
            report = r.Report(createReportForm.type.data, correctedDate, productCount, productPrice)
            reportDict[correctedDate] = report
            db["Monthly"] = reportDict

        else:
            productCount = 0
            productPrice = 0
            for line in transaction:
                list = line.split(", ")
                if dateValidator(list[0]) == correctedDate:
                    productCount += int(list[2])
                    productPrice += float(list[3])
            report = r.Report(createReportForm.type.data, correctedDate, productCount, productPrice)
            reportDict[correctedDate] = report
            db["Yearly"] = reportDict

        transaction.close()
        db.close()

        if createReportForm.type.data == "D":
            return redirect(url_for("reportsDaily"))
        elif createReportForm.type.data == "M":
            return redirect(url_for("reportsMonthly"))
        elif createReportForm.type.data == "Y":
            return redirect(url_for("reportsYearly"))
        else:
            return redirect(url_for("reportsIndex"))
    return render_template('reportsCreate.html', form=createReportForm)

@app.route('/staff/daily-report')
def reportsDaily():
    dailyDict = {}
    db = shelve.open("reportsStorage.db", "r")
    try:
        dailyDict = db["Daily"]
        sortedList = sorted(dailyDict.items(), key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'))
        dailyList = []
        for report in sortedList:
            dailyList.append(report[1])
    except:
        print("Error in retrieving Daily Records.")
        dailyList = []
    finally:
        db.close()

    return render_template('reportsDaily.html', dailyList=dailyList)

@app.route('/staff/monthly-report')
def reportsMonthly():
    monthlyDict = {}
    db = shelve.open("reportsStorage.db", "r")
    try:
        monthlyDict = db["Monthly"]
        sortedList = sorted(monthlyDict.items(), key=lambda x: datetime.strptime(x[0], '%m/%Y'))
        monthlyList = []
        for report in sortedList:
            monthlyList.append(report[1])
    except:
        print("Error in retrieving Monthly Records.")
        monthlyList = []
    finally:
        db.close()
    return render_template('reportsMonthly.html', monthlyList=monthlyList)

@app.route('/staff/yearly-report')
def reportsYearly():
    yearlyDict = {}
    db = shelve.open("reportsStorage.db", "r")
    try:
        yearlyDict = db["Yearly"]
        sortedList = sorted(yearlyDict.items(), key=lambda x: datetime.strptime(x[0], '%Y'))
        yearlyList = []
        for report in sortedList:
            yearlyList.append(report[1])
    except:
        print("Error in retrieving Yearly Records.")
        yearlyList = []
    finally:
        db.close()
    return render_template('reportsYearly.html', yearlyList=yearlyList)

@app.route('/staff/daily-report/delete/<id>', methods=["POST"])
def reportsDeleteDaily(id):
    dailyDict = {}
    db = shelve.open("reportsStorage.db", "w")
    dailyDict = db["Daily"]

    del dailyDict[id.replace('-', '/')]

    db["Daily"] = dailyDict
    db.close()

    return redirect(url_for("reportsDaily"))

@app.route('/staff/monthly-report/delete/<id>', methods=["POST"])
def reportsDeleteMonthly(id):
    monthlyDict = {}
    db = shelve.open("reportsStorage.db", "w")
    monthlyDict = db["Monthly"]

    del monthlyDict[id.replace('-', '/')]

    db["Monthly"] = monthlyDict
    db.close()

    return redirect(url_for("reportsMonthly"))

@app.route('/staff/yearly-report/delete/<id>', methods=["POST"])
def reportsDeleteYearly(id):
    yearlyDict = {}
    db = shelve.open("reportsStorage.db", "w")
    yearlyDict = db["Yearly"]

    del yearlyDict[id]

    db["Yearly"] = yearlyDict
    db.close()

    return redirect(url_for("reportsYearly"))

if __name__ == '__main__':
    app.run(debug=True)
