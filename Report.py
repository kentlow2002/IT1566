class Report:
    def __init__(self, reportType, reportDate, itemSold, revenue):
        self.__reportType = reportType
        self.__reportDate = ""
        self.correctReportDate(reportDate)
        self.__itemSold = itemSold
        self.__revenue = revenue
        self.__commission = ""
        self.calculate_commission(revenue)

    def calculate_commission(self, revenue):
        commission = revenue * 0.1
        self.__commission = commission
        return self.__commission

    def correctReportDate(self, reportDate):
        date = reportDate.split("/")
        if int(date[0]) > 31:
            date[0] = "31"
        if int(date[1]) > 12:
            date[1] = "12"

        if len(date[0]) == 1:
            date[0] = "0" + date[0]
        if len(date[1]) == 1:
            date[1] = "0" + date[1]

        if self.__reportType == "D":
            date = "/".join(date)
        elif self.__reportType == "M":
            del date[0]
            date = "/".join(date)
        else:
            date = date[2]
        self.__reportDate = date
        return self.__reportDate


    def get_reportType(self):
        return self.__reportType

    def get_reportDate(self):
        return self.__reportDate

    def get_itemSold(self):
        return self.__itemSold

    def get_revenue(self):
        return self.__revenue

    def get_commission(self):
        return self.__commission
