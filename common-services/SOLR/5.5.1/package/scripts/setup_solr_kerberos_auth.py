from resource_management.core.resources.system import Execute, File
from resource_management.libraries.functions.format import format
from resource_management.core.source import Template


def setup_solr_kerberos_auth():
    import params

    File(format("{solr_kerberos_jaas_config}"),
         content=Template("solr_server_jaas.conf.j2"),
         owner=params.solr_config_user
         )

    if not params.solr_cloud_mode:
        return

    zk_client_prefix = format('export JAVA_HOME={java64_home}; {cloud_scripts}/zkcli.sh -zkhost ' +
                              '{zookeeper_hosts}{solr_cloud_zk_directory}')
    command = format('{zk_client_prefix} -cmd put /security.json ')
    command += '\'{"authentication":{"class": "org.apache.solr.security.KerberosPlugin"}}\''
    Execute(command,
            ignore_failures=True,
            user=params.solr_config_user
            )
