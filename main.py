import csv
from datetime import datetime

ESTIMATED_JOURNEY_DURATION = {
    'Hammersmith (District, Piccadilly lines)': {
        'Hatton Cross': 27,
        'Barons Court': 1,
        'West Kensington': 3
    }
}
MINIMUM_DELAY_REFUND = 15


# CSV Keys
KEY_DATE = "Date"
KEY_START_TIME = "Start Time"
KEY_END_TIME = "End Time"
KEY_JOURNEY = "Journey/Action"

# TODO:
# - handle the no touch-out case

def parse_date(string_day, string_time):
    return datetime.strptime("{} {}".format(string_day, string_time), '%d-%b-%Y %H:%M')

def is_delayed_journey(station_a, station_b, duration_dt):
    is_delayed = False
    effective_duration_minutes = duration_dt.seconds / 60
    theoric_duration = None
    if station_a in ESTIMATED_JOURNEY_DURATION:
        tmp = ESTIMATED_JOURNEY_DURATION[station_a]
        if station_b in tmp:
            theoric_duration = tmp[station_b]
    if not theoric_duration:
        if station_b in ESTIMATED_JOURNEY_DURATION:
            tmp = ESTIMATED_JOURNEY_DURATION[station_b]
            if station_a in tmp:
                theoric_duration = tmp[station_a]            
    if not theoric_duration:
        print("Could not find theoric duration from {} to {}".format(station_a, station_b))
    else:
        # print("Estimated duration: {}".format(theoric_duration))
        delay = effective_duration_minutes - theoric_duration
        is_delayed = delay >= MINIMUM_DELAY_REFUND 
        if is_delayed:
            print("DELAY! Estimated: {}, effective: {}. Delay {} minutes".format(theoric_duration, effective_duration_minutes, delay))
    return is_delayed
    

def is_tube_journey(str_journey):
    BUS_STRING_PATTERN = "Bus journey, route "
    REFUND_PATTERN = "Oyster helpline refund"
    SEASON_TICKET_BOUGHT_PATTERN = "Season ticket bought, "
    TOP_UP_PATTERN = "Topped up, "
    EXIT_SAME_STATION = "Entered and exited "
    return not str_journey.startswith((BUS_STRING_PATTERN, REFUND_PATTERN, SEASON_TICKET_BOUGHT_PATTERN, TOP_UP_PATTERN,
                                       EXIT_SAME_STATION))


def extract_departure_arrival(journey_str):
    JOURNEY_SEPARATOR = " to "
    departure_station, arrival_station = journey_str.split(JOURNEY_SEPARATOR)
    return departure_station, arrival_station


def parse_csv(filename):
    with open(filename) as csvfile:
        next(csvfile)
        csvfile
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            if is_tube_journey(row[KEY_JOURNEY]):
                end_time_str = row[KEY_END_TIME]
                departure_station, arrival_station = extract_departure_arrival(row[KEY_JOURNEY])
                if end_time_str and arrival_station != ' [No touch-out]':
                    start_date = row[KEY_DATE]
                    start_dt = parse_date(start_date, row[KEY_START_TIME])
                    end_dt = parse_date(start_date, end_time_str)
                    if end_dt < start_dt:
                        # case arrival on the next day
                        print("TODO handle the case")
                    duration = end_dt - start_dt

                    if is_delayed_journey(departure_station, arrival_station, duration):
                        # print("Delayed!")
                        pass
                    else:
                        # print("OK")
                        pass
                else:
                    print("New case to be handled for the journey\n{}\n\n".format(row))
            

if __name__ == '__main__':
    FILENAME = "test-data/input.csv"
    parse_csv(FILENAME)
