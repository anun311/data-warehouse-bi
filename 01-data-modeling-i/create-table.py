from typing import NewType

import psycopg2


PostgresCursor = NewType("PostgresCursor", psycopg2.extensions.cursor)
PostgresConn = NewType("PostgresConn", psycopg2.extensions.connection)

table_drop_events = "DROP TABLE IF EXISTS events"
table_drop_actors = "DROP TABLE IF EXISTS actors"
table_drop_repos = "DROP TABLE IF EXISTS repos"
table_drop_orgs = "DROP TABLE IF EXISTS orgs"
table_drop_payloads = "DROP TABLE IF EXISTS payloads"

table_create_actors = """
    CREATE TABLE IF NOT EXISTS actors (
        id int,
        login text,
        PRIMARY KEY(id)
    )
"""
table_create_repos = """
    CREATE TABLE IF NOT EXISTS repos (
        id int,
        repo_name text,
        PRIMARY KEY(id)
    )
"""
table_create_orgs = """
    CREATE TABLE IF NOT EXISTS orgs (
        id int,
        login_name text,
        PRIMARY KEY(id)
    )
"""

table_create_payloads = """
    CREATE TABLE IF NOT EXISTS payloads (
        id text,
        action text,
        issue_id int,
        issue_title text,
        comment_id int,
        commnet_body text,
        created_at timestamp,
        PRIMARY KEY(id)
    )
"""

table_create_events = """
    CREATE TABLE IF NOT EXISTS events (
        id text,
        type text,
        public text,
        actor_id int,
        repo_id int,
        org_id int,
        payload_id text,
        created_at timestamp,
        PRIMARY KEY(id),
        CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actors(id),
        CONSTRAINT fk_repo FOREIGN KEY(repo_id) REFERENCES repos(id)
    )
"""

create_table_queries = [
    table_create_actors,
    table_create_repos,
    table_create_orgs,
    table_create_payloads,
    table_create_events,
]
drop_table_queries = [
    table_drop_events,
    table_drop_repos,
    table_drop_orgs,
    table_drop_payloads,
    table_drop_actors,
]


def drop_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database.
    - Establishes connection with the sparkify database and gets
    cursor to it.
    - Drops all the tables.
    - Creates all tables needed.
    - Finally, closes the connection.
    """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()