#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2015: Alignak team, see AUTHORS.txt file for contributors
#
# This file is part of Alignak.
#
# Alignak is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alignak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Alignak.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
from future.utils import iteritems
import json
import ujson
import argparse

from alignak.objects.config import Config
from alignak_backend_client.client import Backend

from alignak_backend.models import command
from alignak_backend.models import timeperiod
from alignak_backend.models import hostgroup
from alignak_backend.models import hostdependency
from alignak_backend.models import servicedependency
from alignak_backend.models import serviceextinfo
from alignak_backend.models import trigger
from alignak_backend.models import contact
from alignak_backend.models import contactgroup
from alignak_backend.models import contactrestrictrole
from alignak_backend.models import escalation
from alignak_backend.models import host
from alignak_backend.models import hostextinfo
from alignak_backend.models import hostescalation
from alignak_backend.models import servicegroup
from alignak_backend.models import service
from alignak_backend.models import serviceescalation

parser = argparse.ArgumentParser()
parser.add_argument("cfg", nargs='*', default=None)
args = parser.parse_args()

# Define here the path of the cfg files
cfg = [] # ['cfg/from_shinken/shinken.cfg']

if args.cfg is not None:
    cfg.extend(args.cfg)

if cfg == []:
    print('No cfg file to parse')

# Define here the url of the backend
backend_url = 'http://localhost:5000/'

# Delete all objects in backend ?
destroy_backend_data = True

username = 'admin'
password = 'admin'

# Don't touch after this line
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def check_mapping(items, mapping):
    response = {
        'all_found': True,
        'data': items
    }
    new_list = []
    for item in items:
        if item in mapping:
            new_list.append(mapping[item])
        else:
            response['all_found'] = False
    if response['all_found']:
        response['data'] = new_list
    return response


# Get flat files configuration
alconfig = Config()
buf = alconfig.read_config(cfg)
conf = alconfig.read_config_buf(buf)


print("~~~~~~~~~~~~~~~~~~~~~~ First authentication to delete previous data ~~~~~~~~~~~~~~~~~~~")
# Backend authentication with token generation
headers = {'Content-Type': 'application/json'}
payload = {'username': username, 'password': password, 'action': 'generate'}
backend = Backend(backend_url)
backend.login(username, password)

if backend.token is None:
    print("Can't authenticated")
    exit()
print("~~~~~~~~~~~~~~~~~~~~~~ Authenticated ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# Destroy data in backend if defined
if destroy_backend_data:
    headers = {'Content-Type': 'application/json'}
    backend.delete('command', headers)
    backend.delete('timeperiod', headers)
    backend.delete('hostgroup', headers)
    backend.delete('hostdependency', headers)
    backend.delete('servicedependency', headers)
    backend.delete('serviceextinfo', headers)
    backend.delete('trigger', headers)
    #backend.delete('contact', headers)
    backend.delete('contactgroup', headers)
    backend.delete('contactrestrictrole', headers)
    backend.delete('escalation', headers)
    backend.delete('host', headers)
    backend.delete('hostextinfo', headers)
    backend.delete('hostescalation', headers)
    backend.delete('servicegroup', headers)
    backend.delete('service', headers)
    backend.delete('serviceescalation', headers)
    print("~~~~~~~~~~~~~~~~~~~~~~ Data destroyed ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Order of objects + fields to update post add
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# COMMAND
#    command.use
# TIMEPERIOD
#    timeperiod.use
# HOSTGROUP
#    hostgroup.hostgroup_members
# HOSTDEPENDENCY
#    hostdependency.use
# SERVICEDEPENDENCY
#    servicedependency.use
# SERVICEEXTINFO
#    serviceextinfo.use
# TRIGGER
#    trigger.use
# CONTACT
#    contact.use
# CONTACTGROUP
#    contact.contactgroups / contactgroup.contactgroup_members
# CONTACTRESTRICTROLE
#
# ESCALATION
#    escalation.use
# HOST
#    hostgroup.members / host.use / host.parents
# HOSTEXTINFO
#    hostextinfo.use
# HOSTESCALATION
#    hostescalation.use
# SERVICEGROUP
#    servicegroup.servicegroup_members
# SERVICE
#    service.use
# SERVICEESCALATION
#    serviceescalation.use
#


def update_types(source, schema):
    for prop in source:
        source[prop] = ''.join(source[prop])
        if prop in schema:
            # get type
            if schema[prop]['type'] == 'boolean':
                if source[prop] == '1':
                    source[prop] = True
                else:
                    source[prop] = False
            elif schema[prop]['type'] == 'list':
                source[prop] = source[prop].split(',')
            elif schema[prop]['type'] == 'integer':
                source[prop] = int(source[prop])
    return source


def update_later(later, inserted, ressource, field):
    headers = {'Content-Type': 'application/json'}
    for (index, item) in iteritems(later[ressource][field]):
        data = {field: inserted[item['ressource']][item['value']]}
        headers['If-Match'] = item['_etag']
        backend.patch(''.join([ressource, '/', index]), data, headers, True)


def manage_ressource(r_name, inserted, later, data_later, id_name, schema):
    """

    data_later = [{'field': 'use', 'type': 'simple|list', 'ressource': 'command'}]

    :param r_name:
    :param inserted:
    :param later:
    :param data_later:
    :return:
    """
    if r_name not in inserted:
        inserted[r_name] = {}
    if r_name not in later:
        later[r_name] = {}
    for k, values in enumerate(data_later):
        if values['field'] not in later[r_name]:
            later[r_name][values['field']] = {}
    if r_name in conf:
        for item in conf[r_name]:
            later_tmp = {}
            headers = {
                'Content-Type': 'application/json',
            }
            if 'imported_from' in item:
                del item['imported_from']
            for p in item:
                item[p] = item[p][0]
            item = update_types(item, schema['schema'])
            for k, values in enumerate(data_later):
                if values['field'] in item:
                    if values['ressource'] in inserted and values['field'] in inserted[values['ressource']]:
                        item[values['field']] = inserted[values['ressource']][values['field']]
                    else:
                        later_tmp[values['field']] = item[values['field']]
                        del item[values['field']]
            # special case of timeperiod
            if r_name == 'timeperiod':
                fields = ['imported_from', 'use', 'name', 'definition_order', 'register',
                          'timeperiod_name', 'alias', 'dateranges', 'exclude', 'is_active']
                item['dateranges'] = []
                prop_to_del = []
                for prop in item:
                    if prop not in fields:
                        item['dateranges'].append({prop: item[prop]})
                        prop_to_del.append(prop)
                for prop in prop_to_del:
                    del item[prop]
            print(item)
            response = backend.post(r_name, item, headers)
            if '_error' in response and '_issues' in response:
                print("ERROR: %s" % response['_issues'])
            else:
                if id_name in item:
                    inserted[r_name][item[id_name]] = response['_id']
                else:
                    inserted[r_name][item['name']] = response['_id']
                for k, values in enumerate(data_later):
                    if values['field'] in later_tmp:
                        later[r_name][values['field']][response['_id']] = {'type': values['type'],
                                                                           'ressource': values['ressource'],
                                                                           'value': later_tmp[values['field']],
                                                                           '_etag': response['_etag']}

later = {}
inserted = {}

print("~~~~~~~~~~~~~~~~~~~~~~ add commands ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
data_later = [{'field': 'use', 'type': 'simple', 'ressource': 'command'}]
schema = command.get_schema()
manage_ressource('command', inserted, later, data_later, 'command_name', schema)
print("~~~~~~~~~~~~~~~~~~~~~~ post commands ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
update_later(later, inserted, 'command', 'use')

print("~~~~~~~~~~~~~~~~~~~~~~ add timeperiods ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
data_later = [{'field': 'use', 'type': 'simple', 'ressource': 'timeperiod'}]
schema = timeperiod.get_schema()
manage_ressource('timeperiod', inserted, later, data_later, 'timeperiod_name', schema)
print("~~~~~~~~~~~~~~~~~~~~~~ post timeperiods ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
update_later(later, inserted, 'timeperiod', 'use')

print("~~~~~~~~~~~~~~~~~~~~~~ add hostgroups ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
data_later = [{'field': 'members', 'type': 'list', 'ressource': 'host'},
              {'field': 'hostgroup_members', 'type': 'list', 'ressource': 'hostgroup'}]
schema = hostgroup.get_schema()
manage_ressource('hostgroup', inserted, later, data_later, 'hostgroup_name', schema)
print("~~~~~~~~~~~~~~~~~~~~~~ post hostgroups ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# TODO update_later lists

print("~~~~~~~~~~~~~~~~~~~~~~ add hostdependency ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
data_later = [{'field': 'use', 'type': 'simple', 'ressource': 'hostdependency'}]
schema = hostdependency.get_schema()
manage_ressource('hostdependency', inserted, later, data_later, 'name', schema)
print("~~~~~~~~~~~~~~~~~~~~~~ post hostdependency ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
update_later(later, inserted, 'hostdependency', 'use')

print("~~~~~~~~~~~~~~~~~~~~~~ add servicedependency ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
data_later = [{'field': 'use', 'type': 'simple', 'ressource': 'servicedependency'}]
schema = servicedependency.get_schema()
manage_ressource('servicedependency', inserted, later, data_later, 'name', schema)
print("~~~~~~~~~~~~~~~~~~~~~~ post servicedependency ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
update_later(later, inserted, 'servicedependency', 'use')

print("~~~~~~~~~~~~~~~~~~~~~~ add serviceextinfo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
data_later = [{'field': 'use', 'type': 'simple', 'ressource': 'serviceextinfo'}]
schema = serviceextinfo.get_schema()
manage_ressource('serviceextinfo', inserted, later, data_later, 'name', schema)
print("~~~~~~~~~~~~~~~~~~~~~~ post serviceextinfo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
update_later(later, inserted, 'serviceextinfo', 'use')

print("~~~~~~~~~~~~~~~~~~~~~~ add trigger ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
data_later = [{'field': 'use', 'type': 'simple', 'ressource': 'trigger'}]
schema = trigger.get_schema()
manage_ressource('trigger', inserted, later, data_later, 'trigger_name', schema)
print("~~~~~~~~~~~~~~~~~~~~~~ post trigger ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
update_later(later, inserted, 'trigger', 'use')

print("~~~~~~~~~~~~~~~~~~~~~~ add contact ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
data_later = [{'field': 'use', 'type': 'simple', 'ressource': 'contact'},
              {'field': 'contactgroups', 'type': 'list', 'ressource': 'contactgroup'},
              {'field': 'host_notification_period', 'type': 'simple', 'ressource': 'timeperiod'},
              {'field': 'service_notification_period', 'type': 'simple', 'ressource': 'timeperiod'},
              {'field': 'host_notification_commands', 'type': 'list', 'ressource': 'command'},
              {'field': 'service_notification_commands', 'type': 'list', 'ressource': 'command'}]
schema = contact.get_schema()
manage_ressource('contact', inserted, later, data_later, 'contact_name', schema)
print("~~~~~~~~~~~~~~~~~~~~~~ post contact ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
update_later(later, inserted, 'contact', 'use')

print("~~~~~~~~~~~~~~~~~~~~~~ add contactgroup ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
data_later = [{'field': 'members', 'type': 'list', 'ressource': 'contact'},
              {'field': 'contactgroup_members', 'type': 'list', 'ressource': 'contactgroup'}]
schema = contactgroup.get_schema()
manage_ressource('contactgroup', inserted, later, data_later, 'contactgroup_name', schema)
print("~~~~~~~~~~~~~~~~~~~~~~ post contactgroup ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# TODO update_later lists

print("~~~~~~~~~~~~~~~~~~~~~~ add contactrestrictrole ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
data_later = [{'field': 'conatct', 'type': 'simple', 'ressource': 'contact'}]
schema = contactrestrictrole.get_schema()
manage_ressource('contactrestrictrole', inserted, later, data_later, 'contact', schema)

print("~~~~~~~~~~~~~~~~~~~~~~ add escalation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
data_later = [{'field': 'use', 'type': 'simple', 'ressource': 'escalation'},
              {'field': 'contacts', 'type': 'list', 'ressource': 'contact'},
              {'field': 'contact_groups', 'type': 'list', 'ressource': 'contactgroup'}]
schema = escalation.get_schema()
manage_ressource('escalation', inserted, later, data_later, 'escalation_name', schema)
print("~~~~~~~~~~~~~~~~~~~~~~ post escalation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
update_later(later, inserted, 'escalation', 'use')
