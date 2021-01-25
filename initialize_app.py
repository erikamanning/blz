
def initialize_database(database):

    database.drop_all()
    database.create_all()

    import get_states
    import get_positions
    import get_parties
    import get_legislators
    import get_bills
