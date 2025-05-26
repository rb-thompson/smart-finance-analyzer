import csv
from datetime import datetime
import random
from faker import Faker

fake = Faker()

num_transactions = 500
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 12, 31)

descriptions = {
    'debit': [
        'Repairs for the farmhouse roof',
        'Electricity bill for the household',
        'Starlink subscription for internet access',
        'Grocery shopping for family meals',
        'Coffee for morning routine',
        'Taco purchase from local food truck',
        'Renewed free tier IDE license',
        'Paid for cloud storage for coding projects',
        'Drove to town for job fair',
        'Bought used programming book from thrift store',
        'Gas for driving to town',
        'Firewood for home heating',
        'Donated to open source project',
        'Garden supplies for vegetable patch',
        'Household expenses for cleaning supplies',
        'Flour for baking bread',
        'Replaced USB cable for computer',
        'Library card for internet access',
        'Bought used monitor for coding setup',
        'Vet bill for dog medical care',
        'Donated to coding community project',
        'Batteries for computer backup system',
        'School supplies for teenagers',
        'Sports equipment for teen activities',
        'Chicken feed for the coop',
        'Cat food for household pets',
        'Commuting gas for hospital job',
        'Medical coding certification renewal',
        'Work scrubs for hospital shifts',
        'Teen clothing for school'
    ],
    'credit': [
        'Fixed neighbors computer for payment',
        'Sold app prototype to local business',
        'Found cash in old clothing',
        'Tax refund from previous year',
        'Neighbor paid for router setup',
        'Sold chicken eggs at local market',
        'Bartered coding help for farm goods',
        'Payment for small repair job',
        'Refund from returned computer accessory',
        'Crowdfunding tip for open source contribution',
        'Sold old computer parts locally',
        'Payment for teaching basic computer skills',
        'Hospital paycheck for medical coding',
        'Overtime pay for hospital shift'
    ],
    'transfer': [
        'Paid friend for shared meal cost',
        'Moved funds to household savings',
        'Sent funds to investment account',
        'Split cost of family dinner out',
        'Reimbursed Jessica for grocery run',
        'Paid neighbor for shared internet data',
        'Sent funds for teen school trip',
        'Split cost of community event'
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