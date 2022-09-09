from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.aws.compute import LambdaFunction
from diagrams.onprem.database import Mongodb

with Diagram('Onprem to AWS diagram', show=False):

    timer_trigger = Custom('Timer trigger', 'img/timer.png')

    with Cluster('On-prem'):
        db = Mongodb('MongoDB')

    with Cluster('Google Suite'):
        drive = Custom('Drive', 'img/google_drive.png')
        spreadsheet = Custom('Spreadsheet', 'img/spreadsheet.png')

    with Cluster('AWS'):
        lambda_function_fetcher = LambdaFunction('Fetcher')
        db << Edge(label='read') << lambda_function_fetcher
        lambda_function_fetcher >> Edge(label='write') >> spreadsheet
        timer_trigger >> Edge(label='every 2 hours') >> lambda_function_fetcher

        lambda_function_enricher = LambdaFunction('Enricher')
        lambda_function_enricher << Edge(xlabel='process') << spreadsheet
        lambda_function_enricher >> Edge(label='save') >> drive
        timer_trigger >> Edge(label='every 24 hours') >> lambda_function_enricher
