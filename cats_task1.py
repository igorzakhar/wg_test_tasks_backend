import psycopg2
from psycopg2.extras import execute_values
from terminaltables import AsciiTable


DSN = 'dbname=wg_forge_db user=wg_forge password=42a host=localhost port=5432'


def main():
    conn = None

    try:
        with psycopg2.connect(DSN) as conn:
            with conn.cursor() as curs:
                clear_cat_color_info(curs)
                colors_info = select_count_colors(curs)
                insert_cat_color_info(curs, colors_info)
                print_table(curs, 'cat_colors_info')
    except psycopg2.Error as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def clear_cat_color_info(cursor):
    try:
        cursor.execute('DELETE FROM cat_colors_info')
    except psycopg2.Error as error:
        raise error


def select_count_colors(cursor):
    try:
        cursor.execute(
            'SELECT color, COUNT(color) FROM cats GROUP BY color'
        )
    except psycopg2.Error as error:
        raise error
    return cursor.fetchall()


def insert_cat_color_info(curs, records):
    try:
        execute_values(
            curs,
            'INSERT INTO cat_colors_info (color, count) VALUES %s',
            records
        )
    except psycopg2.Error as error:
        raise error


def print_table(cursor, table_name):
    cursor.execute('SELECT * FROM {}'.format(table_name))

    table_records = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    table_records.insert(0, column_names)

    table_instance = AsciiTable(table_records)
    table_instance.outer_border = False
    table_instance.justify_columns[len(column_names) - 1] = 'right'

    print(table_instance.table)
    print('({} rows)\n'.format(len(table_records[1:])))


if __name__ == '__main__':
    main()
