# External
from flask import Flask, request, jsonify
import traceback
import sys

# Internal 
from blockchain import BlockchainCore
BlockchainCore()

'''
    TODO: secure the API
        1. Make https
        2. Add validators
        3. Add server error wrapper
'''



app = Flask(__name__)
app.run('0.0.0.0', debug=False)

@app.errorhandler(Exception)
def handle_exception(e):
    # Get current system exception
    ex_type, ex_value, ex_traceback = sys.exc_info()

    # Extract unformatter stack traces as tuples
    trace_back = traceback.extract_tb(ex_traceback)

    # Format stacktrace
    stack_trace = list()

    for trace in trace_back:
        stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

    print("Exception type : %s " % ex_type.__name__)
    print("Exception message : %s" %ex_value)
    print('Stack trace: ')
    for p in stack_trace:
        print(p)

    return { 
        'error': True, 
        f'{ex_type.__name__}': f'{ex_value}' 
    }, 500 # Internal server error

@app.route('/v1/health')
def index():
    return { 'status': 'OK' }

import routes.blockchain.routes