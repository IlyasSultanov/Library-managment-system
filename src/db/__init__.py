from fastapi import Depends
from .database import get_db

DepSession = Depends(get_db)
