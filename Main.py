import User as u
import Order as o
import Report as r
import Product as p
import shelve
from flask import Flask, render_template, request, redirect, url_for
from ReportForms import CreateReportForm


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signUp():
    return render_template('signup.html')

@app.route('/buyer/index')
def buyerIndex():
    return render_template('buyerIndex.html')


# staff
@app.route('/staff/index')
def staffIndex():
    return render_template('staffIndex.html')


# reports
@app.route('/reports')
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

@app.route('/reports/create', methods=["GET", "POST"])
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
            if int(date[0]) > 31:
                date[0] = "31"
            if int(date[1]) > 12:
                date[1] = "12"

            if len(date[0]) == 1:
                date[0] = "0" + date[0]
            if len(date[1]) == 1:
                date[1] = "0" + date[1]

            if createReportForm.type.data == "D":
                date = "/".join(date)
            elif createReportForm.type.data == "M":
                del date[0]
                date = "/".join(date)
            else:
                date = date[2]
            return date



        transaction = open("test.txt", "r")
        if createReportForm.type.data == "D":
            productCount = 0
            productPrice = 0
            for line in transaction:
                list = line.split(", ")
                if dateValidator(list[0]) == dateValidator(createReportForm.date.data):
                    productCount += int(list[2])
                    productPrice += float(list[3])
            report = r.Report(createReportForm.type.data, createReportForm.date.data, productCount, productPrice)
            reportDict[report.get_reportDate()] = report
            db["Daily"] = reportDict

        elif createReportForm.type.data == "M":
            productCount = 0
            productPrice = 0
            for line in transaction:
                list = line.split(", ")
                if dateValidator(list[0]) == dateValidator(createReportForm.date.data):
                    productCount += int(list[2])
                    productPrice += float(list[3])
            report = r.Report(createReportForm.type.data, createReportForm.date.data, productCount, productPrice)
            reportDict[report.get_reportDate()] = report
            db["Monthly"] = reportDict

        else:
            productCount = 0
            productPrice = 0
            for line in transaction:
                list = line.split(", ")
                if dateValidator(list[0]) == dateValidator(createReportForm.date.data):
                    productCount += int(list[2])
                    productPrice += float(list[3])
            report = r.Report(createReportForm.type.data, createReportForm.date.data, productCount, productPrice)
            reportDict[report.get_reportDate()] = report
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

@app.route('/reports/daily')
def reportsDaily():
    dailyDict = {}
    db = shelve.open("reportsStorage.db", "r")
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
    return render_template('reportsDaily.html', dailyList=dailyList)

@app.route('/reports/monthly')
def reportsMonthly():
    monthlyDict = {}
    db = shelve.open("reportsStorage.db", "r")
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
    return render_template('reportsMonthly.html', monthlyList=monthlyList)

@app.route('/reports/yearly')
def reportsYearly():
    yearlyDict = {}
    db = shelve.open("reportsStorage.db", "r")
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
    return render_template('reportsYearly.html', yearlyList=yearlyList)

@app.route('/reports/daily/delete/<id>', methods=["POST"])
def reportsDeleteDaily(id):
    dailyDict = {}
    db = shelve.open("reportsStorage.db", "w")
    dailyDict = db["Daily"]

    del dailyDict[id.replace('-', '/')]

    db["Daily"] = dailyDict
    db.close()

    return redirect(url_for("reportsDaily"))

@app.route('/reports/monthly/delete/<id>', methods=["POST"])
def reportsDeleteMonthly(id):
    monthlyDict = {}
    db = shelve.open("reportsStorage.db", "w")
    monthlyDict = db["Monthly"]

    del monthlyDict[id.replace('-', '/')]

    db["Monthly"] = monthlyDict
    db.close()

    return redirect(url_for("reportsMonthly"))

@app.route('/reports/yearly/delete/<id>', methods=["POST"])
def reportsDeleteYearly(id):
    yearlyDict = {}
    db = shelve.open("reportsStorage.db", "w")
    yearlyDict = db["Yearly"]

    del yearlyDict[id]

    db["Yearly"] = yearlyDict
    db.close()

    return redirect(url_for("reportsYearly"))

if __name__ == '__main__':
    app.run()
