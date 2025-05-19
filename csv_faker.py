import csv
from datetime import datetime
import random
from faker import Faker

fake = Faker()

num_transactions = 500000
start_date = datetime(2016, 1, 1)
end_date = datetime(2024, 12, 31)

descriptions = {
    'debit': [
        'Monthly rent payment',
        'Electricity bill',
        'Internet service',
        'Grocery shopping',
        'Coffee at local cafe',
        'Lunch at restaurant',
        'Online course subscription',
        'Software license renewal',
        'Cloud service fee',
        'Purchase of new gadget',
        'Video game purchase',
        'Streaming service subscription',
        'Weekend getaway',
        'Book purchase',
        'Public transportation fare',
        'Gym membership',
        'Donation to open source project',
        'Home improvement supplies',
        'Concert ticket',
        'Food order'
    ],
    'credit': [
        'Monthly salary deposit',
        'Freelance project payment',
        'Dividends from investments',
        'Tax refund',
        'Gift received',
        'Sale of old electronics'
    ],
    'transfer': [
        'Payment to friend for dinner',
        'Transfer to savings account',
        'Transfer to investment account',
        'Shared accommodation expenses',
        'Reimbursement for shared purchase'
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
        amount = round(random.uniform(500, 10000), 2)
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