
import os
import sys
sys.path.append(os.path.abspath('./pddlRunner/src'))
import run_pddl
from bottle import Bottle, request, response, static_file

server = Bottle()
@server.hook('after_request')
def enable_cors():
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
  response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@server.route('/image/<file:path>', method=['GET'])
def image(file):
  return static_file(f'./pddlRunner/problems/{file}',root='./')

@server.route('/map/<file:path>', method=['GET'])
def map(file):
  return static_file(f'./PathPlanPrinter/res/{file}',root='./')

@server.route('/', method=['GET'])
def main():
  return static_file('./web/index.html',root='./')

@server.route('/<file:path>', method=['GET'])
def main_helper(file):
  return static_file(f'./web/{file}',root='./')

@server.route('/plan', method=['POST'])
def plan():
  return run_pddl.run_json(request.body.read())

server.run(host='0.0.0.0', port=80, server='gunicorn', workers=4, threads=2,timeout=0)
