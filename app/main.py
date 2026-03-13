import os

from pipeline.indexer import indexer
from pipeline.queries import query

indexer()

print(query())
