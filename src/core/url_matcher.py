class UrlMatcher:

    def __init__(self, client_validation, global_validation):
        self.client_validation = client_validation
        self.global_validation = global_validation

    def match_url(self, url, client):

        return self.client_validation.get_match(client=client, url=url) or self.global_validation.get_match(url=url)
