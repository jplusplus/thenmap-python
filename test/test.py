from thenmap import Thenmap


def test_initing():
    api = Thenmap()
    se_7 = api["se-7"]

    assert(type(se_7).__name__ is "Dataset")

def test_date():
    api = Thenmap()
    se_7 = api["se-7"]
    assert(len(se_7.geojson["features"]) == 290)
    se_7.date = "1975-05-03"
    assert(len(se_7.geojson["features"]) == 277)
    se_7.date = "1971-12-24"
    assert(len(se_7.geojson["features"]) == 346)

