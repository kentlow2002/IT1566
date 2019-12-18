class Report:
    def __init__(self, reportType, reportDate, itemSold, revenue):
        self.__reportType = reportType
        self.__reportDate = reportDate
        self.__itemSold = itemSold
        self.__revenue = revenue
        self.__commission = ""
        self.calculate_commission(revenue)

    def calculate_commission(self, revenue):
        commission = revenue * 0.1
        self.__commission = commission
        return self.__commission

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
