import threading
import time


def redirect_stdio():
    # disable stdout & stderr when frozen
    if getattr(sys, 'frozen', False):
        # running in a bundle (mean frozen)
        # if frozen, disable child process stdio, otherwise stdio buffer may exceed
        # maxBuffer of node.js execFile, and this child process would be killed.
        F_NULL = open(os.devnull, 'w')
        sys.stdout = F_NULL
        sys.stderr = F_NULL


def flush_stdio():
    while True:
        time.sleep(0.01)
        sys.stdout.flush()
        sys.stderr.flush()


t = threading.Thread(target=flush_stdio)
t.start()


if __name__ == '__main__':
    import sys
    import os
    redirect_stdio()

    import multiprocessing
    multiprocessing.freeze_support()
    
    from logger_config import configure_logger
    import environ
    
    configure_logger()
    
    try:
        import logging
        from server import start_rpc_server
        # run RPCServer
        port = int(os.environ['rpcServerPort'])
        start_rpc_server(port=port)

    except Exception as e:
        # If error in main loop, log to file and re-raise.
        logging.exception('RPC-Server runtime error')
        logging.critical('RPC-Server crashed')
