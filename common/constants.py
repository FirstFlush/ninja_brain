from django.db import IntegrityError, DataError, DatabaseError


MODEL_PATH = "en_streetninja"

DB_WRITE_EXCEPTIONS  = (IntegrityError, DataError, DatabaseError)