from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import ManagedStreamingForKafka
from diagrams.aws.compute import EC2
from diagrams.aws.security import SecretsManager
from diagrams.azure.analytics import Hdinsightclusters
from diagrams.azure.security import KeyVaults
from diagrams.custom import Custom
from diagrams.onprem.queue import Kafka
from diagrams.onprem.security import Vault


def kafka_cluster_interconnections(app, kafka_cluster, secret_store):
    app >> Edge(label='retrieve') >> secret_store
    secret_store - Edge(label='store') - kafka_cluster


with Diagram('Discovery API diagram', show=False):
    auth = Custom('CIAM service', 'img/dnb.png')
    clients = [
        EC2('Client #1'),
        EC2('Client #2'),
        EC2('Client #3'),
    ]
    auth << Edge(label='authenticate') << clients

    api = Custom('Discovery service', 'img/wing.png')
    clients >> api
    with Cluster('AWS'):
        secret_manager = SecretsManager()
        kafka = ManagedStreamingForKafka('MSK')
        kafka_cluster_interconnections(api, kafka, secret_manager)

    with Cluster('Azure'):
        vault = KeyVaults()
        azure_kafka_cluster = Hdinsightclusters('Kafka cluster')
        kafka_cluster_interconnections(api, azure_kafka_cluster, vault)

    with Cluster('On-prem account'):
        kafka_cluster_interconnections(api, Kafka(), Vault())
