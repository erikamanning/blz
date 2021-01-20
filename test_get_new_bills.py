from app import db, headers
from models import Bill
from get_new_bills import get_new_bills


most_recent_bill_date = '2021-01-15'

most_recent_bills = Bill.query.filter(Bill.introduced_date==most_recent_bill_date).all()
print(most_recent_bills)

for bill in most_recent_bills:

    print(f'Bill: {bill.id}, Date: {bill.introduced_date}')
    db.session.delete(bill)


db.session.commit()

#  check bills deleted
recent_bill_check = Bill.query.filter(Bill.introduced_date==most_recent_bill_date).all()

if recent_bill_check:

    for bill in recent_bill_check:

        print('New Bills Found!!')
        print(f'Bill: {bill.id}, Date: {bill.introduced_date}')

else:

    print('No bills found for ', most_recent_bill_date)


print('******************************')
print('Getting new bills: ')
print('******************************')


get_new_bills(117,"both", "introduced")

recent_bill_check = Bill.query.filter(Bill.introduced_date==most_recent_bill_date).all()

if recent_bill_check:

    print('New bills found!')
    for bill in recent_bill_check:

        print(f'Bill: {bill.id}, Date: {bill.introduced_date}')

else:

    print('No bills found for ', most_recent_bill_date)
