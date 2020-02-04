import User as u
import Order as o
import Report as r
import Product as p
import Faq as f
import Cart as c
import shelve
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_mail import Mail, Message
import os
import re
import string
import random
from ReportForms import CreateReportForm
from ProductForms import CreateProductForm, AddCartProduct, EditCartProduct

from UserForms import CreateUserForm, UserLogInForm, UserUpdateForm, ForgetPassForm, ProductsSearch
from staff import CreateStaffForm, StaffUpdateForm, FaqForm
from CartForm import CartUpdateForm
app = Flask(__name__)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_DEFAULT_SENDER = 'xstorenyp@gmail.com',
    MAIL_USERNAME = 'xstorenyp@gmail.com',
    MAIL_PASSWORD = 'admin2020!',
))
app.secret_key = os.urandom(16)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
mail = Mail(app)

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
                if j != None:
                    if userLogInForm.username.data == j.getUsername() and j.loginCheck(userLogInForm.password.data) == 1:
                        usernameValid = 1
                        passwordValid = 1
                        userID = j.getID()

            if passwordValid == 1 and usernameValid == 1:
                login_user(usersDict.get(userID), remember=userLogInForm.remember.data)
                resp = ''
                if current_user.getType() == "Buyer":
                    resp = make_response(redirect(url_for("buyerIndex")))
                    resp.set_cookie('cart',{})
                elif current_user.getType() == "Seller":
                    resp = make_response(redirect(url_for("sellerIndex")))
                else:
                    resp = make_response(redirect(url_for("reportsIndex")))
                resp.set_cookie("userID",str(userID))
                print("checking")
                return resp
            else:
                flash("Invalid Username/Password! Please Try Again.")
                return redirect(url_for("login"))

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
    userLogInForm = UserLogInForm(request.form)
    if request.method == 'POST' and createUserForm.validate():
        usersDict = {}
        db = shelve.open('Users.db', 'c')
        count = 0
        try:
            usersDict = db['Users']
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
        login_user(usersDict.get(count), remember=userLogInForm.remember.data)
        resp = make_response(redirect(url_for("userEdit")))
        resp.set_cookie("userID",str(count))
        print("checking")
        return resp
    return render_template('signup.html', form=createUserForm)

@app.route('/signedup')
def signedUp():
    return render_template('signedup.html')

@app.route('/userEdit',methods=["GET","POST"])
def userEdit():
    userUpdateForm = UserUpdateForm(request.form)
    if request.method == "POST" and userUpdateForm.validate():
        usersDict = {}
        db = shelve.open('Users.db', 'c')
        try:
            usersDict = db['Users']
        except:
            print("Error reading db")

        userID = int(request.cookies.get("userID"))
        user = usersDict.get(userID)
        print(user)
        userType = user.getType()
        if userUpdateForm.deleteAcc.data:
            print('deleting')
            usersDict.pop(userID)
            db['Users'] = usersDict
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
        print("lul")
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

@app.route('/forget',methods=['GET','POST'])
def forget():
    forgetPassForm = ForgetPassForm(request.form)
    if request.method == "POST" and forgetPassForm.validate():
        usersDict = {}
        try:
            db = shelve.open('Users.db','r')
            usersDict = db['Users']
        except Exception as e:
            print(e)
        userEmail = forgetPassForm.email.data
        for i in usersDict:
            if usersDict[i].getEmail() == userEmail:
                try:
                    tempPass = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))
                    msg = Message("Your password has been reset.",recipients=[userEmail],body="To login, please use the following password: "+tempPass)
                    mail.send(msg)
                    usersDict[i].setPassword(tempPass)
                    db['Users'] = usersDict
                    return render_template('thankemail.html')
                except Exception as e:
                    print(e)
                    return render_template('forgot.html',form = forgetPassForm)
    return render_template('forget.html', form=forgetPassForm)

# buyer
@app.route('/buyer/index')
# @login_required
def buyerIndex():
    return render_template('buyerIndex.html')

@app.route('/buyer/product', methods=['GET','POST'])
# @login_required
def buyerProducts():
    productsDict = {}
    productsList = []
    cartProducts = {}
    productsSearch = ProductsSearch(request.form)
    addProductForm = AddCartProduct(request.form)
    try:
        db = shelve.open('products.db', 'r')
        productsDict = db['products']
        if request.method == 'POST':
            if addProductForm.addProduct.data == True:
                cart = request.cookies.get('cart')
                print(cart)
                cart[int(addProductForm.productId.data)] = productsDict[int(addProductForm.productId.data)]
            query = productsSearch.query.data
            for key in productsDict:   # loop through Dictionary
                print("Main py : have products")
                product = productsDict.get(key)
                if product.get_productStatus() == "public" and (query.lower() in product.get_productName().lower() or query in product.get_productDescription().lower()):
                    productsList.append(product)
        else:
            for key in productsDict:   # loop through Dictionary
                print("Main py : have products")
                product = productsDict.get(key)
                if product.get_productStatus() == "public":
                    productsList.append(product)
        db.close()
    except Exception as e:
        print(e)

    return render_template('buyerProduct.html',  productsList=productsList, searchForm=productsSearch, addForm=addProductForm)

@app.route('/buyer/retrieve')
# @login_required
def buyerRetrieve():
    return render_template('buyerRetrieve.html')

@app.route('/buyer/cart', methods = ['GET','POST'])
def cart():
    #if current_user.is_authenticated:
    cartUpdateForm = CartUpdateForm(request.form)
    if request.method == 'POST' and cartUpdateForm.validate():
        cartDict = {}
        try:
            db = shelve.open('products.db', "r")
            cartDict = db["products"]
        except Exception as e:
            print(e)
        return redirect(url_for("buyerCheckout"))

    return render_template('buyerCart.html')
@app.route('/buyer/checkout')
# @login_required
def buyerCheckout():
    return render_template('buyerCheckout.html')
@app.route('/buyer/thanks')
# @login_required
def buyerThanks():
    return render_template('buyerThanks.html')
# seller


@app.route('/seller/index')
@login_required
def sellerIndex():

    productsDict = {}

    try:
        db = shelve.open('products.db', 'r')
        productsDict = db['products']
        productsList = []
        hiddenList = []
        print(current_user.getID())
        for key in productsDict:   # loop through Dictionary
            product = productsDict.get(key)
            print(product.get_productName())
            print(product.get_userID())
            userID = int(current_user.getID())
            if userID == product.get_userID():
                if product.get_productStatus() == "public":
                    productsList.append(product)
                else:
                    hiddenList.append(product)
        db.close()
    except:
        hiddenList = []
        productsList = []
    return render_template('sellerIndex.html', productsList=productsList, count=len(productsList), hiddenList=hiddenList)


@app.route('/seller/listing', methods=['GET', 'POST'])
def sellerListProduct():
    createProductForm = CreateProductForm(request.form)
    if request.method == 'POST' and createProductForm.validate():
        print("test for validate")
        productsDict = {}
        db = shelve.open('products.db', 'c')

        try:
            productsDict = db['products']
            p.Product.countId = db['ProductCountId']

        except:
            print("Error in retrieving Users form storage.db")


        # create an instance of class User
        # send data from the form to class initializer
        if request.files:
                    productPicture = request.files[createProductForm.productPicture.name]

                    # if this print does not show in console, add enctype="multipart/form-data" to the form tag in the html code
                    print(productPicture)

                    productPicture.save(os.path.join("static/assets", productPicture.filename))

                    # this shows the path where it gets saved to
                    print(os.path.join("static/assets", productPicture.filename))

        # this saves it to the object
                    filepath = os.path.join("../../../static/assets", productPicture.filename)

        userID = int(current_user.getID())
        print("Main.py ln 258")
        print(userID)
        product = p.Product(createProductForm.productName.data, createProductForm.productCondition.data, createProductForm.productPrice.data, createProductForm.productQuantity.data, createProductForm.productDescription.data, filepath, userID)
        print(userID)

        # Save the User instance in the usersDict, using userID as the key
        productsDict[product.get_productId()] = product
        db['products'] = productsDict

        # Save the countID to shelve/persistence

        db['ProductCountId'] = p.Product.countId
        print(product.get_productName(), "was stored in shelve successfully with Product ID =", product.get_productId())

        db.close()

        return redirect(url_for('sellerIndex'))

    return render_template('sellerListProduct.html', form=createProductForm)

@app.route('/seller/updateProduct/<int:id>/', methods=['GET', 'POST'])
def updateProduct(id):
    updateProductForm = CreateProductForm(request.form)
    #   POST: when click on submit button to send the data to server


    if request.method == 'POST' and updateProductForm.validate():
        productDict = {}
        db = shelve.open('products.db', 'w')
        productDict = db['products']

        product = productDict.get(id)
        product.set_productName(updateProductForm.productName.data)
        product.set_productCondition(updateProductForm.productCondition.data)
        product.set_productPrice(updateProductForm.productPrice.data)
        product.set_productQuantity(updateProductForm.productQuantity.data)
        product.set_productDesc(updateProductForm.productDescription.data)
        if request.files:
            try:
                productPicture = request.files[updateProductForm.productPicture.name]

                # if this print does not show in console, add enctype="multipart/form-data" to the form tag in the html code
                print(productPicture)

                productPicture.save(os.path.join("static/assets", productPicture.filename))

                # this shows the path where it gets saved to
                print(os.path.join("static/assets", productPicture.filename))

                # this saves it to the object
                filepath = os.path.join("../../../static/assets", productPicture.filename)
                product.set_productPicture(filepath)
            except:
                product.set_productPicture(product.get_productPicture())

        db['products'] = productDict  # write to shelve
        db.close()

        return redirect(url_for('sellerIndex'))

    #   GET: when the page loads
    else:
        # these 4 lines are exactly the same as retrieve data
        productsDict = {}
        db = shelve.open('products.db', 'r')
        productsDict = db['products']
        db.close()

        #   find the data from Data Dictionary
        product = productsDict.get(id)



        #   display the data in the field
        updateProductForm.productName.data = product.get_productName()
        updateProductForm.productCondition.data = product.get_productCondition()
        updateProductForm.productPrice.data = product.get_productPrice()
        updateProductForm.productQuantity.data = product.get_productQuantity()
        updateProductForm.productDescription.data = product.get_productDescription()


        return render_template('updateProduct.html', form=updateProductForm, product=product)




@app.route('/seller/hideProduct/<int:id>/', methods=['GET', 'POST'])
def hideProduct(id):
    productsDict = {}
    # retrieve from persistence
    db = shelve.open('products.db', 'w')
    productsDict = db['products']
    product = productsDict.get(id)
    product.set_productStatusHidden()

    db['products'] = productsDict

    db.close()
    print("product: ", productsDict)

    return redirect(url_for('sellerIndex'))

@app.route('/seller/showProduct/<int:id>/', methods=['GET', 'POST'])
def showProduct(id):
    print("hi")

    productsDict = {}
    # retrieve from persistence
    db = shelve.open('products.db', 'w')
    productsDict = db['products']
    product = productsDict.get(id)
    product.set_productStatusPublic()

    db['products'] = productsDict

    db.close()
    print("product: ", productsDict)
    return redirect(url_for('sellerIndex'))


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
            except KeyError:
                pass
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
    return render_template('retrieveAcc.html', userList=userList, UserID = current_user.getID())
# whatever the person doing staff
#FAQ
@app.route('/faq') #R faq contact us
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
@app.route('/faqType') #R faq by user type
def faqTypeS():
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
    return render_template('FAQtype.html', faqList=faqList, usertype = current_user.getType(), UserID = current_user.getID())

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
                try:
                    count = count
                except UnboundLocalError:
                    count = 0
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
            if current_user.getType() != "Staff":
                return redirect(url_for('faq'))
            else:
                return redirect(url_for("faqstaff"))
    else:
        return redirect(url_for("index"))
    return render_template('FAQask.html', form= createFaqForm, usertype = current_user.getType())
@app.route('/staff/faq') #R faq for staff
@login_required
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
                    if len(date[0]) == 1:
                        date[0] = "0" + date[0]
                    if len(date[1]) == 1:
                        date[1] = "0" + date[1]

                    if datetime.strptime("/".join(date), '%d/%m/%Y'):
                        if createReportForm.type.data == "D":
                            date = "/".join(date)
                            date = datetime.strptime(date, "%d/%m/%Y")
                        elif createReportForm.type.data == "M":
                            del date[:1]
                            date = "/".join(date)
                            date = datetime.strptime(date, "%m/%Y")
                        else:
                            print(date)
                            del date[:2]
                            date = "/".join(date)
                            date = datetime.strptime(date, "%Y")
                elif len(date) == 2:
                    if int(date[0]) > 12:
                        date[0] = "12"

                    if len(date[0]) == 1:
                        date[0] = "0" + date[0]

                    if datetime.strptime("/".join(date), '%m/%Y'):
                        if createReportForm.type.data == "M":
                            date = "/".join(date)
                            date = datetime.strptime(date, "%m/%Y")
                elif len(date) == 1:
                    if datetime.strptime("/".join(date), '%Y'):
                        date = date[0]
                        date = datetime.strptime(date, "%Y")
                return date


            if createReportForm.type.data == "D":
                formDate = createReportForm.day.data + "/" + createReportForm.month.data + "/" + createReportForm.year.data
            elif createReportForm.type.data == "M":
                formDate = createReportForm.month.data + "/" + createReportForm.year.data
            else:
                formDate = createReportForm.year.data

            try:
                correctedDate = dateValidator(formDate)
                if createReportForm.type.data == "D":
                    strCorrectedDate = correctedDate.strftime("%d/%m/%Y")
                elif createReportForm.type.data == "M":
                    strCorrectedDate = correctedDate.strftime("%m/%Y")
                else:
                    strCorrectedDate = correctedDate.strftime("%Y")
                today = datetime.today()

                if correctedDate > today:
                    flash("The date %s have not pass, Please try again." % correctedDate)
                    return redirect(url_for("reportsCreate"))
            except:
                flash("The date %s is a invalid date/format, Please try again." % formDate)
                return redirect(url_for("reportsCreate"))

            # transaction = open("test.txt", "r")

            import stepInDB
            orders = {
                stepInDB.Order(0, "12/12/2019", "testing", "delivered", "address", 100, 1),
                stepInDB.Order(1, "13/12/2019", "testing", "delivered", "address", 200, 9),
                stepInDB.Order(2, "12/12/2019", "testing", "delivered", "address", 100, 5),
                stepInDB.Order(3, "12/12/2019", "testing", "delivered", "address", 300, 4),
                stepInDB.Order(4, "14/12/2019", "testing", "delivered", "address", 400, 3),
                stepInDB.Order(5, "12/12/2019", "testing", "delivered", "address", 100, 15),
                stepInDB.Order(6, "13/12/2019", "testing", "delivered", "address", 150, 10),
                stepInDB.Order(7, "13/12/2018", "testing", "delivered", "address", 150, 10),
                stepInDB.Order(8, "13/12/2017", "testing", "delivered", "address", 150, 10),
            }
            stepInOrdersDB = shelve.open("stepInOrdersDB.db", "c")
            stepInOrdersDB["test"] = orders
            stepInOrdersDB.close()



            order = {}
            stepInOrdersDB = shelve.open("stepInOrdersDB.db", "r")
            order = stepInOrdersDB["test"]
            if createReportForm.type.data == "D":
                if today >= correctedDate:
                    if strCorrectedDate not in reportDict:
                        productCount = 0
                        productPrice = 0
                        for all in order:
                            if dateValidator(all.get_orderDate()).strftime("%d/%m/%Y") == strCorrectedDate:
                                productCount += int(all.get_orderQuan())
                                productPrice += float(all.get_orderPrice())
                        report = r.Report(createReportForm.type.data, strCorrectedDate, productCount, productPrice)
                        reportDict[strCorrectedDate] = report
                        db["Daily"] = reportDict
                    else:
                        db["Daily"] = reportDict
                        flash("The date %s already exists in the database, please delete the old report if a new report is required" % strCorrectedDate)
                        return redirect(url_for("reportsCreate"))
                else:
                    flash("The date %s have to be elapsed to be created." % strCorrectedDate)
                    return redirect(url_for("reportsCreate"))

            elif createReportForm.type.data == "M":
                if today > correctedDate:
                    if strCorrectedDate not in reportDict:
                        productCount = 0
                        productPrice = 0
                        for all in order:
                            if dateValidator(all.get_orderDate()).strftime("%m/%Y") == strCorrectedDate:
                                productCount += int(all.get_orderQuan())
                                productPrice += float(all.get_orderPrice())
                        report = r.Report(createReportForm.type.data, strCorrectedDate, productCount, productPrice)
                        reportDict[strCorrectedDate] = report
                        db["Monthly"] = reportDict
                    else:
                        db["Monthly"] = reportDict
                        flash("The date %s already exists in the database, please delete the old report if a new report is required" % strCorrectedDate)
                        return redirect(url_for("reportsCreate"))
                else:
                    flash("The date %s have to be elapsed to be created." % strCorrectedDate)
                    return redirect(url_for("reportsCreate"))

            else:
                if today > correctedDate:
                    if strCorrectedDate not in reportDict:
                        productCount = 0
                        productPrice = 0
                        for all in order:
                            if dateValidator(all.get_orderDate()).strftime("%Y") == strCorrectedDate:
                                productCount += int(all.get_orderQuan())
                                productPrice += float(all.get_orderPrice())
                        report = r.Report(createReportForm.type.data, strCorrectedDate, productCount, productPrice)
                        reportDict[strCorrectedDate] = report
                        db["Yearly"] = reportDict
                    else:
                        db["Yearly"] = reportDict
                        flash("The date %s already exists in the database, please delete the old report if a new report is required" % strCorrectedDate)
                        return redirect(url_for("reportsCreate"))
                else:
                    flash("The date %s have to be elapsed to be created." % strCorrectedDate)
                    return redirect(url_for("reportsCreate"))

            stepInOrdersDB.close()
            db.close()

            flash("The report for %s has be generated successfully" % strCorrectedDate)
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

#orders
@app.route('/order')
#@login_required
def order():
    #if current_user.is_authenticated and current_user.getType() == "Buyer":
        orderDict = {}
        db = shelve.open("orderStorage.db", "c")
        try:
            orderDict = db["Order"]
        except Excecption as e:
            print(e)
if __name__ == '__main__':
    app.run(debug=True)
