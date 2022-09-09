from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EKS
from diagrams.aws.network import APIGateway
from diagrams.custom import Custom
from diagrams.gcp.analytics import Bigquery

with Diagram('AWS to GCP diagram', show=False, direction='RL'):

    apis = [
        APIGateway('Experian API'),
        APIGateway('Folkeregister API'),
        APIGateway('Proff API')
    ]

    with Cluster('AWS'):
        eks = EKS('EKS')
        notify_edge = Edge(label='notify')
        eks << notify_edge << apis

    with Cluster('GCP'):
        bigquery = Bigquery('Info dump')
        data_studio = Custom('', 'img/google_data_studio.png')

        eks >> Edge(xlabel='update') >> bigquery
        bigquery >> Edge(label='analyze') >> data_studio
