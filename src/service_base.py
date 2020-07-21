import boto3

class Resource():
    def __init__(self, service):
        self.session = boto3.Session(region_name='us-west-2')
        self.resource = self.session.resource(service)

    def __call__(self, args):
        try:
            command = getattr(self, args.func)
        except AttributeError:
            print(f'Command {args.func} was not recognized')
        else:
            command(args)

class Client():
    def __init__(self, service):
        self.session = boto3.Session(region_name='us-west-2')
        self.client = self.session.client(service)

    def __call__(self, args):
        try:
            command = getattr(self, args.func)
        except AttributeError:
            print(f'Command {args.func} was not recognized')
        else:
            command(args)