import matlab.engine
eng = matlab.engine.connect_matlab()
while(true):
    x = eng.workspace['m']
    print(x)