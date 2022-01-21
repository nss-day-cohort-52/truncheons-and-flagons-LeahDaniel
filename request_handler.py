import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from stat import FILE_ATTRIBUTE_REPARSE_POINT
from teams import get_teams, get_all_players, get_all_team_scores


class HandleRequests(BaseHTTPRequestHandler):
    def parse_query_string_parameters(self, params):
        filters = {}
        pairs = params.split("&")
        for pair in pairs:
            [key, value] = pair.split("=")
            if key in filters:
                filters[key]['resources'].append(value)
            else:
                filters[key] = { 'resources': [value] }

        return filters

    def parse_url(self, path):
        id = None
        filters = None
        url_parts = path.split("/") # localhost:8088/customers/1  localhost:8088/customers?_embed=blah&_expand=blah
        url_parts.pop(0)

        resource = url_parts[0]
        if "?" in resource:
            [resource, params] =  resource.split("?")
            filters = self.parse_query_string_parameters(params)

        try:
            route_parameters = url_parts[1] #if grabbing a singular dictionary
            if "?" in route_parameters:
                [id, params] = route_parameters.split("?")
                id = int(id)
                filters = self.parse_query_string_parameters(params)
            else:
                try:
                    id = int(route_parameters)
                except IndexError:
                    pass  # No route parameter exists: /animals
                except ValueError:
                    pass  # Request had trailing slash: /animals/
        except IndexError:
            pass  # No route parameter exists

        return (resource, id, filters)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        response = {}
        
        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)
        
        if len(parsed) > 2:
            (resource, id, filters) = parsed
            if resource == "teams":
                response = f"{get_teams(filters)}"
            elif resource == "players":
                response = f"{get_all_players()}"
            elif resource == "teamscores":
                response = f"{get_all_team_scores()}"

        self.wfile.write(response.encode())


def main():
    host = ''
    port = int(os.environ['PORT'])
    HTTPServer((host, port), HandleRequests).serve_forever()


main()
