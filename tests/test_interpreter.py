from agents.interpreter_agent import Interpreter

def test_interpret_known():
    interpreter = Interpreter(ranges_path='medical_ranges.json')
    extracted = [{'name':'Hemoglobin','value':11.2,'unit':'g/dL'}]
    res = interpreter.interpret(extracted, sex='female')
    assert res[0]['status'] in ['low','normal','high']