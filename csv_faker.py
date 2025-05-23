import csv
from datetime import datetime
import random
from faker import Faker

fake = Faker()

num_transactions = 500
start_date = datetime(2016, 1, 1)
end_date = datetime(2024, 12, 31)

descriptions = {
    'debit': [
        'Repairs for the drafty farmhouse leaky roof again',
        'Electricity bill to keep the coding rig humming',
        'Starlink subscription only internet that works out here',
        'Grocery run for ramen and clearance beef',
        'Coffee from the gas station caffeine is life',
        'Splurged on a taco from the food truck',
        'Renewed free tier IDE license pro is for city folks',
        'Paid for cloud storage my codes only home',
        'Drove miles to a career fair free coffee no jobs',
        'Bought a dog eared Python book from the thrift store',
        'Gas money for networking at the pizzerias open mic',
        'Paid for firewood choppings my cardio',
        'Tossed cash to an open source repo basically a patron',
        'Garden supplies to grow my own food',
        'Household expenses lightbulbs and hope',
        'Bulk flour for DIY pizza dough sauce is optional',
        'Replaced a fried USB cable from the dollar store',
        'Paid for a library card to use their WiFi',
        'Bought a used server cabinet at a garage sale',
        'Vet bill for the farm cats who help me code',
        'Donated to a crowdfunded Linux distro',
        'New batteries for =the UPS keeping my PC alive'
    ],
    'credit': [
        'Debugged neighbors ancient PC for cash and a pie',
        'Sold an app prototype to a sketchy startup',
        'Found cash in an old pair of jeans millionaire vibes',
        'Tax refund thanks IRS',
        'Neighbor paid me for setting up their router',
        'Sold a bucket of chicken eggs at the farmers market',
        'Bartered coding help for a sack of potatoes',
        'Got paid for a Craigslist keyboard repair gig',
        'Refund from returning a broken mouse to the thrift store',
        'Crowdfunding tip for my open source bug fix',
        'Sold old RAM sticks to a fellow broke coder',
        'Grandpa paid for teaching him about AI'
    ],
    'transfer': [
        'Paid buddy back',
        'Moved cash to my savings',
        'Sent funds to my investment account crypto dream lives on',
        'Split the cost of a group diner meal',
        'Reimbursed fiance',
        'Bank transfer to my side hustle account',
        'Sent cash to friend for gas after a coding jam',
        'Split the cost of a community BBQ I brought the vibes'
    ]
}

transactions = []
for i in range(1, num_transactions + 1):
    date = fake.date_between(start_date=start_date, end_date=end_date)
    customer_id = random.randint(101, 999)
    transaction_type = random.choice(['debit', 'credit', 'transfer'])

    if transaction_type == 'debit':
        amount = round(random.uniform(5, 300), 2)
        description = random.choice(descriptions['debit'])
    elif transaction_type == 'credit':
        amount = round(random.uniform(5, 950), 2)
        description = random.choice(descriptions['credit'])
    else:
        amount = round(random.uniform(10, 500), 2)
        description = random.choice(descriptions['transfer'])

    transactions.append([i, date.strftime('%Y-%m-%d'), customer_id, amount, transaction_type, description])

csv_file = 'developer_transactions.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['transaction_id', 'date', 'customer_id', 'amount', 'type', 'description'])
    writer.writerows(transactions)

print(f"Generated {num_transactions} fake transactions and saved them to '{csv_file}'")