import argparse
import boto3

ec2 = boto3.resource('ec2', region_name='us-west-2')

def configure_arguments(resource_parser):
    parser = resource_parser.add_parser('subnet', help='Manage Subnet instances')

    subparser = parser.add_subparsers(description='Subnet Commands', dest='subnet')

    list_parser = subparser.add_parser('list', help='List Subnet instances')
    list_parser.add_argument('--limit', type=int , help='The maximum number of results to return.')

def parse_arguments(args):
    command_map = {
        'list': list_instances,
    }

    func = command_map[args.subnet]
    func(args)

def list_instances(args):
    print('Listing Subnet instances...')

    _list_details(ec2.subnets.all())

def _list_details(instances):
    print(''.join((
        'Id'.ljust(25),
        'VPC'.ljust(25),
        'CIDR'.ljust(25),
        'Default'.ljust(25),
        'Zone'.ljust(25),
        'Tags'
    )))

    for i in instances:
        tags = i.tags if i.tags else []
        print(''.join((
            str(i.subnet_id).ljust(25),
            str(i.vpc_id).ljust(25),
            str(i.cidr_block).ljust(25),
            str(i.default_for_az).ljust(25),
            str(i.availability_zone).ljust(25),
            ', '.join([f'{t["Key"]}={t["Value"]}' for t in tags])
        )))