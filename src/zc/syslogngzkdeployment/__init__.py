import subprocess
import zc.metarecipe
import zc.zk

class Aggregate(zc.metarecipe.Recipe):

    def __init__(self, buildout, name, options):
        super(Aggregate, self).__init__(buildout, name, options)
        assert name.endswith('.0'), name # There can be only one.

        name = name[:-2]
        path = '/'+name.replace(',', '/')
        name = name.replace(',', '_')

        zk = zc.zk.ZK('zookeeper:2181')
        options = zk.properties(path)

        self['deployment'] = dict(
            recipe = 'zc.recipe.deployment',
            name = name,
            user = options.get('user', 'zope'),
            )

        self[name+'.conf'] = dict(
            recipe = 'zc.recipe.deployment:configuration',
            deployment = 'deployment',
            directory = '/etc/syslog-ng/syslog-ng.d',
            text = aggregate_template % dict(
                port = options['port'],
                name = name,
                lpath = options.get(
                    'path', '/var/log/%s/$R_YEAR-$R_MONTH-$R_DAY.log' % name)
                ),
            )

    def install(self):
        subprocess.call('/etc/init.d/syslog-ng reload')

    update = install

aggregate_template = r'''
source s_%(name)s {
    tcp(ip(0.0.0.0)
    max_connections(1000)
    time_zone("+00:00")
    port(%(port)s));
    };

destination d_%(name)s {
    file("%(lpath)s"
         perm(0644)
         dir_perm(0755)
         create_dirs(yes)
         template("$HOST $PROGRAM $MSG\n")
         template_escape(no)
         );
    };

log { source(s_%(name)s); destination(d_%(name)s); };
'''
