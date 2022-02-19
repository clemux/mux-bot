import os
from collections import defaultdict
from datetime import datetime

import requests

API_TOKEN = os.getenv('MUX_CTS_API_TOKEN')
BASE_URL = 'https://api.cts-strasbourg.eu/v1/siri/2.0/'


def get_stops(latitude, longitude):
    r = requests.request(
        url=(
            BASE_URL + f'stoppoints-discovery?latitude={latitude}'
            + f'&longitude={longitude}'
            + '&distance=500'),
        auth=(API_TOKEN, ''),
        method='GET',
    )
    stop_points = r.json()['StopPointsDelivery']['AnnotatedStopPointRef']
    stops = defaultdict(list)
    for stop_point in stop_points:
        stops[stop_point['StopName']].append(stop_point['StopPointRef'])
    return stops


def get_arrivals(stop_refs):
    stops_string = '&'.join([
        f'MonitoringRef={stop_ref}' for stop_ref in stop_refs
    ])
    r = requests.request(
        url=BASE_URL + 'stop-monitoring?' + stops_string + '&VehicleMode=tram&MaximumStopVisits=1',
        method='GET',
        auth=(API_TOKEN, '')
    )
    monitoring_deliveries = r.json()['ServiceDelivery']['StopMonitoringDelivery']
    visits = []
    for d in monitoring_deliveries:
        visits.append(d['MonitoredStopVisit'])
    journeys = []
    for v in visits:
        for mjv in v:
            journeys.append(mjv['MonitoredVehicleJourney'])
    arrivals = []
    for j in journeys:
        datetime_string = j['MonitoredCall']['ExpectedArrivalTime']
        stop = j['MonitoredCall']['StopPointName']
        eta = datetime.fromtimestamp(
            datetime.fromisoformat(datetime_string).timestamp() - datetime.now().timestamp()
        ).strftime('%M:%S')
        arrival = {
            'stop': stop,
            'line': j['LineRef'],
            'destination': j['DestinationName'],
            'time': eta,
        }
        arrivals.append(arrival)

    return arrivals


def main():
    stops = get_stops(latitude=48.580511513290396, longitude=7.762197047635817)
    refs = []
    for stop, line_ref in stops.items():
        refs.extend(line_ref)
    arrivals = get_arrivals(refs)
    for arrival in arrivals:
        print(f"{arrival['stop']}: {arrival['line']} - {arrival['destination']} - {arrival['time']}")


if __name__ == '__main__':
    main()