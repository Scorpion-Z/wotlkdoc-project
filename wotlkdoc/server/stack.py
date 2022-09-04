# -*- coding: utf-8 -*-

import typing as T
import attr
import cottonformation as cf
from cottonformation.res import ec2


@attr.s
class MainStack(cf.Stack):
    project_name: str = attr.ib()
    stage: str = attr.ib()
    vpc_id: str = attr.ib()
    default_sg_id: str = attr.ib()
    sg_authorized_ips: T.List[str] = attr.ib(factory=list)

    @property
    def env_name(self):
        """
        A prefix for most of naming convention. Isolate resource from each other.
        """
        return f"{self.project_name}-{self.stage}"

    @property
    def stack_name(self):
        """
        CloudFormation stack name.
        """
        return f"{self.env_name}"

    def mk_rg1(self):
        """
        Make resource group 1
        """
        name = f"{self.env_name}/sg/project-default"
        self.sg_project_default = ec2.SecurityGroup(
            "SecurityGroupProjectDefault",
            rp_GroupDescription="Resources that has this security can talk to each other",
            p_GroupName=name,
            p_VpcId=self.vpc_id,
            p_SecurityGroupIngress=[
                ec2.PropSecurityGroupIngress(
                    rp_IpProtocol="-1",
                    p_FromPort=-1,
                    p_ToPort=-1,
                    p_CidrIp=f"{authorized_ip}/32",
                )
                for authorized_ip in self.sg_authorized_ips
            ],
            p_Tags=cf.Tag.make_many(
                Name=name
            ),
        )

    def mk_rg2(self):
        """
        Make resource group 2
        """
        pass

    def mk_rg3(self):
        """
        Make resource group 3
        """
        pass

    def post_hook(self):
        """
        A user custom post stack initialization hook function. Will be executed
        after object initialization.

        We will put all resources in two different resource group.
        And there will be a factory method for each resource group. Of course
        we have to explicitly call it to create those resources.
        """
        self.mk_rg1()
        self.mk_rg2()
        self.mk_rg3()

"""

mysql --host="prod-server.c7pwcs7oc5l0.us-east-1.rds.amazonaws.com" --user="admin" --password="gw8CH&wjRW%Q"

GRANT ALL PRIVILEGES ON * . * TO 'acore'@'gw8CH&wjRW%Q' WITH GRANT OPTION;

CREATE USER 'acore'@'localhost' IDENTIFIED BY 'acore' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0;
CREATE USER 'new_master_user'@'%' IDENTIFIED BY 'password';


GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* TO 'new_master_user'@'%' WITH GRANT OPTION;

"""