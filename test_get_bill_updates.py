from app import db, headers
from models import Bill
from get_bill_updates import get_bill_updates


most_recent_update_date = '2021-01-15'

most_recently_updated_bills = Bill.query.filter(Bill.latest_major_action_date==most_recent_update_date).all()
print(most_recently_updated_bills)

for bill in most_recently_updated_bills:

    print(f'Bill: {bill.id}, Date: {bill.latest_major_action_date}')
    bill.latest_major_action = 'nyehehehehe'
    bill.latest_major_action_date = '99-99-99'

db.session.add_all(most_recently_updated_bills)
db.session.commit()

#  check bills deleted
recent_bill_check = Bill.query.filter(Bill.latest_major_action_date=='99-99-99').all()



for bill in recent_bill_check:

    print(f'Bill: {bill.id}, Date: {bill.latest_major_action_date}')
    print(f'Date: {bill.latest_major_action_date}')
    print(f'Update: {bill.latest_major_action}')


print('******************************')
print('Getting bill updates... ')
print('******************************')


get_bill_updates("both",117 )

recent_bill_check = Bill.query.filter(Bill.latest_major_action_date==most_recent_update_date).all()


print('******************************')
print('New Bills Found!!')
print('******************************')


for bill in recent_bill_check:

    print(f'Bill: {bill.id}, Date: {bill.latest_major_action_date}')
    print(f'Date: {bill.latest_major_action_date}')
    print(f'Update: {bill.latest_major_action}')
