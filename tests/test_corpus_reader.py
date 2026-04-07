import os

from app.rag.corpus.reader import reader


def test_dir_reader(tmp_doc_dir, tmp_file):

    new_tmp_directory = tmp_doc_dir
    print("Temporary directory created", new_tmp_directory)

    tmp_dir_path = os.path.join(new_tmp_directory, "ingest_text_tmp.text")
    new_tmp_file = tmp_file(tmp_dir_path)
    print("Temporary file created", new_tmp_file)

    load_tmp_directory = reader(input_dir=new_tmp_directory)
    assert len(load_tmp_directory) == 1, "Reader is working correctly"
