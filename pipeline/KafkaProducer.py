# coding: utf-8
from time import sleep
from kafka import KafkaProducer
# logging.basicConfig(level=logging.DEBUG)

kafka_topic = 'ERCLabCrawler'


def main():
    with open("../data//kakao.txt", "r", encoding='utf8') as f:
        if f.mode == "r":
            objects = f.readlines()
            i= 0
            for object in objects:
                if i > 0:
                    print("Sending ("+str(i)+") ...")
                    print(object)
                    send_to_consumer(object)
                    sleep(2)
                i = i+1
                # if i == 5:
                #break # this break is for testing a single line object
            print("All Finished...")


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['muzamil-VirtualBox'],
                                  api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer


def send_to_consumer(object) :
    producer = connect_kafka_producer()
    producer.send(kafka_topic, object.encode('utf-8'))
    producer.flush()


if __name__ == "__main__":
    main()

