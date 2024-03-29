#
#   SpyServer User Monitor - Netstat parsing
#
import io
import logging
import subprocess
from contextlib import contextmanager


@contextmanager
def pipe(*command):
    """ Open a subprocess and return lines from it. """
    with open("/dev/null", "wb") as devnull:
        with subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=devnull
        ).stdout as f:
            if bytes is not str:  # Python 3
                f = io.TextIOWrapper(f, encoding="UTF-8", errors="replace")
            yield f


def netstat_listeners(program_filter=None):
    """ Run NetStat to determine what current processes are listening on TCP ports 
        Can also filter by program name.

    """

    _output = {}

    with pipe("netstat", "-tnlp") as f:
        for line in f:
            if line.rstrip().startswith("Proto"):
                break

        for line in f:
            parts = line.split()

            # Example TCP output
            # ['tcp', '0', '0', '0.0.0.0:22', '0.0.0.0:*', 'LISTEN', '-']

            # Skip over IPv6 sockets because i'm lazy
            if "tcp6" in parts[0]:
                continue

            host, port = parts[3].split(":")
            port = int(port)

            pid_program = parts[6]

            if "/" in pid_program:
                pid, program = pid_program.split("/", 1)

                # If a filter has been provided, filter by it.
                if program_filter is not None:
                    if program_filter not in program:
                        continue

            else:
                # PID unknown
                # If we have a filter set, we have no way of knowing what the program name is, so skip it.
                if program_filter is not None:
                    continue
                pid = None
                program = "unknown"

            _output[port] = {"host": host, "pid": pid, "program": program}

    return _output


def netstat_users():
    """ Run NetStat to determine what current TCP connections are in progress 
        Output as a dict of lists, organised by server TCP port number.
        e.g.
        {
            5020: ['ip_1', 'ip_2'],
            5040: ['ip_3', 'ip_4]
        }
    """

    _output = {}

    with pipe("netstat", "-tn") as f:
        for line in f:
            if line.rstrip().startswith("Proto"):
                break

        for line in f:
            parts = line.split()

            # Example
            # ['tcp', '0', '5160', '192.168.88.201:5020', '<ip>:52008', 'ESTABLISHED']

            # Skip over IPv6 connections because I'm lazy.
            if "tcp6" in parts[0]:
                continue

            server_host, server_port = parts[3].split(":")
            server_port = int(server_port)

            client_host, client_port = parts[4].split(":")
            client_port = int(client_port)

            if server_port not in _output:
                _output[server_port] = [client_host]
            else:
                _output[server_port].append(client_host)

    return _output


def main():
    print("Listeners:")
    print(netstat_listeners(program_filter="spyserver"))
    print("Clients:")
    print(netstat_users())


if __name__ == "__main__":
    main()
