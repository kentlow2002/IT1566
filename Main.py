import User as u
import Order as o
import Report as r
import Product as p
import shelve
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import os
from ReportForms import CreateReportForm
from UserForms import CreateUserForm, UserLogInForm, UserUpdateForm


app = Flask(__name__)
app.secret_key = os.urandom(16)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    usersDict = {}
    db = shelve.open('Users.db', 'r')
    try:
        usersDict = db['Users']
    except:
        print("Error in retrieving Users from storage.db.")
    return usersDict.get(user_id)

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
            userID = -1
            for i,j in usersDict.items():
                if userLogInForm.username.data == j.getUsername() and j.loginCheck(userLogInForm.password.data) == 1:
                    usernameValid = 1
                    passwordValid = 1
                    userID = j.getID()

            if passwordValid == 1 and usernameValid == 1:
                login_user(usersDict.get(userID), remember=userLogInForm.remember.data)
                resp = make_response(redirect(url_for("userEdit")))
                resp.set_cookie("userID",str(userID))
                print("checking")
                return resp

        except Exception as e:
            print("ERROR", e)

        return redirect(url_for("logout"))
    return render_template('login.html', form=userLogInForm)

@app.route('/logout')
@login_required
def logout():
    logout_user()
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

        if createUserForm.username.data[:7] == "{Admin}":
            user = u.Staff(createUserForm.username.data,createUserForm.email.data, createUserForm.password.data, count)
        else:
            if createUserForm.type.data == "Buyer":
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

@app.route('/userEdit',methods=["GET","POST"])
def userEdit():
    userUpdateForm = UserUpdateForm(request.form)
    usersDict = {}
    db = shelve.open('Users.db', 'r')
    try:
        usersDict = db['Users']
    except:
        print("Error reading db")

    userID = int(request.cookies.get("userID"))
    user = usersDict[userID]
    userType = user.getType()
    userUpdateForm.username.data = user.getUsername()
    userUpdateForm.email.data = user.getEmail()
    if request.method == "POST" and userUpdateForm.validate():
        if form.deleteAcc.data:
            usersDict[userID] = 0
            return redirect('/index')
        else:
            if user.loginCheck(userUpdateForm.oldPassword.data):
                user.setEmail(userUpdateForm.email.data)
                if userUpdateForm.newPassword.data.isalnum():
                    user.setPassword(userUpdateForm.newPassword.data)

        urlString = '/'+userType.lower()+'/index'
        return redirect(urlString)

    return render_template('userEdit.html', form=userUpdateForm, usertype=userType)

# buyer
@app.route('/buyer/index')
# @login_required
def buyerIndex():
    return render_template('buyerIndex.html')

# seller
@app.route('/seller/index')
# @login_required
def sellerIndex():
    return render_template('sellerIndex.html')


# staff

# whatever the person doing staff


# reports
@app.route('/staff')
@login_required
def reportsIndex():
    if current_user.is_authenticated and current_user.getType() == "Staff":
        print(current_user.getType())
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
    elif current_user.is_authenticated and current_user.getType() == "Buyer":
        return redirect(url_for("buyerIndex"))
    elif current_user.is_authenticated and current_user.getType() == "Seller":
        return redirect(url_for("sellerIndex"))
    else:
        return redirect(url_for("index"))


@app.route('/staff/create-report', methods=["GET", "POST"])
@login_required
def reportsCreate():
    if current_user.is_authenticated and current_user.getType() == "Staff":
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

            flash("The report for %s has be created/updated successfully" % correctedDate)
            if createReportForm.type.data == "D":
                return redirect(url_for("reportsDaily"))
            elif createReportForm.type.data == "M":
                return redirect(url_for("reportsMonthly"))
            elif createReportForm.type.data == "Y":
                return redirect(url_for("reportsYearly"))
            else:
                return redirect(url_for("reportsIndex"))
        return render_template('reportsCreate.html', form=createReportForm)
    elif current_user.is_authenticated and current_user.getType() == "Buyer":
        return redirect(url_for("buyerIndex"))
    elif current_user.is_authenticated and current_user.getType() == "Seller":
        return redirect(url_for("sellerIndex"))
    else:
        return redirect(url_for("index"))


@app.route('/staff/daily-report')
@login_required
def reportsDaily():
    if current_user.is_authenticated and current_user.getType() == "Staff":
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
    elif current_user.is_authenticated and current_user.getType() == "Buyer":
        return redirect(url_for("buyerIndex"))
    elif current_user.is_authenticated and current_user.getType() == "Seller":
        return redirect(url_for("sellerIndex"))
    else:
        return redirect(url_for("index"))


@app.route('/staff/monthly-report')
@login_required
def reportsMonthly():
    if current_user.is_authenticated and current_user.getType() == "Staff":
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
    elif current_user.is_authenticated and current_user.getType() == "Buyer":
        return redirect(url_for("buyerIndex"))
    elif current_user.is_authenticated and current_user.getType() == "Seller":
        return redirect(url_for("sellerIndex"))
    else:
        return redirect(url_for("index"))


@app.route('/staff/yearly-report')
@login_required
def reportsYearly():
    if current_user.is_authenticated and current_user.getType() == "Staff":
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
    elif current_user.is_authenticated and current_user.getType() == "Buyer":
        return redirect(url_for("buyerIndex"))
    elif current_user.is_authenticated and current_user.getType() == "Seller":
        return redirect(url_for("sellerIndex"))
    else:
        return redirect(url_for("index"))


@app.route('/staff/daily-report/delete/<id>', methods=["POST"])
@login_required
def reportsDeleteDaily(id):
    if current_user.is_authenticated and current_user.getType() == "Staff":
        dailyDict = {}
        db = shelve.open("reportsStorage.db", "w")
        dailyDict = db["Daily"]

        del dailyDict[id.replace('-', '/')]

        db["Daily"] = dailyDict
        db.close()

        return redirect(url_for("reportsDaily"))
    elif current_user.is_authenticated and current_user.getType() == "Buyer":
        return redirect(url_for("buyerIndex"))
    elif current_user.is_authenticated and current_user.getType() == "Seller":
        return redirect(url_for("sellerIndex"))
    else:
        return redirect(url_for("index"))


@app.route('/staff/monthly-report/delete/<id>', methods=["POST"])
@login_required
def reportsDeleteMonthly(id):
    if current_user.is_authenticated and current_user.getType() == "Staff":
        monthlyDict = {}
        db = shelve.open("reportsStorage.db", "w")
        monthlyDict = db["Monthly"]

        del monthlyDict[id.replace('-', '/')]

        db["Monthly"] = monthlyDict
        db.close()

        return redirect(url_for("reportsMonthly"))
    elif current_user.is_authenticated and current_user.getType() == "Buyer":
        return redirect(url_for("buyerIndex"))
    elif current_user.is_authenticated and current_user.getType() == "Seller":
        return redirect(url_for("sellerIndex"))
    else:
        return redirect(url_for("index"))


@app.route('/staff/yearly-report/delete/<id>', methods=["POST"])
@login_required
def reportsDeleteYearly(id):
    if current_user.is_authenticated and current_user.getType() == "Staff":
        yearlyDict = {}
        db = shelve.open("reportsStorage.db", "w")
        yearlyDict = db["Yearly"]

        del yearlyDict[id]

        db["Yearly"] = yearlyDict
        db.close()

        return redirect(url_for("reportsYearly"))
    elif current_user.is_authenticated and current_user.getType() == "Buyer":
        return redirect(url_for("buyerIndex"))
    elif current_user.is_authenticated and current_user.getType() == "Seller":
        return redirect(url_for("sellerIndex"))
    else:
        return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
