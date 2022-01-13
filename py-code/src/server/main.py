"""
An entry for all zeroRPC APIs
Specified apis are classed in package api
This is the entry of the entire python app
"""

from concurrent import futures

import grpc
import msgpack

from server.configs import DEFAULT_SERVER_PORT, MAX_MESSAGE_LENGTH

from . import rpc_pb2
from . import rpc_pb2_grpc
from apis import ApiRouter

class RPCServicer(rpc_pb2_grpc.ServiceRPCServicer):

    __router = ApiRouter()

    def request(self, request, context):
        try:
            route = request.route
            argData = msgpack.unpackb(request.argData)
            args = argData['args']
            kwargs = argData['kwargs']
            reply = self.__router.invoke_api(route, args=args or [], kwargs=kwargs or {})
            bytesReply = msgpack.packb(reply)
        except Exception as e:
            err_msg = type(e).__name__
            if e.args:
                err_msg += ': {desc}'.format(desc=e.args[0])
            context.abort(grpc.StatusCode.UNKNOWN, err_msg)
        return rpc_pb2.ApiResponse(replyData=bytesReply)

    def listApis(self, request, context):
        try:
            routes = self.__router.list_apis()
        except Exception as e:
            err_msg = type(e).__name__
            if e.args:
                err_msg += ': {desc}'.format(desc=e.args[0])
            context.abort(grpc.StatusCode.UNKNOWN, err_msg)
        return rpc_pb2.RpcRoutesList(rpcRoute=routes)


def start_rpc_server(host='127.0.0.1', port=DEFAULT_SERVER_PORT, max_workers=1, max_message_length=MAX_MESSAGE_LENGTH):
    host = "127.0.0.1"
    addr = '{host}:{port}'.format(host=host, port=port)
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers), 
        options=[
            ('grpc.max_send_message_length', max_message_length),
            ('grpc.max_receive_message_length', max_message_length),
        ]
    )
    rpc_pb2_grpc.add_ServiceRPCServicer_to_server(
        RPCServicer(), server
    )
    server.add_insecure_port(addr)
    server.start()
    server.wait_for_termination()
