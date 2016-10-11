from survivorsReports import SurvivorsReport
from itemsReports import ItemsReports


def get_reports():

    return {
        'reports':
            {
                'survivors':SurvivorsReport().report_survivor_quantity(),
                'items':ItemsReports().items_report()
            }
    }
