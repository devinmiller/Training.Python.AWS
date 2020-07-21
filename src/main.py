from argparse import ArgumentParser 

import pkgutil
import importlib
import inspect

import resources

if __name__ == '__main__':
    parser = ArgumentParser(description='A CLI for AWS')
    resource_parser = parser.add_subparsers(description='Manage specific AWS resources', dest='command')
    
    modules = pkgutil.iter_modules(resources.__path__, resources.__name__ + '.') 
    imports = [importlib.import_module(module_name) for _, module_name, _ in modules]

    handlers = [
        handler(resource_parser)
        for module in imports 
        for name, handler in inspect.getmembers(module, inspect.isclass) 
        if handler.__module__ == module.__name__
    ]

    args = parser.parse_args() 

    for handler in handlers:
        if handler.can_parse(args.command):
            handler(args)
    