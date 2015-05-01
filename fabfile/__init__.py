#!/usr/bin/env python
# coding: utf-8



from fabric.api import env

import tail
import dev
import warden

#env.hosts = []
env.user = "vcap"
env.password = "c1oudc0w"


