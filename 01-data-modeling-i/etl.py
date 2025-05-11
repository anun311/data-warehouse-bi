import glob
import json
import os
from typing import List

import psycopg2 
# libray to connect with PostgreSQL


def get_files(filepath: str) -> List[str]:
    """
    Description: This function is responsible for listing the files in a directory
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    return all_files


def process(cur, conn, filepath):
    # Get list of files from filepath
    all_files = get_files(filepath)

    for datafile in all_files:
        with open(datafile, "r") as f:
            data = json.loads(f.read())
            for each in data:
                # Print some sample data
                
                if each["type"] == "IssueCommentEvent":
                    id_ = each["id"]
                    print(id_)
                    type_ = each["type"]
                    public_ = each["public"]
                    created_at = str(each["created_at"])
                    created_at = created_at[:10] + " " + created_at[11:19]

                    actor_id = each["actor"]["id"]
                    actor_login = each["actor"]["login"]
                    repo_id = each["repo"]["id"]
                    repo_name = each["repo"]["name"]
                    pl_action = each["payload"]["action"]
                    pl_issue_id = each["payload"]["issue"]["id"]

                    pl_issue_title = each["payload"]["issue"]["title"]
                    pl_issue_title = pl_issue_title.replace("'", "")

                    pl_comm_id = each["payload"]["comment"]["id"]
                    pl_comm_body = each["payload"]["comment"]["body"]
                    pl_comm_body = pl_comm_body.replace("'", "")

                    pl_comm_created = str(each["payload"]["comment"]["created_at"])
                    pl_comm_created = pl_comm_created[:10] + " " + pl_comm_created[11:19]

                    org_id = each["org"]["id"]
                    org_login = each["org"]["login"]
                    payload_id = str(pl_issue_id) + "-" + str(pl_comm_id)

                    # Insert data into tables here
                    insert_actor_statement = f"""
                        INSERT INTO actors (
                            id,
                            login
                        ) VALUES ({actor_id}, '{actor_login}')
                        ON CONFLICT (id) DO NOTHING
                    """
                    cur.execute(insert_actor_statement)

                    insert_repo_statement = f"""
                        INSERT INTO repos (
                            id,
                            repo_name
                        ) VALUES ({repo_id}, '{repo_name}')
                        ON CONFLICT (id) DO NOTHING
                    """
                    cur.execute(insert_repo_statement)

                    insert_org_statement = f"""
                        INSERT INTO orgs (
                            id,
                            login_name
                        ) VALUES ({org_id}, '{org_login}')
                        ON CONFLICT (id) DO NOTHING
                    """
                    cur.execute(insert_org_statement)

                    insert_payload_statement = f"""
                        INSERT INTO payloads (
                            id,
                            action,
                            issue_id,
                            issue_title,
                            comment_id,
                            commnet_body,
                            created_at
                        ) VALUES ('{payload_id}', '{pl_action}', {pl_issue_id}, '{pl_issue_title}', {pl_comm_id}, '{pl_comm_body}', '{pl_comm_created}')
                        ON CONFLICT (id) DO NOTHING
                    """
                    cur.execute(insert_payload_statement)

                    insert_event_statement = f"""
                        INSERT INTO events (
                            id,
                            type,
                            public,
                            actor_id,
                            repo_id,
                            org_id,
                            payload_id,
                            created_at
                        ) VALUES ({id_}, '{type_}', '{public_}', {actor_id}, {repo_id}, {org_id}, '{payload_id}', '{created_at}')
                        ON CONFLICT (id) DO NOTHING
                    """
                    cur.execute(insert_event_statement)

                else:
                    id_ = each["id"]
                    print(id_)
                    type_ = each["type"]
                    public_ = each["public"]
                    created_at = str(each["created_at"])
                    created_at = created_at[:10] + " " + created_at[11:19]

                    actor_id = each["actor"]["id"]
                    actor_login = each["actor"]["login"]
                    repo_id = each["repo"]["id"]
                    repo_name = each["repo"]["name"]
                    org_id = None
                    payload_id = None

                    # Insert data into tables here
                    insert_actor_statement = f"""
                        INSERT INTO actors (
                            id,
                            login
                        ) VALUES ({actor_id}, '{actor_login}')
                        ON CONFLICT (id) DO NOTHING
                    """
                    cur.execute(insert_actor_statement)

                    insert_repo_statement = f"""
                        INSERT INTO repos (
                            id,
                            repo_name
                        ) VALUES ({repo_id}, '{repo_name}')
                        ON CONFLICT (id) DO NOTHING
                    """
                    cur.execute(insert_repo_statement)

                    insert_event_statement = f"""
                        INSERT INTO events (
                            id,
                            type,
                            public,
                            actor_id,
                            repo_id,
                            org_id,
                            payload_id,
                            created_at
                        ) VALUES ({id_}, '{type_}', '{public_}', {actor_id}, {repo_id}, NULL, NULL, '{created_at}')
                        ON CONFLICT (id) DO NOTHING
                    """
                    cur.execute(insert_event_statement)

                conn.commit()


def main():
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()

    process(cur, conn, filepath="../data")

    conn.close()


if __name__ == "__main__":
    main()