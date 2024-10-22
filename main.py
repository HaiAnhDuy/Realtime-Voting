import json
import random
import psycopg2
import requests
from confluent_kafka import SerializingProducer

BASE_URL = 'https://randomuser.me/api/?nat=gb'
PARTIES = ['Management_Party','Savior Party','Tech Republic Party']

# random.seed(21)
random.seed(21)

def create_tables(conn,cur):
    cur.execute("""
        
        CREATE TABLE IF NOT EXISTS candidates (
        candidate_id  VARCHAR(255) PRIMARY KEY,
        candidate_name VARCHAR(255),
        party_affiliation VARCHAR(255),
        biography TEXT,
        campaign_platform TEXT,
        photo_url TEXT
        ) 
        
    """ )

    cur.execute("""
        
        CREATE TABLE IF NOT EXISTS voters (
        voters_id  VARCHAR(255) PRIMARY KEY,
        voters_name VARCHAR(255),
        date_of_birth DATE,
        gender VARCHAR(255),
        nationality VARCHAR(255),
        registration_number VARCHAR(255),
        address_street VARCHAR(255),
        address_city VARCHAR(255),
        address_state VARCHAR(255),
        address_country VARCHAR(255),
        address_postcode VARCHAR(255),
        email VARCHAR(255),
        phone_number VARCHAR(255),
        picture TEXT,
        registered_age INTEGER
        ) 
        
    """ )
    cur.execute("""
       CREATE TABLE IF NOT EXISTS votes (
         voters_id VARCHAR(255) UNIQUE,
         candidate_id VARCHAR(255),
         voting_time TIMESTAMP,
         vote int DEFAULT 1,
         primary key (voters_id,candidate_id)
       )
    """)

    conn.commit() # lưu thay đổi
def generate_candidate_data(candidate_number, total_parties):
    response = requests.get(BASE_URL + '&gender=' + ('female' if candidate_number %2 == 1 else 'male'))
    if response.status_code == 200:
        user_data = response.json()['results'][0]

        return {
            'candidate_id': user_data['login']['uuid'],
            'candidate_name': f"{user_data['name']['first']} {user_data['name']['last']}",
            'party_affiliation': PARTIES[candidate_number % total_parties],
            'biography': 'A brief biography of the candidate',
            'campaign_platform': "Key campaign promises and or platform",
            'photo_url': user_data['picture']['large']
        }
    else:
        return "ERROR fetching data"
def generate_voter_data():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        user_data = response.json()['results'][0]
        return {
            'voters_id':  user_data['login']['uuid'],
            'voters_name': f"{user_data['name']['first']} {user_data['name']['last']}"  ,
            'date_of_birth': user_data['dob']['date'],
            'gender': user_data['gender'],
            'nationality': user_data['nat'],
            'registration_number': user_data['login']['username'],
            'address': {
                'street': f"{user_data['location']['street']['number']} {user_data['location']['street']['name']}",
                'city': user_data['location']['city'],
                'state': user_data['location']['state'],
                'country':user_data['location']['country'] ,
                'postcode':user_data['location']['postcode']
            },

            'email': user_data['email'],
            'phone_number': user_data['phone'],
            'picture':user_data['picture']['large'],
            'registered_age':user_data['registered']['age']
        }
def insert_voter(conn,cur,voter_data):
    print('check:',voter_data)
    cur.execute("""
       INSERT INTO voters(voters_id,voters_name,date_of_birth,gender,nationality,registration_number,
       address_street , address_city ,address_state,address_country,address_postcode ,email,phone_number,
       picture,registered_age
       )
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,
                (
                voter_data['voters_id'],voter_data['voters_name'],voter_data['date_of_birth'],voter_data['gender'],voter_data['nationality'],
                voter_data['registration_number'],voter_data['address']['street'],voter_data['address']['city'],voter_data['address']['state'],
                voter_data['address']['country'],voter_data['address']['postcode'],voter_data['email'],voter_data['phone_number'],voter_data['picture'],
                voter_data['registered_age']
                )
                )
    conn.commit()

def delivery_report(err,msg):
    if err is not None:
        print(f"Message Delivery Failed: {err}")
    else:
        print(f"essage Delivery to {msg.topic()} [{msg.partition()}]")

if __name__ == "__main__":
    producer = SerializingProducer(
        {
            'bootstrap.servers': 'localhost:9092'

        }
    )
    try:
        conn = psycopg2.connect("host=localhost dbname=voting user=postgres password=postgres") # tạo database,Kết nối đến cơ sở dữ liệu PostgreSQL
        cur = conn.cursor() # tạo một đối tượng cursor để thực hiện truy vấn SQL.

        create_tables(conn,cur) # tạo các bảng nếu chưa tồn tại

        cur.execute("""
           SELECT * FROM candidates
        """)

        candidates = cur.fetchall() # lấy kết quả truy vấn tất cả nhung ứng cử viên

        if (len(candidates) == 0):
            for i in range(3):
                candidate = generate_candidate_data(i ,3)
                cur.execute("""
                    INSERT INTO candidates(candidate_id,candidate_name,party_affiliation,biography,campaign_platform,photo_url)
                    VALUES(%s,%s,%s,%s,%s,%s)
                """,
                            (
                                candidate['candidate_id'],candidate['candidate_name'],candidate['party_affiliation'],candidate['biography'],candidate['campaign_platform'],
                                candidate['photo_url']
                            )
                            )
                conn.commit()

        for i in range(1000):
            voter_data = generate_voter_data()
            insert_voter(conn,cur,voter_data)

            producer.produce(
                "voters_topic",
                key=voter_data['voters_id'],
                value=json.dumps(voter_data),
                on_delivery=delivery_report

            )
            producer.flush()
    except Exception as e:
        print(e)
