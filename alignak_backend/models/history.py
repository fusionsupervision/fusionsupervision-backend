#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource information of history
"""


def get_name():
    """
    Get name of this resource

    :return: name of this resource
    :rtype: str
    """
    return 'history'


def get_schema():
    """
    Schema structure of this resource

    :return: schema dictionary
    :rtype: dict
    """
    return {
        'schema': {
            'date': {
                'type': 'integer',
                'default': None
            },
            'host': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'host',
                    'embeddable': True
                },
                'required': True,
            },
            'service': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'service',
                    'embeddable': True
                },
                'required': True,
                'nullable': True
            },
            'user': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'user',
                    'embeddable': True
                },
                'nullable': True
            },
            'type': {
                'type': 'string',
                'required': True,
                'allowed': [
                    # Check result
                    "check.result",

                    # Request to force a check
                    "check.request",
                    "check.requested",

                    # Add acknowledge
                    "ack.add",
                    # Set acknowledge
                    "ack.processed",
                    # Delete acknowledge
                    "ack.delete",

                    # Add downtime
                    "downtime.add",
                    # Set downtime
                    "downtime.processed",
                    # Delete downtime
                    "downtime.delete"
                ],
                'default': 'check.result'
            },
            'message': {
                'type': 'string',
                'default': ''
            },
            'check_result': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'logcheckresult',
                    'embeddable': True
                },
                'required': False,
            },
            'content': {
                'type': 'dict',
                'schema': {
                    # Command acknowledge, useful?
                    'acknowledged': {
                        'type': 'boolean',
                        'default': False
                    },
                    # Execution result:
                    # 4: Not executed
                    # 3: Unknown (configuration problem, missing program,...)
                    # 0, 1, 2: Ok, Warning, Critical
                    'state_id': {
                        'type': 'integer',
                        'default': 4,
                        'allowed': [0, 1, 2, 3, 4],
                    },
                    'state': {
                        'type': 'string',
                        'allowed': [
                            "UP", "DOWN", "UNREACHABLE",
                            "OK", "WARNING", "CRITICAL", "UNKNOWN"
                        ],
                        'required': True,
                    },
                    'state_type': {
                        'type': 'string',
                        'allowed': [
                            "HARD", "SOFT"
                        ],
                        'required': True,
                    },
                    'last_state': {
                        'type': 'string',
                        'allowed': [
                            "UP", "DOWN", "UNREACHABLE",
                            "OK", "WARNING", "CRITICAL", "UNKNOWN"
                        ],
                        'required': True,
                    },
                    'last_state_type': {
                        'type': 'string',
                        'allowed': [
                            "HARD", "SOFT"
                        ],
                        'required': True,
                    },
                    'state_changed': {
                        'type': 'boolean',
                        'default': False
                    },
                    'latency': {
                        'type': 'float',
                        'default': 0.0
                    },
                    'execution_time': {
                        'type': 'float',
                        'default': 0.0
                    },
                    # Service concerned
                    # To be used like a service_description:
                    # - package name for a peripheral
                    # - 'kiosk' for the kiosk status
                    'service': {
                        'type': 'string'
                    },
                    # Execution result message
                    'output': {
                        'type': 'string'
                    },
                    # Execution result message (extra information)
                    'long_output': {
                        'type': 'string'
                    },
                    # Execution result performance data
                    'perfdata': {
                        'type': 'string'
                    }
                }
            },
            '_realm': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'realm',
                    'embeddable': True
                },
                'required': True,
            },
            '_sub_realm': {
                'type': 'boolean',
                'default': False
            },
            '_users_read': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'user',
                        'embeddable': True,
                    }
                },
            },
        }
    }
