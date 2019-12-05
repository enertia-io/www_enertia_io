from Jumpscale import j

class Package(j.baseclasses.threebot_package):
    def setup_locations(self):
        """
        ports & paths used for threebotserver
        see: {DIR_BASE}/code/github/threefoldtech/jumpscaleX_core/docs/3Bot/web_environment.md
        will start bottle server web interface which include (gedis http interface, gedis websocket interface and
        bcdbfs web server)
        endpoints:
        "/web/gedis/http"       >    gedis htto interface
        "/web/gedis/websocket"  >    gedis websocket interface
        "/web/bcdbfs"           >    bcdbfs web server
        "/weblibs"              >    static jumpscale weblibs files
        """

        self.openresty.configure()

        # get our main webserver
        for port in (443, 80):
            website = self.openresty.get_from_port(port)

            # PROXY for gedis HTTP
            locations = website.locations.get(name="webinterface_locations")

            package_actors_location = locations.locations_proxy.new()
            package_actors_location.name = "enertia"
            package_actors_location.path_url = "~* /(.*)/(.*)/actors/(.*)/(.*)$"
            package_actors_location.ipaddr_dest = "127.0.0.1"
            package_actors_location.port_dest = 9999
            package_actors_location.path_dest = ""
            package_actors_location.type = "http"
            package_actors_location.scheme = "http"

            ## more code omitted.


            website.configure()

    def start(self):

        # add the main webapplication

        self.setup_locations()

        from threebot_packages.zerobot.webinterface.bottle.gedis import app

        self.gevent_rack.bottle_server_add(name="bottle_web_interface", port=9999, app=app, websocket=True)
        # self.gevent_rack.webapp_root = webapp
