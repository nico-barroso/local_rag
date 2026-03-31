from frontend.app_interface import render_chat
from pipeline.indexer import load_indexer

index = load_indexer()
render_chat()
