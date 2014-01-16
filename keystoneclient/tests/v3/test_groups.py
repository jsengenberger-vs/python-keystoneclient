# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import uuid

import httpretty

from keystoneclient.tests.v3 import utils
from keystoneclient.v3 import groups


class GroupTests(utils.TestCase, utils.CrudTests):
    def setUp(self):
        super(GroupTests, self).setUp()
        self.key = 'group'
        self.collection_key = 'groups'
        self.model = groups.Group
        self.manager = self.client.groups

    def new_ref(self, **kwargs):
        kwargs = super(GroupTests, self).new_ref(**kwargs)
        kwargs.setdefault('name', uuid.uuid4().hex)
        return kwargs

    @httpretty.activate
    def test_list_groups_for_user(self):
        user_id = uuid.uuid4().hex
        ref_list = [self.new_ref(), self.new_ref()]

        self.stub_entity(httpretty.GET,
                         ['users', user_id, self.collection_key],
                         status=200, entity=ref_list)

        returned_list = self.manager.list(user=user_id)
        self.assertEqual(len(ref_list), len(returned_list))
        [self.assertTrue(isinstance(r, self.model)) for r in returned_list]

    @httpretty.activate
    def test_list_groups_for_domain(self):
        ref_list = [self.new_ref(), self.new_ref()]
        domain_id = uuid.uuid4().hex

        self.stub_entity(httpretty.GET,
                         [self.collection_key],
                         status=200, entity=ref_list)

        returned_list = self.manager.list(domain=domain_id)
        self.assertTrue(len(ref_list), len(returned_list))
        [self.assertTrue(isinstance(r, self.model)) for r in returned_list]

        self.assertEqual(httpretty.last_request().querystring,
                         {'domain_id': [domain_id]})
