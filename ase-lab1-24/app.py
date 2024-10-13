from flask import Flask, request, make_response, jsonify
import random, time, os, threading
from functools import reduce
from ast import literal_eval

app = Flask(__name__)

#Endpoint /add for addition which takes a and b as query parameters.
@app.route('/add')
def add():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        save_last("add",(a,b),a+b)
        return make_response(jsonify(s=a+b), 200) #HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST

#Endpoint /sub for subtraction which takes a and b as query parameters.
@app.route('/sub')
def sub():
    a = request.args.get('a',type = float)
    b = request.args.get('b',type = float)
    if a and b:
        save_last("sub",(a,b),a-b)
        return make_response(jsonify(s=a-b), 200) #HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST
    
#Endpoint /mul for multiplication which takes a and b as query parameters.
@app.route('/mul')
def mul():
    a = request.args.get('a',type = float)
    b = request.args.get('b',type = float)
    if a and b:
        save_last("mul",(a,b),a*b)
        return make_response(jsonify(s=a*b), 200) #HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST

#Endpoint /div for division which takes a and b as query parameters. Returns HTTP 400 BAD REQUEST also for division by zero.
@app.route('/div')
def div():
    a = request.args.get('a',type = float)
    b = request.args.get('b',type = float)
    if (a and b) and (b != 0):
        save_last("div",(a,b),a/b)
        return make_response(jsonify(s=a/b), 200) #HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST

#Endpoint /mod for modulo which takes a and b as query parameters. Returns HTTP 400 BAD REQUEST also for division by zero.
@app.route('/mod')
def mod():
    a = request.args.get('a',type = float)
    b = request.args.get('b',type = float)
    if (a and b) and (b != 0):
        save_last("mod",(a,b),a%b)
        return make_response(jsonify(s=a%b), 200) #HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST

#Endpoint /random which takes a and b as query parameters and returns a random number between a and b included. Returns HTTP 400 BAD REQUEST if a is greater than b.
@app.route('/rand')
def rand():
    a = request.args.get('a',type = float)
    b = request.args.get('b',type = float)
    #Random number
    randomNum = random.uniform(a,b)
    if (a and b) and (randomNum < b):
        save_last("randomNum",(a,b),res)
        return make_response(jsonify(randomNum), 200)
    else:
        return make_response(str(randomNum) + ' is an Invalid Random Number\n', 400)

#Endpoint /upper which given the string a it returns it in a JSON all in uppercase.
@app.route('/upper')
def upper():
    a = request.args.get('a', type = str)
    if a:
        save_last("upper","("+a+")", a)
        return make_response(jsonify(a.upper()), 200)
    else:
        return make_response('Invalid Type of Input\n', 400)

#Endpoint /lower which given the string a it returns it in a JSON all in lowercase.
@app.route('/lower')
def lower():
    a = request.args.get('a', type = str)
    if a:
        save_last("lower","("+a+")",a)
        return make_response(jsonify(a.lower()), 200)
    else:
        return make_response('Invalid Type of Input\n', 400)

#Endpoint /concat which given the strings a and b it returns in a JSON the concatenation of them.
@app.route('/concat')
def concat():
    a = request.args.get('a', type = str)
    b = request.args.get('b', type = str)
    s = a + b
    if a and b:
        save_last("concat",(a,b), s)
        return make_response(jsonify(s), 200)
    else:
        return make_response('Invalid Type of Input\n', 400)
    

#Endpoint /reduce which takes the operator op (one of add, sub, mul, div, concat) and a lst string representing a
#list and apply the operator to all the elements giving the result. 
# For instance, /reduce?op=add&lst=[2,1,3,4] returns a JSON containing {s=10}, meaning 2+1+3+4.
@app.route('/reduce')
def red_endpoint():
    op = request.args.get('op', type=str)
    lst = request.args.get('lst', type=lambda x: literal_eval(x))

    if not op or not lst:
        return make_response('Invalid input\n', 400)   
    if op == 'add':
        result = reduce(lambda x, y: x + y, lst)
    elif op == 'sub':
        result = reduce(lambda x, y: x - y, lst)
    elif op == 'mul':
        result = reduce(lambda x, y: x * y, lst)
    elif op == 'div':
        result = reduce(lambda x, y: x / y, lst)
    elif op == 'concat':
        result = "".join(map(str, lst))
    else:
        return make_response('Invalid operation\n', 400)
    save_last("reduce",(op,lst),result)
    return make_response(jsonify(s = result), 200)

#Endpoint /crash which terminates the service execution after responding to the client with info about the host
# (L'host è il computer o server che ospita il servizio) and the port of the service.
@app.route('/crash')
def crash():
    def close():
        time.sleep(1)
        os._exit(0)
    thread = threading.Thread(target=close)
    thread.start()
    ret = str(request.host) + " crashed"
    return make_response(jsonify(s=ret), 200)

# Endpoint /last che restituisce una stringa che rappresenta l'ultima operazione richiesta con successo,
# nel formato op(args)=res, ad esempio add(2.0,3.0)=5.0 oppure reduce('add',[2,1,3,4])=10 o rand(1,3)=2.
# Risponde con il codice HTTP 404 se nessuna operazione è stata eseguita.
# Suggerimento: per fare ciò, è necessario modificare gli altri endpoint e utilizzare un file.

@app.route('/last')
def last():
    try:
        with open('last.txt', 'r') as f:
            return make_response(jsonify(s=f.read()), 200)
    except FileNotFoundError:
        return make_response('No operations yet\n', 404)


def save_last(op,args,res):
    with open('last.txt', 'w') as f:
            f.write(f'{op}{args}={res}')


if __name__ == '__main__':
    app.run(debug=True)









