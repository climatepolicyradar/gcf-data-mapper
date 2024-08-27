from gcf_data_mapper.parsers.collection import collection


def test_returns_empty():
    collection_data = collection()
    assert collection_data == []
