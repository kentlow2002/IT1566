import User as u
import Order as o
import Report as r
import Product as p
import Faq as f
import shelve
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import os
from ReportForms import CreateReportForm
from UserForms import CreateUserForm, UserLogInForm, UserUpdateForm
from staff import CreateStaffForm, StaffUpdateForm, FaqForm

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

        try:
            db = shelve.open('Users.db', 'r')
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

        return redirect(url_for("login"))
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
        count = 0
        try:
            usersDict = db['Users']
            count = 0
            while True:
                if usersDict[count] == "null":
                     break
                count += 1
        except:
            print("Error in retrieving Users from storage.db.")
        print(count)
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
    if request.method == "POST" and userUpdateForm.validate():
        usersDict = {}
        db = shelve.open('Users.db', 'w')
        try:
            usersDict = db['Users']
        except:
            print("Error reading db")

        userID = int(request.cookies.get("userID"))
        user = usersDict.get(userID)
        userType = user.getType()
        if userUpdateForm.deleteAcc.data:
            user = 0
            return redirect('/')
        else:
            if user.loginCheck(userUpdateForm.oldPassword.data):
                user.setEmail(userUpdateForm.email.data)
                print("email changed",user)
                if userUpdateForm.newPassword.data.isalnum():
                    user.setPassword(userUpdateForm.newPassword.data)
        db['Users'] = usersDict
        urlString = '/'+userType.lower()+'/index'
        return redirect(urlString)
    else:
        usersDict = {}
        db = shelve.open('Users.db', 'r')
        try:
            usersDict = db['Users']
        except:
            print("Error reading db")

        userID = int(request.cookies.get("userID"))
        user = usersDict.get(userID)
        userType = user.getType()
        userUpdateForm.username.data = user.getUsername()
        userUpdateForm.email.data = user.getEmail()

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
@app.route('/staff/create', methods=['GET', 'POST'])
def staffCreate():
    if current_user.is_authenticated:
        createUserForm = CreateUserForm(request.form)
        if request.method == 'POST' and createUserForm.validate():
            usersDict = {}
            db = shelve.open('Users.db', 'c')
            try:
                usersDict = db['Users']
                count = 0
                while True:
                    if usersDict[count] == "null":
                         break
                    count += 1
            except:
                print("Error in retrieving Users from storage.db.")
                count = 0

            user = u.Staff(createUserForm.username.data,createUserForm.email.data, createUserForm.password.data, count)
            usersDict[user.getID()] = user
            db['Users'] = usersDict
            return redirect(url_for("staffAccounts"))
    else:
        return redirect(url_for("index"))
    return render_template('staffCreate.html', form=createUserForm)

@app.route('/deleteUser/<int:id>', methods=['POST'])
def deleteUser(id):
    usersDict = {}
    db = shelve.open('Users.db', 'w')
    usersDict = db['Users']
    usersDict.pop(id)
    db['Users'] = usersDict
    db.close()
    return redirect(url_for('staffAccounts'))

@app.route('/staff/orders')
def staffOrders():
    return render_template('staffOrders.html')

@app.route('/staff/update')
def staffUpdate():
    return render_template('staffUpdate.html')

#@app.route('/staff/profile')
#def staffProfile():
#    return render_template('staffProfile.html')
@app.route('/staffEdit/<int:id>/', methods=['GET', 'POST'])
def updateUser(id):
    updateStaffForm = StaffUpdateForm(request.form)
    if request.method == 'POST' and updateStaffForm.validate():
        userDict = {}
        db = shelve.open('Users.db', 'w')
        userDict = db['Users']
        user = userDict.get(id)
        user.setUsername(updateStaffForm.username.data)
        user.setEmail(updateStaffForm.email.data)
        user.setPassword(updateStaffForm.password.data)
        db['Users'] = userDict
        db.close()
        return redirect(url_for('staffAccounts'))

    else:
        userDict = {}
        db = shelve.open('Users.db', 'c')
        userDict = db['Users']
        db.close()
        user = userDict.get(id)
        updateStaffForm.username.data = user.getUsername()
        updateStaffForm.email.data = user.getEmail()
    return render_template('staffEdit.html', form=updateStaffForm)

@app.route('/staff/accounts')
def staffAccounts():
    if current_user.is_authenticated:
        db = shelve.open("Users.db", "c")
        try:
            userDict = db["Users"]
            userList = []
            for key in userDict:
                user = userDict.get(key)
                userList.append(user)
        except:
            print("Error in retrieving user storage.")
            userList = []
        finally:
            db.close()
    else:
        return redirect(url_for("index"))
    return render_template('retrieveAcc.html', userList=userList)
# whatever the person doing staff
#FAQ
@app.route('/faq') #R faq
def faq():
    if current_user.is_authenticated:
        db = shelve.open("faq.db", "c")
        try:
            faqDict = db["ticket"]
            faqList = []
            for key in faqDict:
                faqs = faqDict.get(key)
                faqList.append(faqs)

        except:
            print("Error in retrieving faq storage.")
            faqList = []
        finally:
            db.close()
            print(current_user.getID())
    else:
        return redirect(url_for("index"))
    return render_template('FAQs.html', faqList=faqList, usertype = current_user.getType(), UserID = current_user.getID())
@app.route('/faq/ask', methods=['GET', 'POST'])
def ask():
    if current_user.is_authenticated:
        createFaqForm = FaqForm(request.form)
        if request.method == 'POST':
            faqDict = {}
            try:
                db = shelve.open('faq.db', 'c')
                faqDict = db["ticket"]
                count = 0
                while True:
                    if faqDict[count] == "null":
                         break
                    count += 1
            except KeyError:
                count = count
            except:
                print("Error in retrieving tickets from faq.db.")
                count = 0
            tix = f.Ticket(createFaqForm.question.data, createFaqForm.answer.data, current_user.getType(), count, current_user.getID())
            faqDict[tix.getTID()] = tix
            db["ticket"] = faqDict
            # Test codes
            faqDict = db["ticket"]
            tix = faqDict[tix.getTID()]
            print(tix.getTID(), "was stored in shelve successfully ")
            db.close()
            print(faqDict)
            return redirect(url_for('faq'))
    else:
        return redirect(url_for("index"))
    return render_template('FAQask.html', form= createFaqForm, usertype = current_user.getType())
@app.route('/staff/faq') #R faq for staff
def faqstaff():
    if current_user.is_authenticated:
        faqList = ""
        try:
            db = shelve.open("faq.db", "c")
            faqDict = db["ticket"]
            faqList = []
            for key in faqDict:
                faqs = faqDict.get(key)
                faqList.append(faqs)
        except:
            print("error in retrieving faqs")
        finally:
            db.close()
    else:
        return redirect(url_for("index"))
    return render_template('FAQstaff.html', faqList=faqList, usertype = current_user.getType())

@app.route('/answerFAQ/<int:Tid>/', methods=['GET', 'POST'])
def ans(Tid):
    updatefaqForm = FaqForm(request.form)
    if current_user.is_authenticated:
        if request.method == 'POST':
            #try:
            db = shelve.open("faq.db", "w")
            faqDict = db["ticket"]
            faq = faqDict.get(Tid)
            faq.setAns(updatefaqForm.answer.data)
            db["ticket"] = faqDict
            db.close()
            #except:
            #    print("Error updating faq storage.")
            return redirect(url_for('faqstaff'))
        else:
            db = shelve.open('faq.db', 'w')
            try:
                faqDict = db["ticket"]
                faq = faqDict.get(Tid)
                updatefaqForm.question.data = faq.getQn()
                updatefaqForm.answer.data = faq.getAns()

            except:
                print("Error in retrieving faq storage. place 2")
            finally:
                db.close()


    else:
        return redirect(url_for("index"))
    return render_template('FAQans.html', form= updatefaqForm, Quest = faq.getQn())
# reports
@app.route('/staff')
@login_required
def redirectStaff():
    return redirect(url_for("reportsIndex"))


@app.route('/staff/index')
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
