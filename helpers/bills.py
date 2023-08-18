from helpers.common import loadJSONFromFile

bill_file = 'data/bills/bills.json'
bill_info_file = 'data/bills/bill_info.json'

def getBillInfo(bill_name):
    bill_info = {}
    mybills_info = loadJSONFromFile(bill_info_file)
    for i in range(len(mybills_info)):
        if mybills_info[i]['name'] == bill_name:
            bill_info = mybills_info[i]
            break
    return bill_info

def getBillHistory(bill_name):
    bill_history = []
    mybills = loadJSONFromFile(bill_file)
    for i in range(len(mybills)):
        if mybills[i]['name'] == bill_name:
            bill_info = mybills[i]
            bill_history.append(bill_info)

    return bill_history
