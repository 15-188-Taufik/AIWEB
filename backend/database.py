from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ini connection string dari NeonDB kamu (sudah saya bersihkan)
# Perhatikan: kita pakai 'postgresql+psycopg2' agar lebih eksplisit, 
# tapi 'postgresql://' saja biasanya juga jalan.
SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_ohItT4R0jfzL@ep-broad-rain-a1bdqlj8-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

# Opsi connect_args mungkin dibutuhkan untuk SSL di beberapa environment, 
# tapi untuk Neon biasanya URL di atas sudah cukup.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()