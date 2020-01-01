import aiohttp
import requests
import json
from datetime import datetime

# class EarthEplorerClient():

#     def __init__(self):
#         pass


post_request = 'https://earthexplorer.usgs.gov/inventory/json/v/latest/login'

my_params = { 'jsonRequest':'{"username":"dmilewicz","password":"Spartan117RC1136##","authType":"EROS","catalogId":"EE"}'}
# my_params = { 'jsonRequest':'{username:dmilewicz,password:Spartan117RC1136!!,authType:EROS,catalogId:EE}'}
# my_params = {'jsonRequest':'dmilewicz'}

async def run_login():
    async with aiohttp.ClientSession() as session:
        async with session.post(post_request) as resp:
            print("here")
            print(resp)

_LAST_API_KEY_FILE = '.api_key'

_EE_DATE_STR_FORMAT = '%Y-%m-%d'


def build_request(requestData_dict):
    return {'jsonRequest': json.dumps(requestData_dict)}


class SpatialFilter():

    def __init__(self, lower_left=None, upper_right=None, point=None):

        if (lower_left or upper_right) and not (lower_left and upper_right):
            raise ValueError("Why only put upperleft or upperright?")

        self.lower_left = lower_left
        self.upper_right = upper_right

        if point:
            self.lower_left = point
            self.upper_right = point

    def to_dict(self):
        return {
            "filterType":"mbr",
            "lowerLeft": {
                "latitude": self.lower_left[0],
                "longitude": self.lower_left[1]
            },
            "upperRight":{
                "latitude": self.upper_right[0],
                "longitude": self.upper_right[1]
            }
        }

class TemporalFilter():

    def __init__(self, date=None, start_date=None, end_date=None):
        self.start_date = start_date
        self.end_date   = end_date

        if date:
            self.start_date = date
            self.end_date   = date

    def to_dict(self):
        return {
            'startDate': self.start_date.strftime(_EE_DATE_STR_FORMAT),
            'endDate'  : self.end_date.strftime(_EE_DATE_STR_FORMAT)
        }





class EarthClient():

    def __init__(self, version='latest'):

        self.api_key = None
        self.version = version

        # configure url
        self.__configure_base_url(version=self.version)

        self.username = None
        self.password = None

        self.authType = "EROS"

        self.history = []


    def __configure_base_url(self, version):
        url_base_start = 'https://earthexplorer.usgs.gov/inventory/json'

        self.url_base = "/".join([url_base_start, "v", version])
        print(self.url_base)
        return self.url_base

    def __logged_in(self):
        return self.api_key is not None

    def build_request(self, requestData_dict):
        if self.__logged_in():
            requestData_dict['apiKey'] = self.api_key
            return {'jsonRequest': json.dumps(requestData_dict)}

    def set_username(self, username):
        self.username = username

    def login(self, username=None, password=None, catalogId=None):

        if username is None:
            username = self.username

        if password is None:
            password = self.password

        if catalogId is None:
            catalogId = "EE"

        data_fields = {'jsonRequest': json.dumps({
            'username':  username,
            'password':  password,
            'authType':  self.authType,
            'catalogId': catalogId
        })}

        print(data_fields)

        response = requests.post(url=self.url_base + '/login', data=data_fields)

        self.history.append(response)

        if not response.ok:
            print("Error with login")
            return

        print(response.url)
        reply_json = response.json()
        print(reply_json)

        self.api_key = reply_json['data']
        print('API Key: {}'.format(self.api_key))

        with open(_LAST_API_KEY_FILE, 'w') as api_key_file:
            api_key_file.write(self.api_key)

        return True

    def search_dataset(self, datasetName, spatialFilter, temporalFilter):

        if not self.__logged_in():
            print("Error! Not logged in for search_dataset")
            return False

        dataset_search_dict = self.build_request({
            'datasetName': "",
            'spatialFilter': spatialFilter.to_dict(),
            'temporalFilter': temporalFilter.to_dict()
        })














def main():
    # run_login()


    ee = EarthClient()
    ee.login(username='dmilewicz', password='Spartan117RC1136##')

    sf = SpatialFilter()





if __name__ == "__main__":
    main()
