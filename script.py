import constants
from pprint import pprint

from snaptrade_client import SnapTrade, SnapTradeAuth

client = constants.CLIENT_ID
consumer = constants.CONSUMER_KEY

#initialize a client with clientID and consumerkey
snaptrade = SnapTrade(
    auth=SnapTradeAuth.personal_api_key(
        consumer_key=consumer,
        client_id=client
    )
)

#check that the client is able to make request, if the api is up
#api_response= snaptrade.api_status.check()
#pprint(api_response.body)

list_account_info = (snaptrade.account_information.list_user_accounts())

total_portfolio_value = 0
portfolio = []

for account in list_account_info.body:
    if account["status"] != 'closed':
        acc_id = account['id']
        account_info = snaptrade.account_information.get_all_account_positions(acc_id)
        data_freshness = account_info.body["data_freshness"]["as_of"]
        positions = account_info.body["results"]
#        pprint(data_freshness)
        
        account_number = account['name']
#        print(account_number)
        
#        pprint(account_info)
        for position in positions:
            symbol = position['instrument']['symbol']
            description = position['instrument']['description']
            price = float(position['price'])
            units = float(position['units'])
            value = float(units) * float(price)
#            txt = f"You have positions in {description} listed as {symbol}. The price is {price}, you own {units} of this investment. Total value is {total}."
#            print(txt)
            cost_basis = position.get("cost_basis", None)
            og_cost = None
            gain = None
           
            #gain for things that have cost basis:
            if cost_basis is not None:
                og_cost = float(cost_basis) * float(units)
                gain = value - og_cost
                txt = f"You own {value} of {symbol} / {description}, your total gain is {gain}"
#                print(txt)

            #things that are cash_equivalent
            cash_equivalent = position.get("cash_equivalent", False)

            #add up
            total_portfolio_value += value
            values = {"account": account_number, "symbol": symbol, "description": description, "value": value, "cost": og_cost, "total_gain": gain, "cash_equivalent": cash_equivalent}
            portfolio.append(values)


#running tally by account
value_by_account = {}
for card in portfolio:
    account = card["account"]
    value = card["value"]
    if account not in value_by_account:
        value_by_account[account] = 0
    value_by_account[account] += value

for account_name, account_total in value_by_account.items():
    percentage = account_total / float(total_portfolio_value) * 100
    print (f"{account_name} account is {percentage}% of the whole portfolio")


#pprint(value_by_account)
#pprint(calculate_percentage)
#pprint(portfolio)

total_value = f"your total portfolio value is {total_portfolio_value}"
#print(total_value)




