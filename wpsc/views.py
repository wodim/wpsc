import re
from subprocess import Popen

from flask import render_template, abort, jsonify

from app import app, redis, redis_key

def is_valid_guid(guid):
    return re.search(r'^[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12}$', guid) is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app/<guid>')
def app_(guid):
    if not is_valid_guid(guid):
        abort(400)

    # request ongoing?
    status = redis.get(redis_key('%s.%s' % (guid, 'status')))
    if status is None:
        Popen(['python2', 'wpsc/checker.py', guid]) # results have expired, rebuild

    return render_template('app.html', guid=guid)

@app.route('/check/<guid>')
def check(guid):
    if not is_valid_guid(guid):
        abort(400)

    # request ongoing?
    status = redis.get(redis_key('%s.%s' % (guid, 'status')))
    if status is None:
        abort(500) # this should not happen, unless load average is too high

    # error occured?
    if status == 'error':
        return jsonify(status='error')
    elif status == 'processing':
        return jsonify(status='processing')
    elif status == 'done':
        results = {}
        for key in redis.keys('%s.*' % (redis_key(guid),)):
            if key != '%s.status' % (redis_key(guid),):
                results[key] = redis.hgetall(key)

        return jsonify(status='done', results=render_template('table.html', results=results))

    abort(500) # is this even possible?