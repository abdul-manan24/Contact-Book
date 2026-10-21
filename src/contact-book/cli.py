import argparse
import repository

def build_parser():


    parser = argparse.ArgumentParser (
        prog='Contact',
        description='Manage your personal contact book.',
    )


    commands = parser.add_subparsers (
        dest='command', required=True
    )


    add = commands.add_parser('add', help='Create a contact.')
    add.add_argument('--name')
    add.add_argument('--phone')
    add.add_argument('--email')
    add.add_argument('--address')
    add.add_argument('--notes')
    add.set_defaults(func=repository.add_contact)


    listing = commands.add_parser('list', help='List contacts.')
    listing.add_argument('--limit', type=int, default=20)
    listing.add_argument('--offset', type=int, default=0)
    listing.set_defaults(func=repository.list_contacts)


    search = commands.add_parser('search', help='Searches contacts.')
    search.add_argument('query')
    search.add_argument('--limit', type=int, default=50)
    search.set_defaults(func=repository.search_contacts)


    show = commands.add_parser('show', help='Shows a contact.')
    show.add_argument('id', type=int)
    show.set_defaults(func=repository.show_command)


    update = commands.add_parser('update', help='Update a contact.')
    update.add_argument('id', type=int)
    for field in ('name', 'phone', 'email', 'address', 'notes'):
        update.add_argument(f'--{field}')
    update.set_defaults(func=repository.update_contact)


    delete = commands.add_parser('delete', help='Delete a contact.')
    delete.add_argument('--id', type=int)
    delete.add_argument(
        '--yes', action='store_true',
        help='Skip deletion confirmation'
    )
    delete.set_defaults(func=repository.delete_contact)


    count = commands.add_parser('count', help='Count contacts')
    count.set_defaults(func=repository.count_contacts)
    

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    args.func(args)

main()