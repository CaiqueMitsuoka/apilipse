from survivorsReports import SurvivorsReport
from itemsReports import ItemsReports


def get_reports():

    return {
        'reports':
            {
                SurvivorsReport().report_survivor_quantity(),
                ItemsReports().items_report()
            }
    }
