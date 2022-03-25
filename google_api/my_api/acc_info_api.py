#!/usr/bin/env python
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example lists information about an advertising account.

For example, its name, currency, time zone, etc.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

customer_id ="5651232347"

def main(client, customer_id):
    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT
            customer.id,
            customer.descriptive_name,
            customer.currency_code,
            customer.time_zone,
            customer.tracking_url_template,
            customer.auto_tagging_enabled
        FROM customer
        LIMIT 1"""

    request = client.get_type("SearchGoogleAdsRequest")
    request.customer_id = customer_id
    request.query = query
    response = ga_service.search(request=request)
    customer = list(response)[0].customer

    print(f"Customer ID: {customer.id}")
    print(f"\tDescriptive name: {customer.descriptive_name}")
    print(f"\tCurrency code: {customer.currency_code}")
    print(f"\tTime zone: {customer.time_zone}")
    print(f"\tTracking URL template: {customer.tracking_url_template}")
    print(f"\tAuto tagging enabled: {customer.auto_tagging_enabled}")


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage("/Users/erikstorjohann/capstone/capstone-project-tem-2/google_api/my_api/googleads.yaml")

    # parser = argparse.ArgumentParser(
    #     description=(
    #         "Displays basic information about the specified "
    #         "customer's advertising account."
    #     )
    # )
    # The following argument(s) should be provided to run the example.
    # parser.add_argument(
    #     "-c",
    #     "--customer_id",
    #     type=str,
    #     required=True,
    #     help="The Google Ads customer ID.",
    # )
    # args = parser.parse_args()

    try:
        main(googleads_client, customer_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)