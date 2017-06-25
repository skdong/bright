import socket
import constants
import json
import random
import select
import pprint

from log import LOG


class OVSDB_Client(object):
    def __init__(self):
        self.ovsdb = None

    def _gen_id(self):
        return 'a' + str(random.getrandbits(128))

    def _connection(self):
        if not self.ovsdb:
            self.ovsdb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ovsdb.connect(constants.OVSDB_SERVER)

    def _gen_request(self, method, params=[], uuid=None):
        return dict(method=method,
                    params=params,
                    id=uuid if uuid else self._gen_id())

    def _close(self):
        if self.ovsdb:
            try:
                self.ovsdb.close()
            except Exception as e:
                LOG.error(str(e))
            self.ovsdb = None

    def _send(self, info):
        if not self.ovsdb:
            self._connection()
        try:
            self.ovsdb.send(json.dumps(info))
        except Exception as e:
            LOG.error(e.message())
            self._close()

    def _recv(self, size=constants.BUFFER_SIZE):
        message = ''
        while True:
            try:
                self.ovsdb.setblocking(0)
                ready = select.select([self.ovsdb], [], [], constants.TIME_OUT)
                if ready[0]:
                    buf = self.ovsdb.recv(size)
                    message += buf
                else:
                    break
            except Exception as e:
                LOG.error(e.message())
                self._close()
                break
        return message

    def list_dbs(self):
        self._send(self._gen_request(method='list_dbs'))
        return json.loads(self._recv())

    def get_schema(self, schema):
        self._send(self._gen_request('get_schema', [schema]))
        return json.loads(self._recv())

    def get_table(self, schema, table):
        params = []
        params.append(constants.OVSDB_SCHEMA_NAME)
        params.append()
        self._send(self._gen_request('transact', params))


OVSDB = OVSDB_Client()


def test_list_dbs():
    LOG.info(OVSDB.list_dbs())


def test_get_schema():
    pprint.pprint(OVSDB.get_schema(constants.OVSDB_SCHEMA_NAME))


def main():
    test_get_schema()


if __name__ == "__main__":
    main()
