# The code is copied from https://github.com/blockchain-etl/ethereum-etl

from web3 import HTTPProvider
from web3._utils.request import make_post_request
from urllib.parse import urlparse
from const import DEFAULT_TIMEOUT


class BatchHTTPProvider(HTTPProvider):
    def make_batch_request(self, text):
        self.logger.debug(
            "Making request HTTP. URI: %s, Request: %s", self.endpoint_uri, text
        )
        request_data = text.encode("utf-8")
        raw_response = make_post_request(
            self.endpoint_uri, request_data, **self.get_request_kwargs()
        )
        response = self.decode_rpc_response(raw_response)
        self.logger.debug(
            "Getting response HTTP. URI: %s, " "Request: %s, Response: %s",
            self.endpoint_uri,
            text,
            response,
        )
        return response


def get_provider_from_uri(uri_string, timeout=DEFAULT_TIMEOUT, batch=False):
    uri = urlparse(uri_string)
    if uri.scheme == "http" or uri.scheme == "https":
        request_kwargs = {"timeout": timeout}
        if batch:
            return BatchHTTPProvider(uri_string, request_kwargs=request_kwargs)
        else:
            return HTTPProvider(uri_string, request_kwargs=request_kwargs)
    else:
        raise ValueError("Unknown uri scheme {}".format(uri_string))
