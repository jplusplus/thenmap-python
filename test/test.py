from thenmap import Thenmap


def test_initing():
    api = Thenmap()
    se_7 = api["se-7"]

    assert(type(se_7).__name__ is "Dataset")
