import psycopg2


DSN = 'dbname=wg_forge_db user=wg_forge password=42a host=localhost port=5432'


def get_mean_median_mode(cursor, column_name):
    query = '''
        SELECT *
        FROM
        (SELECT
        CAST(AVG({column_name}) AS DECIMAL(10,2)) AS {column_name}_mean,
        PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY {column_name})
        AS {column_name}_median,
        (SELECT ARRAY(
        SELECT {column_name}
        FROM cats
        GROUP BY {column_name}
        HAVING COUNT(*) >= ALL(SELECT count(*)
        FROM cats GROUP BY {column_name})) AS {column_name}_mode
        ) AS {column_name}_mode
        FROM cats) AS stats;
    '''
    try:
        cursor.execute(query.format(column_name=column_name))
    except psycopg2.Error as error:
        raise error

    return cursor.fetchall()


def insert_cat_color_info(curs, records):
    try:
        pass
    except psycopg2.Error as error:
        raise error


def main():
    conn = None

    try:
        with psycopg2.connect(DSN) as conn:
            with conn.cursor() as curs:
                tail_stat = get_mean_median_mode(curs, 'tail_length')
                whiskers_stat = get_mean_median_mode(curs, 'whiskers_length')
    except psycopg2.Error as error:
        print(error)
    else:
        print(tail_stat, whiskers_stat)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    main()
