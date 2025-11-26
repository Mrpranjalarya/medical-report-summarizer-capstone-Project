from agents.extractor_agent import ReportExtractor

def test_simple_extract():
    text = "Hemoglobin: 11.2 g/dL\nWBC: 13500 /uL\nPlatelets: 150000 /uL"
    ext = ReportExtractor().extract(text)['extracted']
    assert any(e['name']=='Hemoglobin' for e in ext)
    assert any(e['name']=='WBC' for e in ext)