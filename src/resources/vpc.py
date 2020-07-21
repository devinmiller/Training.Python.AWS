import argparse
import boto3
from service_base import Resource

class VPC(Resource):
    def __init__(self, root_parser):
        resource_parser = root_parser.add_parser('vpc', help='Manage VPC instances')
        command_parser = resource_parser.add_subparsers(description='VPC Commands', dest='func')

        self._build_list_command(command_parser)

        super().__init__('ec2') 

    def _build_list_command(self, parser):
        cmd_list = parser.add_parser('list', help='List VPC instances')
        cmd_list.add_argument('--limit', type=int , help='The maximum number of results to return.')

    def can_parse(self, command):
        return 'vpc' == command.lower()

    def list(self, args):
        print('Listing VPC instances...')

        self._list_details(self.resource.vpcs.all())

    def _list_details(self, instances):
        print(''.join((
            'Id'.ljust(25),
            'State'.ljust(25),
            'Default'.ljust(25),
            'Tags'
        )))

        for i in instances:
            tags = i.tags if i.tags else []
            print(''.join((
                str(i.vpc_id).ljust(25),
                str(i.state).ljust(25),
                str(i.is_default).ljust(25),
                ', '.join([f'{t["Key"]}={t["Value"]}' for t in tags])
            )))