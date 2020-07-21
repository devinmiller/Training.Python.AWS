import argparse
import boto3
from service_base import Resource

class EC2(Resource):
    def __init__(self, root_parser):
        resource_parser = root_parser.add_parser('ec2', help='Manage EC2 instances')
        command_parser = resource_parser.add_subparsers(description='EC2 Commands', dest='func')

        self._build_create_command(command_parser)
        self._build_start_command(command_parser)
        self._build_stop_command(command_parser)
        self._build_terminate_command(command_parser)
        self._build_list_command(command_parser)

        super().__init__('ec2')      

    def _build_create_command(self, parser):
        cmd_create = parser.add_parser('create', help='Create a new EC2 instance')

        cmd_create.add_argument('name', help='The name of the EC2 instance.')
        cmd_create.add_argument('--ami', default='ami-0e34e7b9ca0ace12d', help='The ID of the AMI.')
        cmd_create.add_argument('--type', default='t2.micro', help='The instance type.')
        cmd_create.add_argument('--max', default=1, help='The maximum number of instances to launch.')
        cmd_create.add_argument('--min', default=1, help='The minimum number of instances to launch.')
        cmd_create.add_argument('--tags', default=[], nargs='+', help='The tags to apply to the resources during launch')

    def _build_start_command(self, parser):
        cmd_start = parser.add_parser('start', help='Start a previously stopped instance')
        cmd_start.add_argument('--ids', nargs='+', help='The IDs of the instances.')
        cmd_start.add_argument('--name', help='The name of the instance.')

    def _build_stop_command(self, parser):
        cmd_stop = parser.add_parser('stop', help='Stop a previously started instance')
        cmd_stop.add_argument('--ids', nargs='+', help='The IDs of the instances.')
        cmd_stop.add_argument('--name', help='The name of the instance.')

    def _build_terminate_command(self, parser):
        cmd_terminate = parser.add_parser('terminate', help='Destroy an existing EC2 instance')
        cmd_terminate.add_argument('--ids', nargs='+', help='The IDs of the instances.')
        cmd_terminate.add_argument('--name', help='The name of the instance.')

    def _build_list_command(self, parser):
        cmd_list = parser.add_parser('list', help='List EC2 instances')
        cmd_list.add_argument('--limit', type=int , help='The maximum number of results to return.')    

    def can_parse(self, command):
        return 'ec2' == command.lower()

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_instances
    def create(self, args):
        tags = dict(tags.split('=') for tags in args.tags)
        tags['Name'] = args.name
        
        create_params = {
            'ImageId': args.ami,
            'InstanceType': args.type,
            'MaxCount': args.max,
            'MinCount': args.min,
            'TagSpecifications': [
                {
                    'ResourceType': 'instance',
                    'Tags': [{'Key': key, 'Value': val} for (key, val) in tags.items()]
                }
            ]
        }

        instances = self.resource.create_instances(**create_params)

        for i in instances:
            i.wait_until_exists()

        self._list_details(instances)

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/collections.html
    def list(self, args):
        print('Listing EC2 instances...')

        if args.limit:
            instances = list(self.resource.instances.limit(args.limit))
        else:
            instances = list(self.resource.instances.all())
        
        self._list_details(instances)

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.start
    def start(self, args):
        print('Starting EC2 instances...')

        filters = []

        if args.ids:
            filters.append({
                'Name': 'instance-id',
                'Values': args.ids
            })

        if args.name:
            filters.append({
                'Name': 'tag:Name',
                'Values': [args.name]
            })

        instances = self.resource.instances.filter(Filters=filters)

        self._list_details(instances)

        for i in instances:
            i.stop()

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.stop
    def stop(self, args):
        print('Stopping EC2 instances...')

        filters = []

        if args.ids:
            filters.append({
                'Name': 'instance-id',
                'Values': args.ids
            })

        if args.name:
            filters.append({
                'Name': 'tag:Name',
                'Values': [args.name]
            })

        instances = self.resource.instances.filter(Filters=filters)

        self._list_details(instances)

        for i in instances:
            i.stop()

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.terminate
    def terminate(self, args):
        print('Terminating EC2 instances...')

        filters = []

        if args.ids:
            filters.append({
                'Name': 'instance-id',
                'Values': args.ids
            })

        if args.name:
            filters.append({
                'Name': 'tag:Name',
                'Values': [args.name]
            })

        instances = self.resource.instances.filter(Filters=filters)

        self._list_details(instances)

        for i in instances:
            i.terminate()

    def _list_details(self, instances):
        print(''.join((
            'Id'.ljust(25),
            'Type'.ljust(25),
            'Status'.ljust(25),
            'Tags'
        )))

        for i in instances:
            print(''.join((
                str(i.instance_id).ljust(25),
                str(i.instance_type).ljust(25),
                str(i.state['Name']).ljust(25),
                ', '.join([f'{t["Key"]}={t["Value"]}' for t in i.tags])
            )))