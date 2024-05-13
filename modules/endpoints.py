import socket
import requests
import uuid
from datetime import datetime, timedelta
from babel.dates import format_date, format_datetime, format_time
from babel.core import Locale
from flask import Flask, request, jsonify
from waitress import serve

from modules.database import db_query
from modules.configuration import dashboard_config, user_config, automation_config
from modules.structs import task,WeatherData


app = Flask(__name__)


# Create a German locale
german_locale = Locale('de', 'DE')


# Helper Functions
def get_local_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a remote server (doesn't matter which one)
        s.connect(("8.8.8.8", 5000))
        # Get the local IP address
        local_ip = s.getsockname()[0]
        # Close the socket
        s.close()
        return local_ip
    except Exception as e:
        print(f"An error occurred while retrieving local IP: {e}")
        return None

def get_mac_address():
    mac_num = uuid.getnode()
    mac_hex = '{:012x}'.format(mac_num)
    mac_address = ':'.join(mac_hex[i:i+2] for i in range(0, 12, 2))

    return mac_address

def run_flask_app():
    local_ip = get_local_ip()
    dashboard_config.mac_address = get_mac_address()
    print(local_ip)
    print(dashboard_config.mac_address)
    serve(app, host=local_ip, port=5000)

def replace_valid_data(data, config):
    try:
        # Get the intersection of keys between data and config
        common_keys = set(data.keys()) & set(config.data.keys())

        for key in common_keys:
            config.data[key] = data[key]
            # Update the value in the config dictionary with the value from data
            # if data[key] is not None:
            #     config.data[key] = data[key]

        config.save_to_file()

    except (ValueError, TypeError) as e:
        print(f"Error: {str(e)}")
        return False, None


# Config Endpoints
@app.route('/get_dashboard_config')
def get_dashboard_config():
    return jsonify(dashboard_config.data)

@app.route('/update_dashboard_config', methods=['POST'])
def update_dashboard_config():
    data = request.get_json()
    replace_valid_data(data, dashboard_config)
    data["waterlevel"] = dashboard_config.waterlevel
    return jsonify({'message': 'Success'})

@app.route('/get_user_config')
def get_user_config():
    return jsonify(user_config.data)

@app.route('/update_user_config', methods=['POST'])
def update_user_config():
    data = request.get_json()
    #new location/data needs to be saved to user_config first
    #since weatherdata requests the new location from user_config
    replace_valid_data(data, user_config)

    #updates dashboardconfig weatherdata outside of default_process
    #when updating user_config lat and lon
    weatherData = WeatherData()
    dashboard_config.current = weatherData.projected_ppt
    dashboard_config.forecast = weatherData.forecast

    return jsonify({'message': 'Success'})

@app.route('/get_automation_config')
def get_automation_config():
    return jsonify(automation_config.data)

@app.route('/update_automation_config', methods=['POST'])
def update_automation_config():
    data = request.get_json()
    replace_valid_data(data, automation_config)
    return jsonify({'message': 'Success'})


# Update OneSignal Player ID
@app.route('/update_player_ids', methods=['POST'])
def update_player_ids():
    data = request.get_json()
    player_id = data["playerID"]

    if player_id not in user_config.player_ids or player_id != "undefined" or player_id != "null":
        user_config.player_ids.append(player_id)
        user_config.save_to_file()
        return jsonify({'message': 'Success'}), 200
    else:
        return jsonify({"message": "String value is already in the singleton array."}), 400


# Send Push Notification
def send_push_notifications(message):

    app_id = '6013af88-5564-4a94-afb1-d364cb366f21'
    api_key = 'NjkyNzFlNzEtYjY5NC00MTMyLTk5YzAtMDc2YWNiZmI4MmQ2'

    url = "https://onesignal.com/api/v1/notifications"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {api_key}'
    }

    data = {
        'app_id': app_id,
        'contents': {'en': message},
        # You can add additional fields to customize the notification further
    }
    
    data['include_player_ids'] = user_config.player_ids

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print("Failed to send notification:", response.status_code, response.json())


#Database Endpoints
@app.route('/get_daily_data')
def get_daily_data():
    column_name = request.args.get('column')
    current_time = datetime.now()
    data = []
    for i in range(23, -1, -1):
        start_time = current_time - timedelta(hours=i)
        end_time = current_time - timedelta(hours=i-1)
        query = "SELECT AVG({}) AS average FROM measurements WHERE date >= '{}' AND date < '{}'".format(column_name, start_time, end_time)
        result = db_query(query)
        average = result[0][0] if result[0][0] is not None else 0
        data.append({'label': start_time.strftime('%H'), 'average': average})
    
    return jsonify(data), 200

@app.route('/get_weekly_data')
def get_weekly_data():
    column_name = request.args.get('column')
    today = datetime.now().date()
    week_start = today - timedelta(days=6)
    
    data = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        query = "SELECT AVG({}) AS average FROM measurements WHERE date >= '{}' AND date < '{}'".format(column_name, day, day + timedelta(days=1))
        result = db_query(query)
        average = result[0][0] if result[0][0] is not None else 0
        german_abbreviated_day_name = format_date(day, format='E', locale=german_locale)
        data.append({'label': german_abbreviated_day_name[:2], 'average': average})
    
    return jsonify(data), 200

@app.route('/get_monthly_data')
def get_monthly_data():
    column_name = request.args.get('column')
    today = datetime.now().date()
    month_start = today - timedelta(days=29)
    
    data = []
    for i in range(30):
        day = month_start + timedelta(days=i)
        query = "SELECT AVG({}) AS average FROM measurements WHERE date >= '{}' AND date < '{}'".format(column_name, day, day + timedelta(days=1))
        result = db_query(query)
        average = result[0][0] if result[0][0] is not None else 0
        day_with_month = f'{day.day}.{day.month}'
        data.append({'label': day_with_month, 'average': average})
    
    return jsonify(data), 200

@app.route('/get_yearly_data')
def get_yearly_data():
    column_name = request.args.get('column')
    today = datetime.now().date()
    data = []
    for i in range(11, -1, -1):
        # Calculate the month and year for each iteration
        month = today.month - i
        year = today.year
        if month <= 0:
            month += 12
            year -= 1
        
        # Calculate the start and end dates for the month
        month_start = datetime(year, month, 1)
        month_end = month_start.replace(day=1, month=month_start.month + 1) if month_start.month < 12 else month_start.replace(year=month_start.year + 1, month=1, day=1)
        
        # Perform the query to retrieve the average for the month
        query = "SELECT AVG({}) AS average FROM measurements WHERE date >= '{}' AND date < '{}'".format(column_name, month_start, month_end)
        result = db_query(query)
        average = result[0][0] if result[0][0] is not None else 0
        # Append the month and average to the data list
        #english_month = month_start.strftime('%B')
        german_month = format_date(month_start, format='MMMM', locale=german_locale)
        data.append({'label': german_month, 'average': average})
    
    return jsonify(data), 200

@app.route('/get_current_data')
def get_current_data():
    data = {
        "messungsZeit": dashboard_config.current_time,
        "lat": user_config.latitude,
        "lon": user_config.longitude,
        "dachflaeche": user_config.calculate_total_surface_area(),
        "gemessen": dashboard_config.waterlevel,
    }

    return data, 200


# Endpoint to trigger threshold_drain
@app.route('/threshold_drain/<threshold_value>')
def trigger_threshold_drain(threshold_value):
    task.set_task("threshold_drain",float(threshold_value))
    dashboard_config.drain_threshold = float(threshold_value)
    return jsonify(message="Threshold drain triggered"), 200


# Endpoint to stop threshold_drain
@app.route('/stop_drain')
def stop_drain():
    print("stopping drain from controller")
    task.set_task("default",None)
    task.set_drain_stopped(True)
    dashboard_config.is_draining = False
    return jsonify(message="Drain stopped"), 200

# Endpoint to get the current Status of the Service
@app.route('/get_service_status')
def get_service_status():
    service_status = "Service is running"
    response = {
        "status": "success",
        "message": service_status
    }
    return jsonify(response), 200

# Add CORS Headers to Response
@app.after_request
def add_cors_header(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response