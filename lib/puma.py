#!/usr/bin/python

#Copyright 2010 Joel Buchheim-Moore

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


import yaml, boto, os
from boto.ec2.regioninfo import RegionInfo

class Puma():
    def __init__(self):
        self.puma_dir = os.environ["HOME"] + "/.puma"
        try:
            self.config = yaml.load(file(self.puma_dir + "/config.yml", "r"))
        except:
            print "ERROR: No config file. need to make one"

        self.keyfile = self.puma_dir + "/creds/" + self.config["keyfile"]
        self.keyname = self.config.get('keyname', "admin")
    def connect(self):
        return boto.connect_ec2(aws_access_key_id=self.config["access_id"],
                                aws_secret_access_key=self.config["access_secret"],
                                is_secure=False,
                                region=RegionInfo(None, self.config.get('location', "nova"),
                                                  self.config.get('ip', "127.0.0.1")),
                                port=self.config.get('port', 8773),
                                path=self.config.get('path', "services/Cloud"))

    def get_image_list(self):
        return [image.id for image in self.connect().get_all_images()]

    def get_instance_list(self):
        return sum([instance.instances for instance in self.connect().get_all_instances()], [])

    def run_instance(self, image_name, num, type):
        return self.connect().run_instances(image_id=image_name, instance_type=type,key_name=self.keyname,
                                           max_count=num)
    def terminate_instance(self, name):
        return self.connect().terminate_instances(name)
