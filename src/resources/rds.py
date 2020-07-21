import argparse
import boto3
from service_base import Client

class RDS(Client):
    def __init__(self, root_parser):
        resource_parser = root_parser.add_parser('rds', help='Manage RDS instances')
        command_parser = resource_parser.add_subparsers(description='RDS Commands', dest='func')

        self._build_list_command(command_parser)
        self._build_create_command(command_parser)

        super().__init__('rds') 

    def can_parse(self, command):
        return 'rds' == command.lower()

    def _build_create_command(self, parser):
        cmd_create = parser.add_parser('create', help='Create RDS instance')
        cmd_create.add_argument('engine', help='The name of the database engine to be used')
        cmd_create.add_argument('--username', required=True, help='The name for the master user')
        cmd_create.add_argument('--password', required=True, help='The password for the master user')
        cmd_create.add_argument('--dbname', help='The name of the database created with the instance')
        cmd_create.add_argument('--instance_id', required=True, help='The DB instance identifier')
        cmd_create.add_argument('--instance_class', default='db.t3.small', help='The DB instance class')
        cmd_create.add_argument('--multi_az', default=False, help='Indicates the DB instance is Multi-AZ')
        cmd_create.add_argument('--backup_days', default=0, help='The number of days automated backups are retained')
        cmd_create.add_argument('--storage', default=20, help='Storage (in gibibytes) to allocate for the DB instance')
        cmd_create.add_argument('--tags', default=[], nargs='+', help='The tags to apply to the resources during launch')


    def _build_list_command(self, parser):
        cmd_list = parser.add_parser('list', help='List RDS instances')

    def list(self, args):
        response = self.client.describe_db_instances()
        instances = response['DBInstances']

        self._list_details(instances)

    def create(self, args):
        print('Creating DB instance...')

        tags = dict(tags.split('=') for tags in args.tags)
        
        create_params = {
            'DBName': args.dbname,
            'DBInstanceIdentifier': args.instance_id,
            'AllocatedStorage': args.storage,
            'DBInstanceClass': args.instance_class,
            'Engine': args.engine,
            'MasterUsername': args.username,
            'MasterUserPassword': args.password,
            'BackupRetentionPeriod': args.backup_days,
            'MultiAZ': args.multi_az,
            'Tags': [{'Key': key, 'Value': val} for (key, val) in tags.items()]
        }

        instance = self.client.create_db_instance(**create_params)

        print(instance)

    def _list_details(self, instances):
        print(''.join((
            'Id'.ljust(25),
            'Class'.ljust(25),
            'Engine'.ljust(25),
            'Storage'
        )))

        for i in instances:
            print(''.join((
                str(i['DBInstanceIdentifier']).ljust(25),
                str(i['DBInstanceClass']).ljust(25),
                str(i['Engine']).ljust(25),
                str(i['AllocatedStorage'])
            )))