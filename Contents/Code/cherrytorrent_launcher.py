###############################################################################
import cherrytorrent
import urllib2

###############################################################################
HTTP_PORT = 8042

###############################################################################
def start_cherrytorrent():
    Thread.Create(thread_proc)

###############################################################################
def thread_proc():
    class CustomLoggerStream:
        def __init__(self, port):
            self.port = port

        def write(self, str):
            Log.Info('{0}'.format(str.rstrip()))

        def flush(self):
            pass

    while True:
        http_config    = { 
                            'port':                 HTTP_PORT
                         }

        try:
            max_download_rate = int(float(Prefs['MAX_DOWNLOAD_RATE']))
        except:
            max_download_rate = 0

        try:
            max_upload_rate = int(float(Prefs['MAX_UPLOAD_RATE']))
        except:
            max_upload_rate = 0

        torrent_config = {
                            'port':                 int(Prefs['INCOMING_PORT']),
                            'max_download_rate':    max_download_rate,
                            'max_upload_rate':      max_upload_rate,
                            'keep_files':           Prefs['KEEP_FILES'],
                            'proxy_type':           Prefs['TORRENT_PROXY_TYPE'],
                            'proxy_host':           Prefs['TORRENT_PROXY_HOST'],
                            'proxy_port':           int(Prefs['TORRENT_PROXY_PORT']) if Prefs['TORRENT_PROXY_PORT'] else 0,
                            'proxy_user':           Prefs['TORRENT_PROXY_USER'],
                            'proxy_password':       Prefs['TORRENT_PROXY_PASSWORD'],
                         }
        
        server = cherrytorrent.Server(http_config, torrent_config, CustomLoggerStream(HTTP_PORT))
        server.run()

###############################################################################
def get_server_status(port):
    try:
        status_json = JSON.ObjectFromURL('http://{0}:{1}'.format(Network.Address, port), cacheTime=0)
        return status_json
    except urllib2.URLError as exception:
        Log.Error('Server unreachable: {0}'.format(exception.reason))
    except Exception as exception:
        Log.Error('Unhandled exception: {0}'.format(exception))

    return None
