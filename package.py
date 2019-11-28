from Jumpscale import j

class Package(j.baseclasses.threebot_package):
    """
    to start need to run 
    kosmos -p
    cl = j.servers.threebot.local_start_default()
    cl.actors.package_manager.package_add(git_url="https://github.com/enertia-io/www_enertia_io")
    we need to restart lapis tmux
    """
    def _init(self, **kwargs):
        self.branch = kwargs["package"].branch or "master"
        self.enertia_io = "https://github.com/enertia-io/www_enertia_io.git"

    def prepare(self):
        """
        called when the 3bot starts
        :return:
        """
        server = self.openresty
        server.install(reset=True)
        server.configure()
        website = server.get_from_port(443)
        locations = website.locations.get("enertia_io")
        static_location = locations.locations_static.new()
        static_location.name = "static"
        static_location.path_url = "/"
        path = j.clients.git.getContentPathFromURLorPath(self.enertia_io, branch=self.branch, pull=True)
        static_location.path_location = path
        static_location.use_jumpscale_weblibs = True
        website.path = path
        locations.configure()
        website.configure()

    def start(self):
        """
        called when the 3bot starts
        :return:
        """
        self.prepare()
    def stop(self):
        """
        called when the 3bot stops
        :return:
        """
        pass

    def uninstall(self):
        """
        called when the package is no longer needed and will be removed from the threebot
        :return:
        """
        pass
