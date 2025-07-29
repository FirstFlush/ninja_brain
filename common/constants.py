from django.db import IntegrityError, DataError, DatabaseError

DB_WRITE_EXCEPTIONS  = (IntegrityError, DataError, DatabaseError)