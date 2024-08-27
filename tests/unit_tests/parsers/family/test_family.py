from gcf_data_mapper.parsers.family import family


def test_returns_empty():
    family_data = family()
    assert family_data == []
