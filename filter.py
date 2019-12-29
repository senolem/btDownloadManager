"""
This script is designed to ban leeches who do not upload
their files, such as '-XL0012-' aka '迅雷' in Chinese.

The API documents referred in this URL:
https://github.com/qbittorrent/qBittorrent/wiki/Web-API-Documentation#set-application-preferences
"""

from urllib import request
import json
import sys
import time
import argparse


def _get_url(url) -> str:
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'

    headers = {'X-Request': 'JSON',
               'User-Agent': user_agent,
               'X-Requested-With': 'XMLHttpRequest',
               'Accept': '*/*'}

    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)

    test = resp.read()
    return test.decode('ascii', 'ignore')


def _post_url(url, content):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'

    headers = {'User-Agent': user_agent,
               'X-Requested-With': 'XMLHttpRequest',
               'Accept': '*/*'}

    request.urlopen(request.Request(url, str.encode(content)))


class IpFilter:

    def __init__(self, url='localhost', port=8080):
        self.torrents_dict = {}
        self.url_port = "http://" + url + ":" + str(port)
        print('connecting to server ' + self.url_port)

    def get_torrent_list(self):
        server_url = self.url_port + "/api/v2/sync/maindata"
        torrents_str = _get_url(server_url)
        obj = json.loads(torrents_str)
        self.torrents_dict = obj['torrents']

    def filter(self):
        """
        Get all the connected peers using torrent hash list and ban the matched peer.
        """
        # the banned_ip value is ip address string split with '\n'
        banned_ip_str = json.loads(_get_url(self.url_port + "/api/v2/app/preferences"))["banned_IPs"]

        for item in self.torrents_dict:
            if self.torrents_dict[item]['num_leechs'] > 0:
                peers = json.loads(self._get_peers_list(item))['peers']
                for ip_port in peers:
                    for xl in ['XL0012', 'Xunlei']:
                        if xl in peers[ip_port]['client']:
                            banned_ip_str += '\n'
                            banned_ip_str += peers[ip_port]['ip']
                            time_str = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
                            print(time_str + peers[ip_port]['ip']
                                  + ' has been deleted due to client name:' + peers[ip_port]['client'])

        _post_url(self.url_port + "/api/v2/app/setPreferences", "json={\"banned_IPs\":\"" + banned_ip_str + "\"}")

    def _get_peers_list(self, torrent_hash):
        server_url = self.url_port + "/api/v2/sync/torrentPeers?rid=0&hash=" + torrent_hash
        return _get_url(server_url)

    def start(self, torrent_time_cycle=300, filter_time_cycle=10):
        """
        Run a while true loop to ban matched ip with certain time interval.
        :param torrent_time_cycle: Time interval to check the torrent list.
        :param filter_time_cycle: Time interval to check the peers.
        :return: none
        """

        print('torrent time interval is ' + str(torrent_time_cycle))
        print('filter time interval is ' + str(filter_time_cycle))
        while True:
            self.get_torrent_list()
            for i in range(0, int(torrent_time_cycle / filter_time_cycle)):
                self.filter()
                time.sleep(filter_time_cycle)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ban Xunlei peers in qBittorrent connections.',
                                     epilog='eg: python3 filter.py -u localhost -p 8080 -a 300 -b 10')
    parser.add_argument('-u', default='localhost', help='url of the service without \'http://\'')
    parser.add_argument('-p', default=8080, type=int, help='port number. default=8080')
    parser.add_argument('-a', default=300,  type=int, help='time interval to fetch torrents list in seconds. default=300')
    parser.add_argument('-b', default=10,   type=int, help='time interval to fetch peers list in seconds. default=10')

    config = parser.parse_args()
    f = IpFilter(url=config.u, port=config.p)
    f.start(torrent_time_cycle=config.a, filter_time_cycle=config.b)
