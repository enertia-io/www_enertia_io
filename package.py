from Jumpscale import j

class Package(j.baseclasses.threebot_package):
    """
    kosmos -p
    cl = j.servers.threebot.local_start_default()
    j.threebot.packages.zerobot.packagemanager.actors.package_manager.package_add(git_url="https://github.com/enertia-io/www_enertia_io")
    """

    def _init(self, **kwargs):
        self.branch = kwargs["package"].branch or "master"
        self.enertia_io = "https://github.com/enertia-io/www_enertia_io"

    def prepare(self):
        website = self.openresty.get_from_port(443)
        locations = website.locations.get("enertia_io")
        static_location = locations.locations_static.new()
        static_location.name = "static"
        static_location.path_url = "/enertia"
        path = j.clients.git.getContentPathFromURLorPath(self.enertia_io, branch=self.branch, pull=True)
        static_location.path_location = path
        static_location.use_jumpscale_weblibs = True # if set, will copy weblibs and serve it from /static/weblibs directly
        locations.configure()
        website.configure()

    def start(self):
        self.prepare()
        
