import csv
from sqlalchemy.exc import IntegrityError
from database import Dev, Empresa, Session

def migrate_devs():
    session = Session()
    with open("devs-data.csv", mode="r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # Se o arquivo CSV tiver mais colunas do que o esperado, use slicing
            name, email, cel, habilidades, password, *extra = row  # Captura colunas extras em *extra

            # Verifica se o desenvolvedor já existe no banco de dados
            existing_dev = session.query(Dev).filter_by(name=name).first()

            if not existing_dev:
                dev = Dev(
                    name=name.strip(),
                    email=email.strip(),
                    cel=cel.strip(),
                    habilidades=habilidades.strip(),
                    password=password.strip()
                )
                session.add(dev)
            else:
                print(f"Desenvolvedor '{name}' já existe no banco de dados.")

    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()  # Em caso de erro, desfaz as mudanças
        print(f"Erro de integridade ao inserir devs: {e}")
    finally:
        session.close()

def migrate_empresas():
    session = Session()
    with open("empresas-data.csv", mode="r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            name, email, cel, habilidades, password, *extra = row  # Captura colunas extras em *extra

            # Verifica se a empresa já existe no banco de dados
            existing_empresa = session.query(Empresa).filter_by(name=name).first()

            if not existing_empresa:
                empresa = Empresa(
                    name=name.strip(),
                    email=email.strip(),
                    cel=cel.strip(),
                    habilidades=habilidades.strip(),
                    password=password.strip()
                )
                session.add(empresa)
            else:
                print(f"Empresa '{name}' já existe no banco de dados.")

    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade ao inserir empresas: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    migrate_devs()  # Migra desenvolvedores
    migrate_empresas()  # Migra empresas
