import datetime
import time

from cassandra.cluster import Cluster

TABLE_NETFLIX_PRIMARY = "netflix_master"
TABLE_NETFLIX_TITLES_BY_DATE = "netflix_titles_by_date"
TABLE_NETFLIX_TITLES_BY_RATING = "netflix_titles_by_rating"

TITLE_PULP_FICTION = "Pulp Fiction"
TITLE_LIFE_OF_JIMMY = "Life of Jimmy"

SHOW_ID_LIFE_OF_JIMMY = 100000000
SHOW_ID_PULP_FICTION = 100000001
KEYSPACE_NAME = "demo"
HOST_ADDRESS = "127.0.0.1"


def create_cluster():
    cluster = Cluster([HOST_ADDRESS])
    session = cluster.connect()
    return (cluster, session)


def create_keyspace(session):
    session.execute("CREATE KEYSPACE IF NOT EXISTS " + KEYSPACE_NAME + " WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};	")
    session.set_keyspace(KEYSPACE_NAME)


def create_primary(session):

    create_primary = "CREATE TABLE IF NOT EXISTS " + TABLE_NETFLIX_PRIMARY + " \
        (show_id int, \
        cast list<text>, \
        country list<text>, \
        date_added date, \
        description text, \
        director list <text>, \
        duration text, \
        listed_in list <text>, rating text, release_year int, title text, type text, \
        PRIMARY KEY((title), show_id))"

    print 'Creating Primary Table'
    return session.execute(create_primary)


def create_titles_by_date(session):

    create_titles_by_date = "CREATE TABLE IF NOT EXISTS " + TABLE_NETFLIX_TITLES_BY_DATE + " \
        (show_id int, \
        date_added date, \
        release_year int, \
        title text, \
        type text, \
        PRIMARY KEY((release_year), date_added, show_id)) \
        WITH CLUSTERING ORDER BY (date_added DESC)"

    print 'Creating Titles By Date Table'
    return session.execute(create_titles_by_date)


def create_titles_by_rating(session):

    create_titles_by_rating = "CREATE TABLE IF NOT EXISTS " + TABLE_NETFLIX_TITLES_BY_RATING + " \
        (show_id int, \
        rating text, \
        title text, \
        PRIMARY KEY((rating), show_id))"

    print "Creating Titles By Rating Table"
    return session.execute(create_titles_by_rating)


def prepare_inserts_primary(session):

    insert = "INSERT INTO %s " % (TABLE_NETFLIX_PRIMARY)
    query = insert + \
        "(title, show_id, cast, country, date_added, description, director, duration, listed_in, rating, release_year, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

    print "Preparing: %s " % query
    return session.prepare(query)


def prepare_inserts_date(session):
    insert = "INSERT INTO %s " % (TABLE_NETFLIX_TITLES_BY_DATE)
    query = insert + \
        "(show_id, date_added, release_year, title, type) VALUES(?, ?, ?, ?, ?)"
    print "Preparing: %s " % query
    return session.prepare(query)


def prepare_inserts_rating(session):
    insert = "INSERT INTO %s " % (TABLE_NETFLIX_TITLES_BY_RATING)
    query = insert + \
        "(show_id, rating, title) VALUES (?,?,?)"
    print "Preparing: %s " % query
    return session.prepare(query)


def prepare_reads_all_by_title_primary(session):
    select = "SELECT * FROM %s " % (
        TABLE_NETFLIX_PRIMARY)
    query = select + "WHERE title = ?"
    print "Preparing: %s " % query
    return session.prepare(query)


def prepare_reads_director_by_title_primary(session):
    select_director = "SELECT director FROM %s " % (TABLE_NETFLIX_PRIMARY)
    query = select_director + "WHERE title = ?"
    print "Preparing: %s " % query
    return session.prepare(query)


def prepare_update_director(session):
    update_director = "UPDATE %s " % (TABLE_NETFLIX_PRIMARY)
    query = update_director + \
        "SET director = ? WHERE show_id = ? AND title = ?"
    print "Preparing: %s " % query
    return session.prepare(query)


def insert_primary_records(session, preparedInsertPrimary):

    life_of_jimmy_date_added = datetime.date(2020, 6, 1)
    params_jimmy = [TITLE_LIFE_OF_JIMMY,
                    SHOW_ID_LIFE_OF_JIMMY,
                    ['Jimmy'],
                    ['United States'],
                    life_of_jimmy_date_added,
                    'Experiences of a guitar playing DataStax developer',
                    ['Franky J'],
                    '42 min',
                    ['Action'],
                    'TV-18',
                    2020,
                    'Movie']

    pulp_fiction_date_added = datetime.date(2019, 1, 19)
    paramsPulp = [TITLE_PULP_FICTION,
                  SHOW_ID_PULP_FICTION,
                  ['John Travolta', 'Samuel L. Jackson',
                   'Uma Thurman', 'Harvey Keitel', 'Tim Roth', 'Amanda Plummer', 'Maria de Medeiros',
                   'Ving Rhames', 'Eric Stoltz', 'Rosanna Arquette', 'Christopher Walken',
                   'Bruce Willis'],
                  ['United States'],
                  pulp_fiction_date_added,
                  'This stylized crime caper weaves together stories ...',
                  ['Quentin Tarantino'],
                  '42 min',
                  ['Classic Movies', 'Cult Movies', 'Dramas'],
                  'R',
                  1994,
                  'Movie']

    print "Inserting into Primary Table for title: %s " % (TITLE_LIFE_OF_JIMMY)
    session.execute(preparedInsertPrimary, (params_jimmy))

    print "Inserting into Primary Table for title: %s " % (TITLE_PULP_FICTION)
    session.execute(preparedInsertPrimary, (paramsPulp))


def insert_titles_by_date_records(session, preparedInsertDate):

    params_jimmy = [
        SHOW_ID_LIFE_OF_JIMMY,
        datetime.date(2020, 6, 1),
        2020,
        TITLE_LIFE_OF_JIMMY,
        'Movie'
    ]

    params_pulp = [
        SHOW_ID_PULP_FICTION,
        datetime.date(2019, 1, 19),
        1994,
        TITLE_PULP_FICTION,
        'Movie'
    ]

    print "Inserting into TitlesByDate Table for title: %s" % (
        TITLE_LIFE_OF_JIMMY)
    session.execute(preparedInsertDate, params_jimmy)

    print "Inserting into TitlesByDate Table for title: %s" % (
        TITLE_PULP_FICTION)
    session.execute(preparedInsertDate, params_pulp)


def insert_titles_by_rating_records(session, preparedInsertRating):

    params_jimmy = [
        SHOW_ID_LIFE_OF_JIMMY,
        "TV-18",
        TITLE_LIFE_OF_JIMMY
    ]

    params_pulp = [
        SHOW_ID_PULP_FICTION,
        "R",
        TITLE_PULP_FICTION
    ]
    print "Inserting into TitlesByRating Table for title: %s " % (
        TITLE_LIFE_OF_JIMMY)
    session.execute(preparedInsertRating, params_jimmy)

    print "Inserting into TitlesByRating Table for title: %s " % (
        TITLE_PULP_FICTION)
    session.execute(preparedInsertRating, params_pulp)


def read_all(session, tableName):

    query = "SELECT * FROM %s " % (tableName)
    print "Selecting all from Table: %s" % (tableName)
    query = session.prepare(query)
    return session.execute(query)


def read_all_primary_by_title(session, titleName, prepared_read_by_title_primary):
    params_select = [titleName]

    print "Select all from Primary table with Title: %s" % (titleName)
    return session.execute(prepared_read_by_title_primary, params_select)


def read_director_from_primary_by_title(session, titleName, prepared_read_director_primary):

    params_select = [titleName]
    print "Selecting director from Primary table with Title: %s: " % (
        titleName)
    return session.execute(prepared_read_director_primary, params_select)


def update_director_in_primary_by_title(session, showId, titleName, directorList, prepare_update_director):

    params_update = [directorList, showId, titleName]
    print "Updating director list by Title: %s and Show ID: %s" % (
        titleName, showId)
    return session.execute(prepare_update_director, params_update)


def print_all(result_set):
    print result_set.all()


def main():

    try:
        print ""
        print "Connection to cluster - step 1"
        (cluster, session) = create_cluster()

        try:
            print ""
            print "Creating keyspace - step 2"

            create_keyspace(session)

            print ""
            print "Creating tables - step 3"

            create_primary(session)
            create_titles_by_date(session)
            create_titles_by_rating(session)

            print ""
            print "Creating prepared statements - step 4"
            prepared_insert_primary = prepare_inserts_primary(session)
            prepared_insert_date = prepare_inserts_date(session)
            prepared_insert_rating = prepare_inserts_rating(session)
            prepared_read_director_by_title_primary = prepare_reads_director_by_title_primary(
                session)
            prepared_read_all_by_title_primary = prepare_reads_all_by_title_primary(
                session)
            prepared_update_director = prepare_update_director(session)

            print ""
            print "Inserting records - step 5"
            insert_primary_records(session, prepared_insert_primary)
            insert_titles_by_date_records(session, prepared_insert_date)
            insert_titles_by_rating_records(session, prepared_insert_rating)

            print ""
            print "Reading records - step 6"
            print_all(read_all(session, TABLE_NETFLIX_PRIMARY))
            print ""
            print_all(read_all(session, TABLE_NETFLIX_TITLES_BY_RATING))
            print ""
            print_all(read_all(session, TABLE_NETFLIX_TITLES_BY_DATE))
            print ""
            print_all(read_all_primary_by_title(
                session, TITLE_PULP_FICTION, prepared_read_all_by_title_primary))
            print ""
            print_all(read_director_from_primary_by_title(
                session, TITLE_PULP_FICTION, prepared_read_director_by_title_primary))

            print ""
            print "Updating record with read - step 7"
            update_director_in_primary_by_title(session, SHOW_ID_PULP_FICTION,
                                                TITLE_PULP_FICTION,
                                                ['Quentin Jerome Tarantino'], prepared_update_director)

            print ""
            print_all(read_director_from_primary_by_title(
                session, TITLE_PULP_FICTION, prepared_read_director_by_title_primary))

        finally:
            print "Disconnecting from cluster - step 8"
            try:
                cluster.shutdown()
                time.sleep(2)
            except Exception as shutdownException:
                print ("Error during shutdown: ", shutdownException)
    except Exception as ex:
        print "Something failed during Python Netflix experience"
        print("Error: ", ex)


if __name__ == "__main__":
    main()
