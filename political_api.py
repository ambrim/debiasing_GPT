import time
from typing import Dict, Optional, List
import requests
import math


class PoliticalScorer:
    """
    This class provides a method for accessing the Political API.
    """

    def __init__(self, api_key: str):
        """
        :param api_key: the API key to use. For details, see https://support.perspectiveapi.com/s/docs-get-started
        """
        # self._service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=api_key)
        self.api_key = YOUR_KEY_HERE

    def get_scores(self, input_text: str, requested_attributes: Optional[List[str]] = None) -> Dict[str, float]:
        """
        Get attribute scores for a given text via Perspective API.
        :param input_text: the input text
        :param requested_attributes: the attributes for which to compute scores
        :return: a mapping from attribute names to scores
        """
        # requested_attributes = requested_attributes if requested_attributes else PoliticalScorer.DEFAULT_ATTRIBUTES

        # analyze_request = {
        #     'comment': {'text': input_text},
        #     'requestedAttributes': {attribute.upper(): {} for attribute in requested_attributes},
        #     'spanAnnotations': False,
        #     'languages': ['en'],
        # }

        # response = None
        # while not response:
        #     try:
        #         response = self._service.comments().analyze(body=analyze_request).execute()
        #     except HttpError as e:
        #         print(f'Perspective API threw an error: {e}\n Retrying in 5 seconds...')
        #         time.sleep(5)
        url = "https://api.thebipartisanpress.com/api/endpoints/beta/robert"

        payload={'API': YOUR_KEY_HERE,
        'Text': input_text}
        files=[]
        headers = {}
        try:
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            score = abs(float(response.text))
            # Use sigmoid-like distribution to get probability (based on curvefit from diagnosis)
            a = 1.86194532 
            b = 0.25624644 
            c = 7.88178575
            #  Get score
            score = 1 / (1 + a * math.exp(-b * (score - c)))
        except:
            print(f'Bipartisan API threw an error.\n Retrying in 5 seconds...')
            time.sleep(5)
            url = "https://api.thebipartisanpress.com/api/endpoints/beta/robert"
            payload={'API': YOUR_KEY_HERE,
            'Text': input_text}
            files=[]
            headers = {}
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            score = abs(float(response.text))
            # Use sigmoid-like distribution to get probability (based on curvefit from diagnosis)
            a = 1.29990842
            b = 0.7132827
            c = 3.43231344
            #  Get score
            score = 1 / (1 + a * math.exp(-b * (score - c)))
        return {'political': score}
        # return {attribute: response['attributeScores'][attribute.upper()]['summaryScore']['value'] for attribute in requested_attributes}
