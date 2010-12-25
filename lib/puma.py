#!/usr/bin/python

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
    def connect(self):
        return boto.connect_ec2(aws_access_key_id=self.config["access_id"],
                                aws_secret_access_key=self.config["access_secret"],
                                is_secure=False,
                                region=RegionInfo(None, self.config.get('location', "nova"),
                                                  self.config.get('ip', "127.0.0.1")),
                                port=self.config.get('port', 8773),
                                path=self.config.get('path', "services/Cloud"))

    def auth_group(self):
        self.connect.authorize_security_group(self.config.get("security_group", "default"),
                                                      ip_protocol='tcp',
                                                      from_port='22',
                                                      to_port='22',
                                      cidr_ip='%s/32' % self.config.get("ip", "127.0.0.1"))

    def get_image_list(self):
        return [image.id for image in self.connect().get_all_images()]

    def get_instance_list(self):
        return sum([instance.instances for instance in self.connect().get_all_instances()], [])

    def run_instance(self, image_name):
        #self.auth_group()
        return self.connect().run_instances(image_id="ami-tiny", instance_type="m1.tiny",key_name="joel")
