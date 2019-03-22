import psycopg2


DSN = 'dbname=wg_forge_db user=wg_forge password=42a host=localhost port=5432'


def get_cats_stat(cursor):
    query = '''
        SELECT *
        FROM
        (SELECT ARRAY(
        SELECT tail_length
        FROM cats
        GROUP BY tail_length
        HAVING COUNT(*) >= ALL(SELECT count(*)
        FROM cats GROUP BY tail_length)) AS tail_length_mode
        ) AS tail_length_mode,
        (SELECT ARRAY(
        SELECT whiskers_length
        FROM cats
        GROUP BY whiskers_length
        HAVING COUNT(*) >= ALL(SELECT count(*)
        FROM cats GROUP BY whiskers_length)) AS twhiskers_length_mode
        ) AS whiskers_length_mode,
        (SELECT
        CAST(AVG(tail_length) AS DECIMAL(10,2)) AS tail_length_mean,
        CAST(AVG(whiskers_length) AS DECIMAL(10,2)) AS whiskers_length_mean,
        PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY tail_length)
        AS tail_length_median,
        PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY whiskers_length)
        AS whiskers_length_median
        FROM cats) AS stats;
    '''

    try:
        cursor.execute(query)
    except psycopg2.Error as error:
        raise error

    return cursor.fetchall()


def main():
    conn = None

    try:
        with psycopg2.connect(DSN) as conn:
            with conn.cursor() as curs:
                cats_statistic = get_cats_stat(curs)
    except psycopg2.Error as error:
        print(error)
    else:
        print(cats_statistic)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    main()
