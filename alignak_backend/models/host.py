#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource information of host
"""

def get_name():
    """
    Get name of this resource

    :return: name of this resource
    :rtype: str
    """
    return 'host'


def get_schema():
    """
    Schema structure of this resource

    :return: schema dictionnary
    :rtype: dict
    """
    return {
        'allow_unknown': True,
        'schema': {
            'imported_from': {
                'type': 'string',
                'default': ''
            },
            'use': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'host',
                    'embeddable': True
                },
            },
            'name': {
                'type': 'string',
                'default': ''
            },
            'definition_order': {
                'type': 'integer',
                'default': 100
            },
            'register': {
                'type': 'boolean',
                'default': True
            },
            'host_name': {
                'type': 'string',
                'required': True,
                'unique': True,
                'regex': '^[^`~!$%^&*"|\'<>?,()=]+$'
            },
            'alias': {
                'type': 'string',
                'default': ''
            },
            'display_name': {
                'type': 'string',
                'default': ''
            },
            'address': {
                'type': 'string',
                'default': ''
            },
            'parents': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'host',
                        'embeddable': True,
                    }
                },
            },
            'hostgroups': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'hostgroup',
                        'embeddable': True,
                    }
                },
            },
            'check_command': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'command',
                    'embeddable': True
                }
            },
            'check_command_args': {
                'type': 'string',
                'default': ''
            },
            'initial_state': {
                'type': 'string',
                'minlength': 1,
                'maxlength': 1,
                'default': 'u',
                'allowed': ["u", "d", "u"]
            },
            'max_check_attempts': {
                'type': 'integer',
                'default': 1
            },
            'check_interval': {
                'type': 'integer',
                'default': 5
            },
            'retry_interval': {
                'type': 'integer',
                'default': 0
            },
            'active_checks_enabled': {
                'type': 'boolean',
                'default': True
            },
            'passive_checks_enabled': {
                'type': 'boolean',
                'default': True
            },
            'check_period': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'timeperiod',
                    'embeddable': True
                }
            },
            'check_freshness': {
                'type': 'boolean',
                'default': False
            },
            'freshness_threshold': {
                'type': 'integer',
                'default': 0
            },
            'event_handler': {
                'type': 'string',
                'default': ''
            },
            'event_handler_enabled': {
                'type': 'boolean',
                'default': False
            },
            'low_flap_threshold': {
                'type': 'integer',
                'default': 25
            },
            'high_flap_threshold': {
                'type': 'integer',
                'default': 50
            },
            'flap_detection_enabled': {
                'type': 'boolean',
                'default': True
            },
            'flap_detection_options': {
                'type': 'list',
                'default': ['o', 'd', 'u']
            },
            'process_perf_data': {
                'type': 'boolean',
                'default': True
            },
            'retain_status_information': {
                'type': 'boolean',
                'default': True
            },
            'retain_nonstatus_information': {
                'type': 'boolean',
                'default': True
            },
            'contacts': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'contact',
                        'embeddable': True,
                    }
                },
            },
            'contact_groups': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'contactgroup',
                        'embeddable': True,
                    }
                },
            },
            'notification_interval': {
                'type': 'integer',
                'default': 60
            },
            'first_notification_delay': {
                'type': 'integer',
                'default': 0
            },
            'notification_period': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'timeperiod',
                    'embeddable': True
                }
            },
            'notification_options': {
                'type': 'list',
                'default': ['d', 'u', 'r', 'f']
            },
            'notifications_enabled': {
                'type': 'boolean',
                'default': True
            },
            'stalking_options': {
                'type': 'list',
                'default': []
            },
            'notes': {
                'type': 'string',
                'default': ''
            },
            'notes_url': {
                'type': 'string',
                'default': ''
            },
            'action_url': {
                'type': 'string',
                'default': ''
            },
            'icon_image': {
                'type': 'string',
                'default': ''
            },
            'icon_image_alt': {
                'type': 'string',
                'default': ''
            },
            'icon_set': {
                'type': 'string',
                'default': ''
            },
            'vrml_image': {
                'type': 'string',
                'default': ''
            },
            'statusmap_image': {
                'type': 'string',
                'default': ''
            },
            '2d_coords': {
                'type': 'string',
                'default': ''
            },
            '3d_coords': {
                'type': 'string',
                'default': ''
            },
            'failure_prediction_enabled': {
                'type': 'boolean',
                'default': False
            },
            'realm': {
                'type': 'string',
                'default': None
            },
            'poller_tag': {
                'type': 'string',
                'default': 'None'
            },
            'reactionner_tag': {
                'type': 'string',
                'default': 'None'
            },
            'resultmodulations': {
                'type': 'list',
                'default': []
            },
            'business_impact_modulations': {
                'type': 'list',
                'default': []
            },
            'escalations': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'escalation',
                        'embeddable': True,
                    }
                },
            },
            'maintenance_period': {
                'type': 'string',
                'default': ''
            },
            'time_to_orphanage': {
                'type': 'integer',
                'default': 300
            },
            'service_overrides': {
                'type': 'list',
                'default': []
            },
            'service_excludes': {
                'type': 'list',
                'default': []
            },
            'service_includes': {
                'type': 'list',
                'default': []
            },
            'labels': {
                'type': 'list',
                'default': []
            },
            'business_rule_output_template': {
                'type': 'string',
                'default': ''
            },
            'business_rule_smart_notifications': {
                'type': 'boolean',
                'default': False
            },
            'business_rule_downtime_as_ack': {
                'type': 'boolean',
                'default': False
            },
            'business_rule_host_notification_options': {
                'type': 'list',
                'default': []
            },
            'business_rule_service_notification_options': {
                'type': 'list',
                'default': []
            },
            'business_impact': {
                'type': 'integer',
                'default': 2
            },
            'trigger': {
                'type': 'string',
                'default': ''
            },
            'trigger_name': {
                'type': 'string',
                'default': ''
            },
            'trigger_broker_raise_enabled': {
                'type': 'boolean',
                'default': False
            },
            'trending_policies': {
                'type': 'list',
                'default': []
            },
            'checkmodulations': {
                'type': 'list',
                'default': []
            },
            'macromodulations': {
                'type': 'list',
                'default': []
            },
            'custom_views': {
                'type': 'list',
                'default': []
            },
            'snapshot_enabled': {
                'type': 'boolean',
                'default': False
            },
            'snapshot_command': {
                'type': 'string',
                'default': ''
            },
            'snapshot_period': {
                'type': 'string',
                'default': ''
            },
            'snapshot_criteria': {
                'type': 'list',
                'default': ['d', 'u']
            },
            'snapshot_interval': {
                'type': 'integer',
                'default': 5
            },
            '_brotherhood': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'brotherhood',
                        'embeddable': True,
                    }
                },
            },
            '_users_read': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'contact',
                        'embeddable': True,
                    }
                },
            },
            '_users_create': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'contact',
                        'embeddable': True,
                    }
                },
            },
            '_users_update': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'contact',
                        'embeddable': True,
                    }
                },
            },
            '_users_delete': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'contact',
                        'embeddable': True,
                    }
                },
            },
        }
    }
