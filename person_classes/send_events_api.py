import requests
import socket
from requests import session
import urllib.request
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, Date, DateTime, Text)

from sqlalchemy.orm import sessionmaker
import json
Base = declarative_base()

CONNECTION_STRING = 'sqlite:///test.db'


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(CONNECTION_STRING)


def create_table(engine):
    Base.metadata.create_all(engine)


global internet
global track_ids
global send_event_func
global request_api_keys
global Session

track_ids = []


class EVENTS(Base):
    __tablename__ = "EVENTS"
    EVENT_ID = Column(Integer, primary_key=True)
    PC_ID = Column('PC_ID', Text())
    EVENT_DATE = Column('EVENT_DATE', Date())
    EVENT_TIME = Column('EVENT_TIME', DateTime())
    PERSON_ID = Column('PERSON_ID', Text())
    PRESENCE = Column('PRESENCE', Text())
    DISTRACTION = Column('DISTRACTION', Text())
    EMOTION = Column('EMOTION', Text())

MAIN_API_URL = "http://20.216.38.173:7031"


def request_api_keys():
    with open('config_parameters.json') as json_file:
        data = json.load(json_file)

    return data['AuthKeys']['apiKey'], data['AuthKeys']['apiSecret']


def send_event_func(latest_event, apiKey, apiSecret):
    event_obj = {
        "pcId": latest_event.PC_ID or "PC1",
        "eventDate": str(latest_event.EVENT_DATE),
        "eventTime": str(latest_event.EVENT_TIME),
        "personId": latest_event.PERSON_ID,
        "presence": int(latest_event.PRESENCE),
        "distraction": int(latest_event.DISTRACTION),
        "emotion": str(latest_event.EMOTION)
    }
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
        'x-auth-api-key': apiKey,
        'x-auth-api-secret': apiSecret
    }
    try:
        response = requests.post('http://20.216.38.173:7031/events', headers=headers, json=event_obj)
        print(event_obj)
        return response
    except:
        pass

# def internet(host="8.8.8.8", port=53, timeout=3):
#     """
#     Host: 8.8.8.8 (google-public-dns-a.google.com)
#     OpenPort: 53/tcp
#     Service: domain (DNS/TCP)
#     """
#     try:
#         socket.setdefaulttimeout(timeout)
#         socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
#         return True
#     except socket.error as ex:
#         return False

def internet(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

def send_event_main():
    engine = db_connect()
    create_table(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    latest_event = session.query(EVENTS).order_by(
        EVENTS.EVENT_ID.desc()).first()

    if internet():
        print("Internet is working")
        apiKey, apiSecret = request_api_keys()
        print("IDs in track_ids ", len(track_ids))
        if len(track_ids) > 0:
            for index, id in enumerate(track_ids):
                latest_event = session.query(
                    EVENTS).filter_by(EVENT_ID=id).first()
                print("latest_event.EVENT_ID ", latest_event.EVENT_ID)
                send_event_func(latest_event, apiKey, apiSecret)
                del track_ids[index]

        # print("latest_event.EVENT_ID ", latest_event.EVENT_ID)

        response = send_event_func(latest_event, apiKey, apiSecret)
        print(response.text)
        session.close()
        if response.status_code >= 200 and response.status_code < 300:
            return {"msg": "Successfully Sent", "isSent": True}
        else:
            return {"msg": "Failed to Send", "isSent": False}
    else:
        print("Internet is not working")
        track_ids.append(latest_event.EVENT_ID)
        print(f"Tracking IDS {track_ids}")
        session.close()
        return {"msg": "Failed to Send, Internet not connected will try later", "isSent": False}
