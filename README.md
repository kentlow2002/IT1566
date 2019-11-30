# IT1566
Grp project for app dev it1566

CRUD structure:

Users super class
  userType
  userName
  userEmail
  userPassword
  Buyer

    Create BuyerAcc
    Retrieve Acc details
    Update Acc details
    Delete Acc

  Seller
    productsList
    Create SellerAcc
    Retrieve Acc details
    Update Acc details
    Delete Acc details

  Staff

    Create StaffAcc
    Retrieve StaffAcc
    Update Acc details
    Delete Acc

Products class
  productName
  productPrice
  productDescription

  Create Products
  Retrieve Products
  Update Products details
  Delete Products

Orders class
  orderId
  orderDate (ddmmyyyy)
  orderNote

  Create Orders
  Retrieve Orders
  Update Orders
  Delete Orders

Reports class
  Create Reports (daily,monthly,yearly)
  Retrieve Reports (daily,monthly,yearly)
  Delete Reports
