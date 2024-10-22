import time
from asyncio.staggered import staggered_race
from confluent_kafka import Consumer, KafkaError
import numpy as np
import pandas as pd
import  psycopg2
from pyspark.examples.src.main.python.als import update
from streamlit_autorefresh import st_autorefresh

import streamlit as st
from kafka import KafkaConsumer
import simplejson as json
import matplotlib.pyplot as plt
from voting import consumer


def fetch_voting_stats():
    conn = psycopg2.connect("host=localhost dbname=voting user=postgres password=postgres")
    cur = conn.cursor()

    #fetch total number of voters
    cur.execute("""
    SELECT COUNT(*) as voters_count FROM voters;
    """)
    voter_count = cur.fetchone()[0]
    #fetch total number of voters
    cur.execute("""
    SELECT COUNT(*) as candidates_count FROM candidates;
    """)
    candidate_count = cur.fetchone()[0]
    return voter_count, candidate_count

def plot_colered_bar_chart(results):
    data_type = results['candidate_name']

    colors = plt.cm.viridis(np.linspace(0,1,len(data_type)))
    plt.bar(data_type,results['total_votes'],color=colors)
    plt.xlabel("Candidate")
    plt.ylabel("Total votes")
    plt.title("Vote Counts per Candidate")
    plt.xticks(rotation=90)
    return plt

def plot_donut_chart(data):
    labels = list(data['candidate_name'])
    sizes = list(data['total_votes'])

    fig, ax = plt.subplots()
    ax.pie(sizes,labels=labels, autopct='%1.1f%%',startangle=140)
    ax.axis('equal')
    plt.title("Candidate Votes")
    return fig
@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i: i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

def paginate_table(table_data):
    top_menu = st.columns(3)
    with top_menu[0]:
        sort = st.radio("Sort Data", options=["Yes", "No"], horizontal=1, index=1)
    if sort == "Yes":
        with top_menu[1]:
            sort_field = st.selectbox("Sort By", options=table_data.columns)
        with top_menu[2]:
            sort_direction = st.radio(
                "Direction", options=["⬆️", "⬇️"], horizontal=True
            )
        table_data = table_data.sort_values(
            by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
        )
    pagination = st.container()

    bottom_menu = st.columns((4, 1, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[10, 25, 50, 100])
    with bottom_menu[1]:
        total_pages = (
            int(len(table_data) / batch_size) if int(len(table_data) / batch_size) > 0 else 1
        )
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1
        )
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")

    pages = split_frame(table_data, batch_size)
    pagination.dataframe(data=pages[current_page - 1], use_container_width=True)
def sidebar():
    if st.session_state.get('latest_update') is None:
        st.session_state['last_update'] = time.time()
    refresh_interval = st.sidebar.slider("Refresh interval (seconds)",5,60,10)
    st_autorefresh(interval=refresh_interval * 1000, key='auto')

    if st.sidebar.button('Refresh Data'):
        update_data()

def update_data(topic):

    last_refresh = st.empty()
    last_refresh.text(f"Last refresh at: {time.strftime('%y -%m - %d %h:%m:%s')}")


    voter_count, candidate_count = fetch_voting_stats()
    st.markdown("""---""")
    col1,col2 = st.columns(2)
    col1.metric("Total voters",voter_count)
    col2.metric("Candidate count",candidate_count)

    consumer = create_kafka_consumer(topic)
    data = fetch_data_from_kafka(consumer)

    results = pd.DataFrame(data)

    results =  results.loc[results.groupby('candidate_id')['total_votes'].idxmax()]
    leading_candidate = results.loc[results['total_votes'].idxmax()]

    #Display the leading candidate information
    st.markdown("""---""")
    st.header("Leading Candidate")
    col1,col2 = st.columns(2)
    with col1:
        st.image(leading_candidate['photo_url'],width=200)
    with col2:
        st.header(leading_candidate['candidate_name'])
        st.subheader(leading_candidate['party_affiliation'])
        st.subheader('Total votes : {}'.format(leading_candidate['total_votes']))
    #display the statistics and visualiastions
    st.markdown("""---""")
    st.header('Voting statistics')
    results = results[['candidate_id', 'candidate_name', 'party_affiliation', 'total_votes']]
    results = results.reset_index(drop=True)

    col1,col2 = st.columns(2)
    with col1:
        bar_fig = plot_colered_bar_chart(results)
        st.pyplot(bar_fig)
    with col2:
        donut_fig = plot_donut_chart(results)
        st.pyplot(donut_fig)

    st.table(results)

    #fetch data from kafka turn out location
    location_consumer = create_kafka_consumer('aggregated_turnout_by_location')
    location_data = fetch_data_from_kafka(location_consumer)
    location_results = pd.DataFrame(location_data)

    #max location
    location_results =  location_results.loc[location_results.groupby('state')['count'].idxmax()]
    location_results = location_results.reset_index(drop=True)

    st.header("Location of voters")
    paginate_table(location_results)

    st.session_state['last_update'] = time.time()







def create_kafka_consumer(topic_name):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers = 'localhost:9092',
        auto_offset_reset = 'earliest',
        value_deserializer = lambda x: json.loads(x.decode('utf-8'))

    )
    return consumer

def fetch_data_from_kafka(consumer):
    msg = consumer.poll(timeout_ms = 1000)
    data = []
    for message in msg.values():
        for sub_message in message:
            data.append(sub_message.value)
    return data

# st.title("Realtime Voting Project")
# topic_name = "aggregated_votes_per_candidate"
# sidebar()
# update_data(topic_name)

def test_fetch_data_kafka_topic():
    results = []
    conf = {
        'bootstrap.servers': 'localhost:9092'
    }
    consumer = Consumer(conf | {
    'group.id': 'voting-group',
    'auto.offset.reset' : 'earliest',
    'enable.auto.commit': False
    })
    consumer.subscribe(['aggregated_votes_per_candidate'])
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        elif msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        else:
            data = json.loads(msg.value().decode('utf-8'))
            print('>>kiem tra',data)
            # results.append(data)




test_fetch_data_kafka_topic()




