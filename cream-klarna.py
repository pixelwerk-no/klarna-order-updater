#!/usr/bin/env python

import argparse
import sys
import klarnacheckout

parser = argparse.ArgumentParser(description='Klarna command line client.')
parser.add_argument('--acknowledge-order', dest='checkout_id', action='store', nargs=1,
                    help='acknowledge order with specified checkout id')

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

checkout_id = args.checkout_id[0]

klarnacheckout.Order.base_uri = 'https://checkout.testdrive.klarna.com/checkout/orders'
klarnacheckout.Order.content_type = 'application/vnd.klarna.checkout.aggregated-order-v2+json'

connector = klarnacheckout.create_connector('shared_secret')
order = klarnacheckout.Order(connector, checkout_id)
order.fetch()

if order['status'] == 'checkout_complete':
    update_data = {'status': 'created'}

    order.update(update_data)
else:
    raise Exception(
        "The checkout order with id %s is not complete. Aborting. Order status will NOT be updated." % checkout_id)
