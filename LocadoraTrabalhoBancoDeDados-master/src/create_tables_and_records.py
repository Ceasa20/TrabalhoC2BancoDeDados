from pathlib import Path

from conexion.oracle_queries import OracleQueries

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"


def create_tables(query:str):
    list_of_commands = query.split(";")

    oracle = OracleQueries(can_write=True)
    oracle.connect()

    for command in list_of_commands:
        command = command.strip()
        if command:
            print(command)
            try:
                oracle.executeDDL(command)
                print("Successfully executed")
            except Exception as e:
                    print(f"Falha ao executar comando SQL: {e}")
                    raise
def generate_records(query:str, sep:str=';'):
    list_of_commands = query.split(sep)

    oracle = OracleQueries(can_write=True)
    oracle.connect()

    for command in list_of_commands:
        command = command.strip()
        if command:
            print(command)
            oracle.write(command)
            print("Successfully executed")

def run():

    with (SQL_DIR / "create_tables.sql").open(encoding="utf-8") as f:
        query_create = f.read()

    print("Creating tables...")
    create_tables(query=query_create)
    print("Tables successfully created!")

    # with (SQL_DIR / "inserting_samples_records.sql").open(encoding="utf-8") as f:
    #     query_generate_records = f.read()

    # print("Gerenating records")
    # generate_records(query=query_generate_records)
    # print("Records successfully generated!")

    with (SQL_DIR / "inserirDados.sql").open(encoding="utf-8") as f:
        query_generate_records = f.read()

    print("Gerenating records")
    generate_records(query=query_generate_records)
    print("Records successfully generated!")


if __name__ == '__main__':
    run()