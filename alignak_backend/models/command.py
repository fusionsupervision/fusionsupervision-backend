def get_name():
    return 'command'


def get_schema():
    return {
        'schema': {
            'use': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'command',
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

            'command_name': {
                'type': 'string',
                'required': True,
                'unique': True,
            },

            'command_line': {
                'type': 'string',
                'required': True,
            },

            'poller_tag': {
                'type': 'string',
                'default': 'None'
            },

            'reactionner_tag': {
                'type': 'string',
                'default': 'None'
            },

            'module_type': {
                'type': 'string',
                'default': 'fork'
            },

            'timeout': {
                'type': 'integer',
                'default': -1
            },

            'enable_environment_macros': {
                'type': 'boolean',
                'default': False
            },
        }
    }