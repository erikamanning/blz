def update_db(session):

    print('Getting bill updates...')
    from get_app_data import get_bill_updates   

    print('Getting new bills...')
    from get_app_data import get_new_bills

    print('Done! App data is updated.')
 