import os
from psycopg_pool import ConnectionPool


pool = ConnectionPool(conninfo=os.environ["DATABASE_URL"])


class TruckQueries:
    def get_truck(self, truck_id):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT u.id AS user_id, u.first, u.last,
                        u.avatar, u.email, u.username,
                        t.id AS truck_id, t.name,
                        t.website, t.category,
                        t.vegetarian_friendly
                    FROM users u
                    JOIN trucks t ON(u.id = t.owner_id)
                    WHERE t.id = %s
                    """,
                    [truck_id],
                )

                truck = None
                row = cur.fetchone()

                if row is not None:
                    truck = {}
                    truck_fields = [
                        "truck_id",
                        "name",
                        "website",
                        "category",
                        "vegetarian_friendly",
                    ]
                    for i, column in enumerate(cur.description):
                        if column.name in truck_fields:
                            truck[column.name] = row[i]
                    truck["id"] = truck["truck_id"]

                    owner = {}
                    owner_fields = [
                        "user_id",
                        "first",
                        "last",
                        "avatar",
                        "email",
                        "username",
                    ]
                    for i, column in enumerate(cur.description):
                        if column.name in owner_fields:
                            owner[column.name] = row[i]
                    owner["id"] = owner["user_id"]

                    truck["owner"] = owner
                return truck


class UserQueries:
    def get_all_users(self):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, first, last, avatar,
                        email, username
                    FROM users
                    ORDER BY last, first
                """
                )

                results = []
                for row in cur.fetchall():
                    record = {}
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]
                    results.append(record)

                return results

    def get_user(self, id):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, first, last, avatar,
                        email, username
                    FROM users
                    WHERE id = %s
                """,
                    [id],
                )

                record = None
                row = cur.fetchone()
                if row is not None:
                    record = {}
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]

                return record

    def create_user(self, data):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                params = [
                    data.first,
                    data.last,
                    data.avatar,
                    data.email,
                    data.username,
                ]
                cur.execute(
                    """
                    INSERT INTO users (first, last, avatar, email, username)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, first, last, avatar, email, username
                    """,
                    params,
                )

                record = None
                row = cur.fetchone()
                if row is not None:
                    record = {}
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]

                return record

    def update_user(self, user_id, data):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                params = [
                    data.first,
                    data.last,
                    data.avatar,
                    data.email,
                    data.username,
                    user_id,
                ]
                cur.execute(
                    """
                    UPDATE users
                    SET first = %s
                      , last = %s
                      , avatar = %s
                      , email = %s
                      , username = %s
                    WHERE id = %s
                    RETURNING id, first, last, avatar, email, username
                    """,
                    params,
                )

                record = None
                row = cur.fetchone()
                if row is not None:
                    record = {}
                    for i, column in enumerate(cur.description):
                        record[column.name] = row[i]

                return record

    def delete_user(self, user_id):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM users
                    WHERE id = %s
                    """,
                    [user_id],
                )
