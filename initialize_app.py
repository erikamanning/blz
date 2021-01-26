def initialize_database(database):

    print('Creating db tables...')

    database.drop_all()
    database.create_all()

    print('Getting state data...')
    from get_app_data import get_states

    print('Getting position data...')
    from get_app_data import get_positions

    print('Getting party data...')
    from get_app_data import get_parties

    print('Getting legislator data...')
    from get_app_data import get_legislators

    print('Getting bill data...')
    print('(please sit tight! this can take a while)')
    from get_app_data import get_bills

    print('Done! Database is set up!')
