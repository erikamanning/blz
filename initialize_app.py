
def initialize_database(database):

    database.drop_all()
    database.create_all()

    from get_app_data import get_states
    from get_app_data import get_positions
    from get_app_data import get_parties
    from get_app_data import get_legislators
    from get_app_data import get_bills
