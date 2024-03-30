from app import webserver
from flask import request, jsonify

import os
import json

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")
    # Check if job_id is valid
    # If not, return error
    # {
    # "status": "error",
    # "reason": "Invalid job_id"
    # }   
    if job_id is None or not job_id.isdigit() or int(job_id) < 0 or int(job_id) >= webserver.job_counter:
        return jsonify ({
            "status": "error",
            "reason": "Invalid job_id"
        })

    # Check if job_id is running
    if webserver.data_parser.job_maintainer.is_job_running(int(job_id)):
        return jsonify({'status': 'running'})
    
    # Check if job_id is done and return the result
    #    res = res_for(job_id)
    #    return jsonify({
    #        'status': 'done',
    #        'data': <JSON_PROCESSING_RESULT>
    #    })
    
    # Read result from results/job_id.json
    with open(f"results/{job_id}.json", "r") as fin:
        res = json.load(fin)
    
    return jsonify({
        'status': 'done',
        'data': res
    })

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # Get request data
    data = request.json
    print(f"Got request {data} in states_mean_request")

    # Get current job_id
    job_id = webserver.job_counter

    # Register job. Don't wait for task to finish
    webserver.tasks_runner.__submit__(webserver.data_parser.states_mean, data, job_id)
    
    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    # Get request data
    data = request.json
    print(f"Got request {data} for state_mean")

    # Get current job_id
    job_id = webserver.job_counter

    # Increment job_id counter
    webserver.job_counter += 1

    # Register job. Don't wait for task to finish
    webserver.tasks_runner.__submit__(webserver.data_parser.state_mean, data, job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    # Get request data
    data = request.json
    print(f"Got request {data} for best5")

    # Get current job_id
    job_id = webserver.job_counter

    # Register job. Don't wait for task to finish
    webserver.tasks_runner.__submit__(webserver.data_parser.best5, data, job_id)

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    # Get request data
    data = request.json
    print(f"Got request {data} for worst5")

    # Get current job_id
    job_id = webserver.job_counter

    # Register job. Don't wait for task to finish
    webserver.tasks_runner.__submit__(webserver.data_parser.worst5, data, job_id)

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    # Get request data
    data = request.json
    print(f"Got request {data} for global_mean")

    # Get current job_id
    job_id = webserver.job_counter

    # Register job. Don't wait for task to finish
    webserver.tasks_runner.__submit__(webserver.data_parser.global_mean, data, job_id)

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    # Get request data
    data = request.json
    print(f"Got request {data} for diff_from_mean")

    # Get current job_id
    job_id = webserver.job_counter

    # Register job. Don't wait for task to finish
    webserver.tasks_runner.__submit__(webserver.data_parser.diff_from_mean, data, job_id)

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # Get request data
    data = request.json
    print(f"Got request {data} for state_diff_from_mean")

    # Get current job_id
    job_id = webserver.job_counter
    
    # Register job. Don't wait for task to finish
    webserver.tasks_runner.__submit__(webserver.data_parser.state_diff_from_mean, data, job_id)

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": job_id})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # Get request data
    data = request.json
    print(f"Got request {data} for state_diff_from_mean")

    # Get current job_id
    job_id = webserver.job_counter

    # Register job. Don't wait for task to finish
    webserver.tasks_runner.__submit__(webserver.data_parser.mean_by_category, data, job_id)

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": job_id})

    
@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # Get request data
    data = request.json
    print(f"Got request {data} for state_diff_from_mean")

    # Get current job_id
    job_id = webserver.job_counter

    # Register job. Don't wait for task to finish
    webserver.tasks_runner.__submit__(webserver.data_parser.state_mean_by_category, data, job_id)

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": job_id})


@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    # Register job. Don't wait for task to finish
    webserver.tasks_runner.__shutdown__()

    # Return 200 OK
    return jsonify({"message": "Shutting down gracefully"}), 200


@webserver.route('/api/jobs', methods=['GET'])
def jobs():
    # Respond with a json with all the job ids and their status
    #  {
    #      "status": "done"
    #      "data": [
    #       { "job_id_1": "done"},
    #       { "job_id_2": "running"},
    #       { "job_id_3": "running"}
    #   ]
    #  }
    jobs = []
    for job_id in range(1, webserver.job_counter):
        if webserver.data_parser.job_maintainer.is_job_running(job_id):
            jobs.append({job_id: "running"})
        elif webserver.data_parser.job_maintainer.is_job_done(job_id):
            jobs.append({job_id: "done"})

    return jsonify({"status": "done", "data": jobs})

@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    # Respond with the number of jobs that have been submitted
    return jsonify({"num_jobs": webserver.job_counter - 1})


# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
