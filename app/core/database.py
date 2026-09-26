from sqlalchemy import create_engine , text
from sqlalchemy.orm import sessionmaker,declarative_base

database_url = ( 
    "mssql+pyodbc://@LAPTOP-TOD3072S/employeepayrolldb"
    "?driver=ODBC+driver+18+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)
engine = create_engine(database_url)

sessionLocal = sessionmaker(
    autocommit=False , autoflush=False, bind = engine
)


Base = declarative_base()

def get_db():
    db = sessionLocal()
    try :
        yield db
    finally:
        db.close()

''' to check wether the database is connected successfully or not.'''
# try:
#     with engine.connect() as connection:
#         result = connection.execute(text("SELECT 1"))
#         print("Database connected successfully!")
#         print(result.fetchone())
# except Exception as e:
#     print("Database connection failed!")
#     print(e)
