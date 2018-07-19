# -*- coding: utf-8 -*-
# Copyright (c) 2018 Christiaan Frans Rademan.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
from luxon import register
from luxon import router
from luxon import db

from katalog.models.index import katalog_file

@register.resources()
class Objects(object):
    def __init__(self):
        router.add('GET', 'regex:^.*$', self.get,
                   tag='services')

        router.add('POST', 'regex:^.*$', self.upload,
                   tag='services')

        router.add([ 'PUT', 'PATCH' ], 'regex:^.*$', self.update,
                   tag='services')

        router.add('DELETE', 'regex:^.*$', self.delete,
                   tag='services')

    def get(self, req, resp):
        model = katalog_file()
        model.sql_id(req.route)
        resp.set_header('Content-Type', model['mime_type'])
        return model['content']

    def upload(self, req, resp):
        model = katalog_file()
        model['path'] = req.route
        model['content'] = req.read()

        if req.content_type is None:
            model['mime_type'] = "text/plain; charset=utf-8"
        else:
            model['mime_type'] = req.content_type

        model.commit()

    def update(self, req, resp):
        model = katalog_file()
        model.sql_id(req.route)
        model['content'] = req.read()

        if req.content_type is not None:
            model['mime_type'] = req.content_type

        model.commit()

    def delete(self, req, resp):
        with db() as conn:
            conn.execute('DELETE FROM katalog_file WHERE path = %s', req.route)
            conn.commit()

