import requests
from exceptions import *
from requests import Response


class OpenOpusAPI(object):
    def __init__(self):
        self.base_url = "https://api.openopus.org"

    def get_composers_by_name(self, name: str) -> str:

        """

        * Sends a GET request to the API to retrieve composers by their names 
        * and returns a formatted String containing their basic info.
        * Checks the status code of the HTTP response received from the server
        * and raises an HTTPError exception when appropriate.

        """

        url = f"{self.base_url}/dyn/composer/list/search/{name.lower()}.json"
        response = requests.get(url)
        response.raise_for_status()
        json = response.json()
        composers_string = ""
        try: 
            for composer in json["composers"]:
                if composer["death"] == None:
                    composer["death"] = "Present"
                composers_string += f"Name of composer: {composer['complete_name']} ({composer['birth']} -> {composer['death']})\nBest known epoch: {composer['epoch']}\n"
        except KeyError:
            raise ComposerMissingError("Missing required composer data in the API response.")
        return composers_string

    def get_popular(self, epoch: str = "", n: int = 10) -> list:

        """

        * Sends a GET request to the API to get a list of the n most popular composers.
        * By default, n is set to 10.

        """
        
        if n < 0:
            class InvalidLengthError(Exception):
                pass
            raise InvalidLengthError("Invalid length! Length cannot be a negative number.")
        if (epoch == ""):
            url = f"{self.base_url}/dyn/composer/list/pop.json"
        else:
            url = f"{self.base_url}/dyn/composer/list/epoch/{epoch}.json"     
        try:
            response = requests.get(url)
            response.raise_for_status
            composers_list = response.json()["composers"]
            return [composers_list[i]["complete_name"] for i in range(n)]
        except IndexError:
            raise RequestedTooManyComposersError(f"There are only {len(composers_list)} most popular composers in the API response, not {n}.")
        except KeyError:
            raise InvalidEpoch(f"'{epoch}' is not a valid epoch in the API.")       
        
api = OpenOpusAPI()
print(api.get_popular("Rom"))
