from flask import Flask, render_template, request, abort
import requests
import json

app = Flask("app")

@app.route("/", methods = ['GET', 'POST'])
def hello_world():
    result_names = genTeas()
    if request.method == 'POST':
        user_input = request.form.to_dict() #słownik z formularza
        whatTea = user_input['teaServing'] #jaka herbate chce uzytkownik
        rr = requests.get(url="http://tea_machine:8000/makeTea/" + whatTea)
        if rr.status_code == 200:
            serving = rr.json()["message"]
            return render_template('TeaMachine.html', info=serving, teas=result_names)
        elif rr.status_code == 418:
            messsage = "im a teapot"
            return render_template('TeaMachine.html', info=messsage, teas=result_names)
        else:
            message = f'{rr.status_code} - {rr.json()["detail"]}'
            return render_template('TeaMachine.html', info=messsage, teas=result_names)
    else:
        return render_template('TeaMachine.html', info="hello!", teas = result_names)

@app.route("/add", methods = ['POST'])
def serve():
    #przyciski z herbatami
    result_names = genTeas()

    worker_input = request.form.to_dict()
    try:
        worker_input['quantity'] = int(worker_input['quantity'])
    except:
        raise HTTPException(status_code=422,
                            detail="ilość musi być liczbą")

    rr = requests.put(url="http://tea_machine:8000/addTea/" + worker_input['teaAdd'] + "/" + str(worker_input['quantity']))
    info = rr.json()["message"] + " obecna ilość: " + str(rr.json()["amount"])

    return render_template('TeaMachine.html', teas = result_names, info=info)

@app.errorhandler(500)
def internal_error(error):
    result_names = genTeas()
    return render_template('TeaMachine.html', info="Error!", teas=result_names)

def genTeas():
    r = requests.get(url="http://tea_machine:8000/showAmount")
    results = r.json()
    teas = results["teas"]
    result_names = teas.keys()
    return result_names