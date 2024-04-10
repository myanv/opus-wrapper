import requests
from requests import Response

class OpenOpusAPI(object):
    def __init__(self):
        self.base_url = "https://api.openopus.org"

    def get_composers_by_name(self, name):
        """
        * Retrieves composers by their names and returns a formatted String containing their basic info
        * Checks the status code of the HTTP response received from the server
        * and raises an HTTPError exception when appropriate.
        """
        url = f"{self.base_url}/dyn/composer/list/search/{name.lower()}.json"
        response = requests.get(url)
        response.raise_for_status()
        json = response.json()
        string = ""
        try: 
            for composer in json["composers"]:
                if composer["death"] == None:
                    composer["death"] = "Present"
                string += f"Name of composer: {composer['complete_name']} ({composer['birth']} -> {composer['death']})\nBest known epoch: {composer['epoch']}\n"
        except KeyError:
            class ComposerMissingError(Exception):
                pass
            raise ComposerMissingError("Missing required composer data in the API response.")
        return string
