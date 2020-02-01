import pandas as pd
import operator
df = pd.read_csv('PreInterviewTaskData.csv')

### Create lists of merchants, dates
merchants = []
merchant_frequencies = {}
for merchant in df["merchant"]:
    if (merchant not in merchants):
        merchants.append(merchant)
    if (merchant in merchant_frequencies):
        merchant_frequencies[merchant] += 1
    else:
        merchant_frequencies[merchant] = 1
# print(merchants)

### Create dictionary of lists with: {account : [merchant date pairs for that account]}
account_pairs = {}
for i in range(len(df["account"])):
    df_day = int(str(df["date"][i])[-2:])
    df_account = df["account"][i]
    df_fraud = df["fraud"][i]
    df_merchant = df["merchant"][i]
    if (df_fraud == False):
        if (df_account not in account_pairs):
            account_pairs[df_account] = [(df_merchant, df_day)]
        elif (df_account in account_pairs):
            account_pairs[df_account].append((df_merchant, df_day))
print("created account_pairs")
# print(account_pairs)

### Creating dictionary in the form: exploit_by_date = {date of exploitation : [accounts exploited]}
exploit_by_date = {}
for i in range(len(df["account"])):
    day = int(str(df["date"][i])[-2:])
    if ((df["fraud"][i] == True) and not (day in exploit_by_date)):
        exploit_by_date[day] = [df["account"][i]]
    elif ((df["fraud"][i] == True) and (day in exploit_by_date)):
        exploit_by_date[day].append(df["account"][i])
print("created exploit_by_date")
# print(exploit_by_date)

### optimised version of creating data_structure:
print("data_structure2 start")
data_structure2 = {}
for day_of_exploitation, accounts in exploit_by_date.items():
    # print("day currently processing: ", day_of_exploitation, " of 30.")
    data_structure2[day_of_exploitation] = {}
    for account in accounts:
        account_pair_list = account_pairs[account]
        for i in range(len(account_pair_list)):
            if account_pair_list[i][1] >= day_of_exploitation:
                end_index = i
                data_structure2[day_of_exploitation][account] = account_pairs[account][:i]
                break
print("data_structure2 completed")
# print(data_structure2)
            
# my_df = pd.DataFrame(data_structure2)
# my_df.to_json('my_pd_data_structure2.json')

#### Creating list of merchant_day_pairs for each day_of_exploitation:
# {date_of_exploitation : {merchant_day_pair : frequency, ...}}
days_to_check = [21, 22, 23]                 # Previously identified [21, 22, 23] as days of exploitation (from fraudulent transaction frequencies)
pairs_by_day = {}
for day_of_exploitation in days_to_check:
    accounts = data_structure2[day_of_exploitation]
    pairs_by_day[day_of_exploitation] = {}
    for account, pairs in accounts.items():
        for pair in pairs:
            if (pair in pairs_by_day[day_of_exploitation]):
                pairs_by_day[day_of_exploitation][pair] += 1
            else:
                pairs_by_day[day_of_exploitation][pair] = 1
# print(pairs_by_day)

ordered_pairs_day = {}
for day_of_exploitation, pairs in pairs_by_day.items():
    ordered_pairs_day[day_of_exploitation] = []
    for pair in sorted(pairs, key=pairs.get, reverse=True):
        if (pairs[pair] > 10):
            ordered_pairs_day[day_of_exploitation].append((pair, pairs[pair]))
        else:
            pass
# print(ordered_pairs_day)
print("-------------")

print("RESULT:")
for day_of_exploitation, pairs in pairs_by_day.items():
    print(day_of_exploitation, " : ", ordered_pairs_day[day_of_exploitation])

### RESULT:
# In the form:
# day of exploitation : [(('Merchant compromised', day of compromise), number of matches), ...]
# 21  :  [(('M18', 16), 31), (('M18', 15), 21)]
# 22  :  [(('M18', 16), 33), (('M18', 15), 20)]
# 23  :  [(('M18', 16), 31), (('M18', 15), 21)] --> (next highest entry at matches = 10)




