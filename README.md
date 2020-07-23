# DataStax Desktop - Python Netflix example
An introduction to using the Cassandra database with well-defined steps to optimize your learning. Using a Netflix dataset for sample data, your locally running Cassandra database will contain a minimal set of show data for you to customize and experiment with.

Contributors:
* [Jeff Banks](https://github.com/jeffbanks)
* [Chris Splinter](https://github.com/csplinter)
* [Jamie Gillenwater](https://github.com/jgillenwater)

## Objectives

* Leverage DataStax driver APIs for interaction with a local running Cassandra database.
* Set up a Cassandra Query Language (CQL) session and perform operations such as creating, reading, and writing.
* Use the Netflix show dataset as example information across three differently constructed tables.
* Observe how the partition key along with clustering keys produce an optimized experience.
* Have fun!

## Project Layout

* [app.py](app.py) - main application file
* [netflix-shows.cql](netflix-shows.cql) - file to create the schema

## How this works
To get started, read the `app.py` comments to learn the steps for interacting with your Cassandra database. The functions invoked by `app.py` are created to provide more flexibility for modifications as you learn.

## Setup and running

### Prerequisites
If using [DataStax Desktop](https://www.datastax.com/blog/2020/05/learn-cassandra-datastax-desktop), no prerequisites are required. The Cassandra instance is provided with the DataStax Desktop stack as part of provisioning.

If NOT using DataStax Desktop, spin up your own local instance of Cassandra exposing its address and port to align with the settings in the `app.py` file.  You will need to install and perform the following steps:

* A running instance of Apache Cassandra® 2.1+
* Python 2.7, 3.4, 3.5, or 3.6.
* Installed Cassandra driver: `pip install cassandra-driver`
* virtualenv (recommended)

All of the connection code is contained in the `app.py` file.  The `create_cluster` function is used to connect to your instance of Cassandra.

```python
from cassandra.cluster import Cluster
cluster = Cluster(["127.0.0.1"])
session = cluster.connect()
```

## Running
Start the app from the command line.

> python app.py

### Console output

```
Connection to cluster - step 1

Creating keyspace - step 2

Creating tables - step 3
Creating Primary Table
Creating Titles By Date Table
Creating Titles By Rating Table

Creating prepared statements - step 4
Preparing: INSERT INTO netflix_master (title, show_id, cast, country, date_added, description, director, duration, listed_in, rating, release_year, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
Preparing: INSERT INTO netflix_titles_by_date (show_id, date_added, release_year, title, type) VALUES(?, ?, ?, ?, ?)
Preparing: INSERT INTO netflix_titles_by_rating (show_id, rating, title) VALUES (?,?,?)
Preparing: SELECT director FROM netflix_master WHERE title = ?
Preparing: SELECT * FROM netflix_master WHERE title = ?
Preparing: UPDATE netflix_master SET director = ? WHERE show_id = ? AND title = ?

Inserting records - step 5
Inserting into Primary Table for title: Life of Jimmy
Inserting into Primary Table for title: Pulp Fiction
Inserting into TitlesByDate Table for title: Life of Jimmy
Inserting into TitlesByDate Table for title: Pulp Fiction
Inserting into TitlesByRating Table for title: Life of Jimmy
Inserting into TitlesByRating Table for title: Pulp Fiction

Reading records - step 6
Selecting all from Table: netflix_master
[Row(title=u'Life of Jimmy', show_id=100000000, cast=[u'Jimmy'], country=[u'United States'], date_added=Date(18414), description=u'Experiences of a guitar playing DataStax developer', director=[u'Franky J'], duration=u'42 min', listed_in=[u'Action'], rating=u'TV-18', release_year=2020, type=u'Movie'), Row(title=u'Pulp Fiction', show_id=100000001, cast=[u'John Travolta', u'Samuel L. Jackson', u'Uma Thurman', u'Harvey Keitel', u'Tim Roth', u'Amanda Plummer', u'Maria de Medeiros', u'Ving Rhames', u'Eric Stoltz', u'Rosanna Arquette', u'Christopher Walken', u'Bruce Willis'], country=[u'United States'], date_added=Date(17915), description=u'This stylized crime caper weaves together stories ...', director=[u'Quentin Tarantino'], duration=u'42 min', listed_in=[u'Classic Movies', u'Cult Movies', u'Dramas'], rating=u'R', release_year=1994, type=u'Movie')]

Selecting all from Table: netflix_titles_by_rating
[Row(rating=u'TV-18', show_id=100000000, title=u'Life of Jimmy'), Row(rating=u'R', show_id=100000001, title=u'Pulp Fiction')]

Selecting all from Table: netflix_titles_by_date
[Row(release_year=2020, date_added=Date(18414), show_id=100000000, title=u'Life of Jimmy', type=u'Movie'), Row(release_year=1994, date_added=Date(17915), show_id=100000001, title=u'Pulp Fiction', type=u'Movie')]

Select all from Primary table with Title: Pulp Fiction
[Row(title=u'Pulp Fiction', show_id=100000001, cast=[u'John Travolta', u'Samuel L. Jackson', u'Uma Thurman', u'Harvey Keitel', u'Tim Roth', u'Amanda Plummer', u'Maria de Medeiros', u'Ving Rhames', u'Eric Stoltz', u'Rosanna Arquette', u'Christopher Walken', u'Bruce Willis'], country=[u'United States'], date_added=Date(17915), description=u'This stylized crime caper weaves together stories ...', director=[u'Quentin Tarantino'], duration=u'42 min', listed_in=[u'Classic Movies', u'Cult Movies', u'Dramas'], rating=u'R', release_year=1994, type=u'Movie')]

Selecting director from Primary table with Title: Pulp Fiction:
[Row(director=[u'Quentin Tarantino'])]

Updating record with read - step 7
Updating director list by Title: Pulp Fiction and Show ID: 100000001

Selecting director from Primary table with Title: Pulp Fiction:
[Row(director=[u'Quentin Jerome Tarantino'])]
Disconnecting from cluster - step 8
```

### Having trouble?
Are you getting errors reported but can't figure out what to do next?  Copy your log output, document any details, and head over to the [DataStax Community](https://community.datastax.com/spaces/131/datastax-desktop.html) to get some assistance.

### Questions or comments?
If you have any questions or want to post a feature request, visit the [Desktop space at DataStax Community](https://community.datastax.com/spaces/131/datastax-desktop.html)
