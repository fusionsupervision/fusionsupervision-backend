#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2
import requests
import time
import subprocess
import json
from alignak_backend_client.client import Backend


class TestHookLivesynthesis(unittest2.TestCase):

    @classmethod
    def setUp(cls):
        cls.p = subprocess.Popen(['alignak_backend', 'start'])
        time.sleep(3)
        cls.backend = Backend('http://127.0.0.1:5000')
        cls.backend.login("admin", "admin", "force")

    @classmethod
    def tearDown(cls):
        cls.backend.delete("host", {})
        cls.backend.delete("service", {})
        cls.backend.delete("command", {})
        cls.backend.delete("livestate", {})
        cls.backend.delete("livesynthesis", {})
        cls.backend.delete("contact", {})
        cls.p.kill()


    def test_add_host(self):
        data = json.loads(open('cfg/host_srv001.json').read())
        self.backend.post("host", data)
        # Check if livesynthesis right created
        r = self.backend.get('livesynthesis')
        self.assertEqual(len(r['_items']), 1)
        self.assertEqual(r['_items'][0]['hosts_total'], 1)
        self.assertEqual(r['_items'][0]['hosts_up_hard'], 0)
        self.assertEqual(r['_items'][0]['hosts_up_soft'], 0)
        self.assertEqual(r['_items'][0]['hosts_down_hard'], 0)
        self.assertEqual(r['_items'][0]['hosts_down_soft'], 0)
        self.assertEqual(r['_items'][0]['hosts_unreachable_hard'], 1)
        self.assertEqual(r['_items'][0]['hosts_unreachable_soft'], 0)
        self.assertEqual(r['_items'][0]['hosts_acknowledged'], 0)
        self.assertEqual(r['_items'][0]['services_total'], 0)
        self.assertEqual(r['_items'][0]['services_ok_hard'], 0)
        self.assertEqual(r['_items'][0]['services_ok_soft'], 0)
        self.assertEqual(r['_items'][0]['services_warning_hard'], 0)
        self.assertEqual(r['_items'][0]['services_warning_soft'], 0)
        self.assertEqual(r['_items'][0]['services_critical_hard'], 0)
        self.assertEqual(r['_items'][0]['services_critical_soft'], 0)
        self.assertEqual(r['_items'][0]['services_unknown_hard'], 0)
        self.assertEqual(r['_items'][0]['services_unknown_soft'], 0)

    def test_add_service(self):
        # add host
        data = json.loads(open('cfg/host_srv001.json').read())
        self.backend.post("host", data)
        rh = self.backend.get('host')

        # Add command
        data = json.loads(open('cfg/command_ping.json').read())
        self.backend.post("command", data)
        # Check if command right in backend
        rc = self.backend.get('command')

        # Add service
        data = json.loads(open('cfg/service_srv001_ping.json').read())
        data['host_name'] = rh['_items'][0]['_id']
        data['check_command'] = rc['_items'][0]['_id']
        self.backend.post("service", data)

        # Check if livesynthesis right created
        r = self.backend.get('livesynthesis')
        self.assertEqual(len(r['_items']), 1)
        self.assertEqual(r['_items'][0]['hosts_total'], 1)
        self.assertEqual(r['_items'][0]['hosts_up_hard'], 0)
        self.assertEqual(r['_items'][0]['hosts_up_soft'], 0)
        self.assertEqual(r['_items'][0]['hosts_down_hard'], 0)
        self.assertEqual(r['_items'][0]['hosts_down_soft'], 0)
        self.assertEqual(r['_items'][0]['hosts_unreachable_hard'], 1)
        self.assertEqual(r['_items'][0]['hosts_unreachable_soft'], 0)
        self.assertEqual(r['_items'][0]['hosts_acknowledged'], 0)
        self.assertEqual(r['_items'][0]['services_total'], 1)
        self.assertEqual(r['_items'][0]['services_ok_hard'], 1)
        self.assertEqual(r['_items'][0]['services_ok_soft'], 0)
        self.assertEqual(r['_items'][0]['services_warning_hard'], 0)
        self.assertEqual(r['_items'][0]['services_warning_soft'], 0)
        self.assertEqual(r['_items'][0]['services_critical_hard'], 0)
        self.assertEqual(r['_items'][0]['services_critical_soft'], 0)
        self.assertEqual(r['_items'][0]['services_unknown_hard'], 0)
        self.assertEqual(r['_items'][0]['services_unknown_soft'], 0)
