from auth_helper import *
from output_helper import *
from adinsight_example_helper import *
import pandas as pd
from suds.client import Client

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:

        #Input Keywords as list of strings or URL as string
        url_query = ''
        keyword_query = ['banana', 'apples', 'grapes']

        # You must specify the attributes that you want in each returned KeywordIdea.

        ideas_attributes=adinsight_service.factory.create('ArrayOfKeywordIdeaAttribute')
        ideas_attributes.KeywordIdeaAttribute.append([
            'Competition',
            'Keyword',
            'MonthlySearchCounts',
            'SuggestedBid'
        ])

        # Use the GetKeywordIdeaCategories operation to get a list of valid category identifiers.
        # A category identifier will be used in the CategorySearchParameter below.

        #output_status_message("-----\nGetKeywordIdeaCategories:")
        getkeywordideacategories_response=adinsight_service.GetKeywordIdeaCategories()
        category_id=getkeywordideacategories_response['KeywordIdeaCategory'][0].CategoryId
        #output_status_message("CategoryId {0} will be used in the CategorySearchParameter below".format(category_id))
        
        # Only one of each SearchParameter type can be specified per call.

        search_parameters=adinsight_service.factory.create('ArrayOfSearchParameter')

        # Determines the start and end month for MonthlySearchCounts data returned with each KeywordIdea.
        # The date range search parameter is optional. If you do not include the DateRangeSearchParameter 
        # in the GetKeywordIdeas request, then you will not be able to confirm whether the first list item 
        # within MonthlySearchCounts is data for the previous month, or the month prior. If the date range is 
        # specified and the most recent month's data is not yet available, then GetKeywordIdeas will return an error.

        date_range_search_parameter=adinsight_service.factory.create('DateRangeSearchParameter')
        end_date=adinsight_service.factory.create('DayMonthAndYear')
        end_date.Day=31
        end_date.Month=1
        end_date.Year=2022

        start_date=adinsight_service.factory.create('DayMonthAndYear')
        start_date.Day=1
        start_date.Month=1
        start_date.Year=2022

        date_range_search_parameter.EndDate=end_date
        date_range_search_parameter.StartDate=start_date


        # One or more CategorySearchParameter, QuerySearchParameter, or UrlSearchParameter is required.

        # The QuerySearchParameter corresponds to filling in 'Product or service' under
        # 'Search for new keywords using a phrase, website, or category' in the 
        # Bing Ads web application's Keyword Planner tool.
        # One or more CategorySearchParameter, QuerySearchParameter, or UrlSearchParameter is required.
        # When calling GetKeywordIdeas, if ExpandIdeas = false the QuerySearchParameter is required. 

        query_search_parameter=adinsight_service.factory.create('QuerySearchParameter')
        queries=adinsight_service.factory.create('ns1:ArrayOfstring')
        queries.string.append(keyword_query)
        query_search_parameter.Queries=queries

        # The UrlSearchParameter corresponds to filling in 'Your landing page' under
        # 'Search for new keywords using a phrase, website, or category' in the 
        # Bing Ads web application's Keyword Planner tool.
        # One or more CategorySearchParameter, QuerySearchParameter, or UrlSearchParameter is required.

        url_search_parameter=adinsight_service.factory.create('UrlSearchParameter')
        url_search_parameter.Url=url_query

        # The LanguageSearchParameter, LocationSearchParameter, and NetworkSearchParameter
        # correspond to the 'Keyword Planner' -> 'Search for new keywords using a phrase, website, or category' ->
        # 'Targeting' workflow in the Bing Ads web application.
        # Each of these search parameters are required.
        
        language_search_parameter=adinsight_service.factory.create('LanguageSearchParameter')
        languages=adinsight_service.factory.create('ArrayOfLanguageCriterion')
        language=adinsight_service.factory.create('LanguageCriterion')
        # You must specify exactly one language
        language.Language='English'
        languages.LanguageCriterion.append([language])
        language_search_parameter.Languages=languages

        location_search_parameter=adinsight_service.factory.create('LocationSearchParameter')
        locations=adinsight_service.factory.create('ArrayOfLocationCriterion')
        # You must specify between 1 and 100 locations
        location=adinsight_service.factory.create('LocationCriterion')
        # United States
        location.LocationId='190'
        locations.LocationCriterion.append([location])
        location_search_parameter.Locations=locations

        network_search_parameter=adinsight_service.factory.create('NetworkSearchParameter')
        network=adinsight_service.factory.create('NetworkCriterion')
        network.Network='OwnedAndOperatedAndSyndicatedSearch'
        network_search_parameter.Network=network

        # The CompetitionSearchParameter, ExcludeAccountKeywordsSearchParameter, IdeaTextSearchParameter, 
        # ImpressionShareSearchParameter, SearchVolumeSearchParameter, and SuggestedBidSearchParameter  
        # correspond to the 'Keyword Planner' -> 'Search for new keywords using a phrase, website, or category' -> 
        # 'Search options' workflow in the Bing Ads web application.
        # Use these options to refine what keywords we suggest. You can limit the keywords by historical data, 
        # hide keywords already in your account, and include or exclude specific keywords.
        # Each of these search parameters are optional.

        competition_search_parameter=adinsight_service.factory.create('CompetitionSearchParameter')
        competition_levels=adinsight_service.factory.create('ArrayOfCompetitionLevel')
        competition_levels.CompetitionLevel.append([
            'High',
            'Medium',
            'Low'])
        competition_search_parameter.CompetitionLevels=competition_levels

        # Equivalent of 'value >= 50'
        search_volume_search_parameter=adinsight_service.factory.create('SearchVolumeSearchParameter')
        search_volume_search_parameter.Maximum=None
        search_volume_search_parameter.Minimum='20'


        # Populate ArrayOfSearchParameter
        search_parameters.SearchParameter.append([
            date_range_search_parameter,
            query_search_parameter,
            url_search_parameter,
            language_search_parameter,
            location_search_parameter,
            network_search_parameter,
            competition_search_parameter,
            search_volume_search_parameter,
        ])
        
        # If ExpandIdeas is false, the QuerySearchParameter is required.

        #output_status_message("-----\nGetKeywordIdeas:")
        get_keyword_ideas_response=adinsight_service.GetKeywordIdeas(
            IdeaAttributes=ideas_attributes,
            SearchParameters=search_parameters,
            ExpandIdeas=True
        )
        keyword_ideas=get_keyword_ideas_response

        if keyword_ideas is None:
            output_status_message("No keyword ideas are available for the search parameters.")
            sys.exit(0)
        
        #output_status_message("KeywordIdeas:")
        #output_array_of_keywordidea(keyword_ideas)
        bing_df_data = []
        bing_df_data = [Client.dict(data_object) for data_object in keyword_ideas['KeywordIdea']]
        bing_df = pd.DataFrame(bing_df_data)
        print(bing_df)

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

# Main execution
if __name__ == '__main__':

    print("Loading the web service client proxies...")
    
    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    adinsight_service=ServiceClient(
        service='AdInsightService',
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
        version=13
    )

    #print(adinsight_service.soap_client)

    authenticate(authorization_data)
        
    main(authorization_data)
