import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401

''' IMPORTS '''
import traceback

import requests

'''CONSTANTS'''
BitSight_date_time_format = '%Y-%m-%d'

# Disable insecure warnings
requests.packages.urllib3.disable_warnings()


class Client(BaseClient):
    """
    Client will implement the service API, should not contain Cortex XSOAR logic.
    Should do requests and return data
    """

    def http_request(self, method, url_suffix, params=None, data=None):
        full_url = self._base_url + url_suffix

        res = requests.request(
            method,
            full_url,
            verify=self._verify,
            params=params,
            json=data,
            auth=self._auth
        )
        return res

    def get_companies_guid(self):
        uri = 'v1/companies'
        return self.http_request(
            method='GET',
            url_suffix=uri
        )

    def get_company_detail(self, guid):
        uri = f'v1/companies/{encode_string_results(guid)}'
        return self.http_request(
            method='GET',
            url_suffix=uri
        )

    def get_company_findings(self, guid, first_seen, last_seen, severity_gte, grade_gt, asset_category, risk_vector):
        uri = f'v1/companies/{encode_string_results(guid)}/findings'

        params = {
            'first_seen_gte': first_seen,
            'last_seen_lte': last_seen
        }

        if severity_gte:
            params['severity_gte'] = severity_gte

        if grade_gt:
            params['details.grade'] = grade_gt

        if asset_category:
            params['assets.category'] = asset_category

        if risk_vector:
            params['risk_vector'] = risk_vector

        return self.http_request(
            method='GET',
            url_suffix=uri,
            params=params
        )

    # def get_company_alerts(self, first_seen, last_seen, alert_severity, alert_type):
    #     uri = 'v2/alerts'
    #
    #     params = {
    #         'first_seen_gte': first_seen,
    #         'last_seen_lte': last_seen,
    #         'severity': alert_severity,
    #         'alert_type': alert_type
    #     }
    #     return self.http_request(
    #         method='GET',
    #         url_suffix=uri,
    #         params=params
    #     )


'''HELPER FUNCTIONS'''


class OutputContext_Details:
    """
        Class to build a generic output and context.
    """

    def __init__(self, errorCode=None, errorMessage=None, ratingDetails=None, guid=None, customId=None, name=None,
                 description=None, ipv4Count=None, peopleCount=None, shortName=None, industry=None, industrySlug=None,
                 subIndustry=None, subIndustrySlug=None, homePage=None, primaryDomain=None, type=None, displayURL=None,
                 ratings=None, searchCount=None, subscriptionType=None, sparkline=None, subscriptionTypeKey=None,
                 subscriptionEndDate=None, bulkEmailSenderStatus=None, serviceProvider=None,
                 customerMonitoringCount=None, availableUpgradeTypes=None, hasCompanyTree=None,
                 hasPreferredContact=None, isBundle=None, ratingIndustryMedian=None, primaryCompany=None,
                 permissions=None, isPrimary=None, securityGrade=None, inSpmPortfolio=None, isMycompMysubsBundle=None,
                 companyFeatures=None):
        self.command = demisto.command().replace('-', '_').title().replace('_', '')
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        self.guid = guid
        self.customId = customId
        self.name = name
        self.description = description
        self.ipv4Count = ipv4Count
        self.peopleCount = peopleCount
        self.shortName = shortName
        self.industry = industry
        self.industrySlug = industrySlug
        self.subIndustry = subIndustry
        self.subIndustrySlug = subIndustrySlug
        self.homePage = homePage
        self.primaryDomain = primaryDomain
        self.type = type
        self.displayURL = displayURL
        self.ratingDetails = ratingDetails
        self.ratings = ratings
        self.searchCount = searchCount
        self.subscriptionType = subscriptionType
        self.sparkline = sparkline
        self.subscriptionTypeKey = subscriptionTypeKey
        self.subscriptionEndDate = subscriptionEndDate
        self.bulkEmailSenderStatus = bulkEmailSenderStatus
        self.serviceProvider = serviceProvider
        self.customerMonitoringCount = customerMonitoringCount
        self.availableUpgradeTypes = availableUpgradeTypes
        self.hasCompanyTree = hasCompanyTree
        self.hasPreferredContact = hasPreferredContact
        self.isBundle = isBundle
        self.ratingIndustryMedian = ratingIndustryMedian
        self.primaryCompany = primaryCompany
        self.permissions = permissions
        self.isPrimary = isPrimary
        self.securityGrade = securityGrade
        self.inSpmPortfolio = inSpmPortfolio
        self.isMycompMysubsBundle = isMycompMysubsBundle
        self.companyFeatures = companyFeatures
        self.data = {
            "errorCode": errorCode,
            "errorMessage": errorMessage,
            "guid": guid,
            "customId": customId,
            "name": name,
            "description": description,
            "ipv4Count": ipv4Count,
            "peopleCount": peopleCount,
            "shortName": shortName,
            "industry": industry,
            "industrySlug": industrySlug,
            "subIndustry": subIndustry,
            "subIndustrySlug": subIndustrySlug,
            "homePage": homePage,
            "primaryDomain": primaryDomain,
            "type": type,
            "displayURL": displayURL,
            "ratingDetails": ratingDetails,
            "ratings": ratings,
            "searchCount": searchCount,
            "subscriptionType": subscriptionType,
            "sparkline": sparkline,
            "subscriptionTypeKey": subscriptionTypeKey,
            "subscriptionEndDate": subscriptionEndDate,
            "bulkEmailSenderStatus": bulkEmailSenderStatus,
            "serviceProvider": serviceProvider,
            "customerMonitoringCount": customerMonitoringCount,
            "availableUpgradeTypes": availableUpgradeTypes,
            "hasCompanyTree": hasCompanyTree,
            "hasPreferredContact": hasPreferredContact,
            "isBundle": isBundle,
            "ratingIndustryMedian": ratingIndustryMedian,
            "primaryCompany": primaryCompany,
            "permissions": permissions,
            "isPrimary": isPrimary,
            "securityGrade": securityGrade,
            "inSpmPortfolio": inSpmPortfolio,
            "isMycompMysubsBundle": isMycompMysubsBundle,
            "companyFeatures": companyFeatures
        }


class OutputContext_Findngs:
    """
        Class to build a generic output and context.
    """

    def __init__(self, errorCode=None, errorMessage=None, temporaryId=None, affectsRating=None, assets=None,
                 details=None, evidenceKey=None, firstSeen=None, lastSeen=None, relatedFindings=None, riskCategory=None,
                 riskVector=None, riskVectorLabel=None, rolledupObservationId=None, severity=None,
                 severityCategory=None, tags=None, duration=None, comments=None, remainingDecay=None):
        self.command = demisto.command().replace('-', '_').title().replace('_', '')
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        self.temporaryId = temporaryId
        self.affectsRating = affectsRating
        self.assets = assets
        self.details = details
        self.evidenceKey = evidenceKey
        self.firstSeen = firstSeen
        self.lastSeen = lastSeen
        self.relatedFindings = relatedFindings
        self.riskCategory = riskCategory
        self.riskVector = riskVector
        self.riskVectorLabel = riskVectorLabel
        self.rolledupObservationId = rolledupObservationId
        self.severity = severity
        self.severityCategory = severityCategory
        self.tags = tags
        self.duration = duration
        self.comments = comments
        self.remainingDecay = remainingDecay
        self.data = {
            "errorCode": errorCode,
            "errorMessage": errorMessage,
            "temporaryId": temporaryId,
            "affectsRating": affectsRating,
            "assets": assets,
            "details": details,
            "evidenceKey": evidenceKey,
            "firstSeen": firstSeen,
            "lastSeen": lastSeen,
            "relatedFindings": relatedFindings,
            "riskCategory": riskCategory,
            "riskVector": riskVector,
            "riskVectorLabel": riskVectorLabel,
            "rolledupObservationId": rolledupObservationId,
            "severity": severity,
            "severityCategory": severityCategory,
            "tags": tags,
            "duration": duration,
            "comments": comments,
            "remainingDecay": remainingDecay
        }


class OutputContext_Guid:
    """
        Class to build a generic output and context.
    """

    def __init__(self, companyName=None, shortName=None, guid=None, errorCode=None,
                 errorMessage=None):
        self.command = demisto.command().replace('-', '_').title().replace('_', '')
        self.companyName = companyName
        self.shortName = shortName
        self.guid = guid
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        self.data = {
            "companyName": companyName,
            "shortName": shortName,
            "guid": guid,
            "errorCode": errorCode,
            "errorMessage": errorMessage
        }


def get_time_elapsed(fetch_time, last_run, first_fetch):
    today = datetime.today()
    now = datetime.now()
    if 'time' in last_run:
        # Get Last run and parse to date format. Bitsight report will be pulled from last run date to Yesterday's date
        last_run_time = last_run['time']
        last_run = datetime.strptime(last_run_time, '%Y-%m-%dT%H:%M:%SZ')
        last_run_time = last_run.strftime(BitSight_date_time_format)
        time_elapsed_in_minutes = (now - last_run).total_seconds() / 60
    else:
        # If last run time is not set, data will be pulled using fetch_time
        # i.e. last 10min if fetch events is set to 10min
        last_run_time = (today - timedelta(days=first_fetch)).strftime(
            BitSight_date_time_format)
        time_elapsed_in_minutes = fetch_time

    return time_elapsed_in_minutes, last_run_time


'''COMMAND FUNCTIONS'''


def fetch_incidents(client, last_run, params):
    events = []
    minuets_in_day = 1440

    try:
        # If there is no fetch time configured, it will be set to 0 and no events will be pulled
        first_fetch = int(params.get('first_fetch', 1))
        fetch_time = params.get('fetch_time', '00:01')
        current_time = datetime.now().strftime('%H:%M')
        time_elapsed_in_minutes, last_run_date = get_time_elapsed(minuets_in_day, last_run, first_fetch)

        if (time_elapsed_in_minutes >= minuets_in_day) and (current_time >= fetch_time):
            report_entries = []
            findings_res = get_company_findings_command(client, params, last_run_date, True)
            report_entries.extend(findings_res['results'])

            # Commenting below two lines since Alerts are need not to be fetched as incidets
            # alerts_res = get_company_alerts_command(client, params, last_run_date)
            # report_entries.extend(alerts_res['results'])
            for entry in report_entries:
                # Set the Raw JSON to the event. Mapping will be done at the classification and mapping
                event = {
                    "name": "BitSight",
                    "rawJSON": json.dumps(entry)}
                events.append(event)
            last_run_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

            last_run = {'time': last_run_time}
    except Exception as e:
        demisto.error('Failed to fetch events.')
        raise e

    return last_run, events


def test_module(client):
    """
    Returning 'ok' indicates that the integration works like it is supposed to. Connection to the service is successful.
    Anything else will fail the test.
    """
    res = client.get_companies_guid()
    if res.status_code == 200:
        return 'ok', None, None
    else:
        res_json = res.json()
        error_response = res_json.get('detail')
        raise Exception(f"Failed to execute test_module. Error Code: {res.status_code}.Error "
                        f"Response: {error_response}")


def get_companies_guid_command(client):
    generic_iam_context_data_list = []
    res = client.get_companies_guid()

    if res.status_code == 200:
        res_json = res.json()
        generic_iam_context = OutputContext_Guid(companyName='my_company',
                                                 shortName='my_company',
                                                 guid=res_json['my_company']['guid'])
        generic_iam_context_data_list.append(generic_iam_context.data)
        companies_list = res_json.get('companies')
        for company in companies_list:
            generic_iam_context = OutputContext_Guid(companyName=company['name'],
                                                     shortName=company['shortname'],
                                                     guid=company['guid'])
            generic_iam_context_data_list.append(generic_iam_context.data)
    else:
        res_json = res.json()
        generic_iam_context = OutputContext_Guid(errorCode=res.status_code,
                                                 errorMessage=res_json)
        generic_iam_context_data_list.append(generic_iam_context.data)

    generic_iam_context_dt = f'{generic_iam_context.command}(val.id == obj.id && val.instanceName == obj.instanceName)'

    outputs = {
        generic_iam_context_dt: generic_iam_context_data_list
    }

    readable_output = tableToMarkdown(name='Get Companies GUID:',
                                      t=generic_iam_context_data_list,
                                      headers=["companyName", "shortName", "guid", "errorCode", "errorMessage"],
                                      removeNull=True
                                      )
    return (
        readable_output,
        outputs,
        generic_iam_context_data_list
    )


def get_company_details_command(client, args):
    guid = args.get('guid')
    res = client.get_company_detail(guid)

    if res.status_code == 200:
        res_json = res.json()
        generic_iam_context = OutputContext_Details(guid=res_json.get('guid'),
                                                    customId=res_json.get('custom_id'),
                                                    name=res_json.get('name'),
                                                    description=res_json.get('description'),
                                                    ipv4Count=res_json.get('ipv4_count'),
                                                    peopleCount=res_json.get('people_count'),
                                                    shortName=res_json.get('shortname'),
                                                    industry=res_json.get('industry'),
                                                    industrySlug=res_json.get('industry_slug'),
                                                    subIndustry=res_json.get('sub_industry'),
                                                    subIndustrySlug=res_json.get('sub_industry_slug'),
                                                    homePage=res_json.get('homepage'),
                                                    primaryDomain=res_json.get('primary_domain'),
                                                    type=res_json.get('type'),
                                                    displayURL=res_json.get('display_url'),
                                                    ratingDetails=res_json.get('rating_details'),
                                                    ratings=res_json.get('ratings'),
                                                    searchCount=res_json.get('search_count'),
                                                    subscriptionType=res_json.get('subscription_type'),
                                                    sparkline=res_json.get('sparkline'),
                                                    subscriptionTypeKey=res_json.get('subscription_type_key'),
                                                    subscriptionEndDate=res_json.get('subscription_end_date'),
                                                    bulkEmailSenderStatus=res_json.get('bulk_email_sender_status'),
                                                    serviceProvider=res_json.get('service_provider'),
                                                    customerMonitoringCount=res_json.get('customer_monitoring_count'),
                                                    availableUpgradeTypes=res_json.get('available_upgrade_types'),
                                                    hasCompanyTree=res_json.get('has_company_tree'),
                                                    hasPreferredContact=res_json.get('has_preferred_contact'),
                                                    isBundle=res_json.get('is_bundle'),
                                                    ratingIndustryMedian=res_json.get('rating_industry_median'),
                                                    primaryCompany=res_json.get('primary_company'),
                                                    permissions=res_json.get('permissions'),
                                                    isPrimary=res_json.get('is_primary'),
                                                    securityGrade=res_json.get('security_grade'),
                                                    inSpmPortfolio=res_json.get('in_spm_portfolio'),
                                                    isMycompMysubsBundle=res_json.get('is_mycomp_mysubs_bundle'),
                                                    companyFeatures=res_json.get('company_features')
                                                    )
    else:
        res_json = res.json()
        generic_iam_context = OutputContext_Details(errorCode=res.status_code,
                                                    errorMessage=res_json)

    generic_iam_context_dt = f'{generic_iam_context.command}(val.id == obj.id && val.instanceName == obj.instanceName)'

    outputs = {
        generic_iam_context_dt: generic_iam_context.data
    }

    readable_output = tableToMarkdown(name='Get Company Details:',
                                      t=generic_iam_context.data,
                                      headers=["errorCode", "errorMessage", "guid", "customId", "name", "description",
                                               "ipv4Count", "peopleCount", "shortName", "industry", "industrySlug",
                                               "subIndustry", "subIndustrySlug", "homePage", "primaryDomain", "type",
                                               "displayURL", "ratingDetails", "ratings", "searchCount",
                                               "subscriptionType", "sparkline", "subscriptionTypeKey",
                                               "subscriptionEndDate", "bulkEmailSenderStatus", "serviceProvider",
                                               "customerMonitoringCount", "availableUpgradeTypes", "hasCompanyTree",
                                               "hasPreferredContact", "isBundle", "ratingIndustryMedian",
                                               "primaryCompany", "permissions", "isPrimary", "securityGrade",
                                               "inSpmPortfolio", "isMycompMysubsBundle", "companyFeatures"],
                                      removeNull=True
                                      )
    return (
        readable_output,
        outputs,
        generic_iam_context.data
    )


def get_company_findings_command(client, args, first_seen=None, fetch_incidents=False):
    if fetch_incidents:
        guid = args.get('guid', None)
        if not guid:
            res = client.get_companies_guid()
            if res.status_code == 200:
                res_json = res.json()
                guid = res_json.get('my_company')['guid']
            else:
                raise Exception('Unable to fetch GUID')
        severity = args.get('findings_min_severity', None)
        if severity:
            severity = severity.lower()
        grade = args.get('findings_grade', None)
        if type(grade) is list:
            grade = grade.join(',')
        asset_category = args.get('findings_asset_category', None)
        if asset_category:
            asset_category = asset_category.lower()
        risk_vector_list = args.get('risk_vector')
        if not isinstance(risk_vector_list, list):
            risk_vector_list = risk_vector_list.split(',')
        first_seen = first_seen
        last_seen = (datetime.today() - timedelta(days=1)).strftime(BitSight_date_time_format)
    else:
        guid = args.get('guid')
        severity = args.get('severity', None)
        grade = args.get('grade', None)
        asset_category = args.get('asset_category', None)
        if severity:
            severity = severity.lower()
        if grade:
            grade = grade.lower()
        if asset_category:
            asset_category = asset_category.lower()
        risk_vector_list = args.get('risk_vector_label', None)
        if risk_vector_list:
            risk_vector_list = risk_vector_list.split(',')
        else:
            risk_vector_list = []
        first_seen = args.get('first_seen')
        last_seen = args.get('last_seen')

    severity_mapping = {
        'minor': 1,
        'moderate': 2,
        'material': 3,
        'severe': 4
    }

    asset_category_mapping = {
        'low': 'low,medium,high,critical',
        'medium': 'medium,high,critical',
        'high': 'high,critical',
        'critical': 'critical'
    }

    risk_vector_mapping = {
        'web application headers': 'application_security',
        'botnet infections': 'botnet_infections',
        'breaches': 'data_breaches',
        'desktop software': 'desktop_software',
        'dkim': 'dkim',
        'dnssec': 'dnssec',
        'file sharing': 'file_sharing',
        'insecure systems': 'insecure_systems',
        'malware servers': 'malware_servers',
        'mobile app publications': 'mobile_app_publications',
        'mobile application security': 'mobile_application_security',
        'mobile software': 'mobile_software',
        'open ports': 'open_ports',
        'patching cadence': 'patching_cadence',
        'potentially exploited': 'potentially_exploited',
        'server software': 'server_software',
        'spam propagation': 'spam_propagation',
        'spf': 'SPF',
        'ssl certificates': 'ssl_certificates',
        'ssl configurations': 'ssl_configurations',
        'unsolicited communications': 'unsolicited_comm'
    }

    risk_vector = ''
    for vector in risk_vector_list:
        risk_vector += risk_vector_mapping[vector.lower()] + ','

    risk_vector = risk_vector[:-1]

    severity_gte = None
    if severity:
        severity_gte = severity_mapping[severity]

    asset_category_eq = None
    if asset_category:
        asset_category_eq = asset_category_mapping[asset_category]

    res = client.get_company_findings(guid, first_seen, last_seen, severity_gte, grade, asset_category_eq,
                                      risk_vector)

    if not fetch_incidents:
        generic_iam_context_data_list = []
        if res.status_code == 200:
            res_json = res.json()

            results = res_json.get('results')
            if results:
                for result in results:
                    generic_iam_context = OutputContext_Findngs(temporaryId=result.get('temporary_id'),
                                                                affectsRating=result.get('affects_rating'),
                                                                assets=result.get('assets'),
                                                                details=result.get('details'),
                                                                evidenceKey=result.get('evidence_key'),
                                                                firstSeen=result.get('first_seen'),
                                                                lastSeen=result.get('last_seen'),
                                                                relatedFindings=result.get('related_findings'),
                                                                riskCategory=result.get('risk_category'),
                                                                riskVector=result.get('risk_vector'),
                                                                riskVectorLabel=result.get('risk_vector_label'),
                                                                rolledupObservationId=result.get(
                                                                    'rolledup_observation_id'),
                                                                severity=result.get('severity'),
                                                                severityCategory=result.get('severity_category'),
                                                                tags=result.get('tags'),
                                                                duration=result.get('duration'),
                                                                comments=result.get('comments'),
                                                                remainingDecay=result.get('remaining_decay'),
                                                                )
                    generic_iam_context_data_list.append(generic_iam_context.data)
            else:
                generic_iam_context = OutputContext_Findngs()
                generic_iam_context_data_list.append(generic_iam_context.data)

        else:
            res_json = res.json()
            generic_iam_context = OutputContext_Findngs(errorCode=res.status_code,
                                                        errorMessage=res_json)
            generic_iam_context_data_list.append(generic_iam_context.data)

        generic_iam_context_dt = f'{generic_iam_context.command}(val.id == obj.id && val.instanceName == obj.instanceName)'

        outputs = {
            generic_iam_context_dt: generic_iam_context_data_list
        }

        readable_output = tableToMarkdown(name='Get Company findings:',
                                          t=generic_iam_context_data_list,
                                          headers=["errorCode", "errorMessage", "temporaryId", "affectsRating",
                                                   "assets", "details", "evidenceKey", "firstSeen", "lastSeen",
                                                   "relatedFindings", "riskCategory", "riskVector", "riskVectorLabel",
                                                   "rolledupObservationId", "severity", "severityCategory", "tags",
                                                   "duration", "comments", "remainingDecay"],
                                          removeNull=True
                                          )
        return (
            readable_output,
            outputs,
            generic_iam_context_data_list
        )
    else:
        return res.json()


# def get_company_alerts_command(client, args, first_seen):
#     alert_severity_list = args.get('alert_severity')
#     alert_type_list = args.get('alert_type')
#     last_seen = (datetime.today() - timedelta(days=1)).strftime(BitSight_date_time_format)
#
#     if isinstance(alert_severity_list, list):
#         alert_severity = ''
#         for severity in alert_severity_list:
#             alert_severity += severity + ','
#         alert_severity = alert_severity[:-1]
#     else:
#         alert_severity = alert_severity_list
#
#     if isinstance(alert_type_list, list):
#         alert_type = ''
#         for type in alert_type_list:
#             alert_type += type + ','
#         alert_type = alert_type[:-1]
#     else:
#         alert_type = alert_type_list
#
#     res = client.get_company_alerts(first_seen, last_seen, alert_severity, alert_type)
#
#     return res.json()


def main():
    command = demisto.command()
    params = demisto.params()
    """
        PARSE AND VALIDATE INTEGRATION PARAMS
    """
    base_url = params.get('url')
    verify_certificate = not params.get('insecure', False)
    proxy = params.get('proxy', False)
    api_key = params.get('apikey', {})

    LOG(f'Command being called is {command}')

    # commands = {
    #     'test-module': test_module,
    #     'bitsight-get-companies-guid': get_companies_guid_command,
    #     'bitsight-get-company-details': get_company_details_command,
    #     'bitsight-get-company-findings': get_company_findings_command
    # }

    client = Client(
        base_url=base_url,
        verify=verify_certificate,
        proxy=proxy,
        ok_codes=(200),
        auth=requests.auth.HTTPBasicAuth(api_key, '')
    )

    try:
        '''EXECUTION CODE'''
        # if command == 'bitsight-get-company-details' or command == 'bitsight-get-company-findings':
        #     human_readable, outputs, raw_response = commands[command](client, demisto.args())
        #     return_outputs(readable_output=human_readable, outputs=outputs, raw_response=raw_response)
        # elif command == 'bitsight-get-companies-guid' or command == 'test-module':
        #     human_readable, outputs, raw_response = commands[command](client)
        #     return_outputs(readable_output=human_readable, outputs=outputs, raw_response=raw_response)

        if command == 'bitsight-get-company-details':
            human_readable, outputs, raw_response = get_company_details_command(client, demisto.args())
            return_outputs(readable_output=human_readable, outputs=outputs, raw_response=raw_response)
        elif command == 'bitsight-get-company-findings':
            human_readable, outputs, raw_response = get_company_findings_command(client, demisto.args())
            return_outputs(readable_output=human_readable, outputs=outputs, raw_response=raw_response)
        elif command == 'test-module':
            human_readable, outputs, raw_response = test_module(client)
            return_outputs(readable_output=human_readable, outputs=outputs, raw_response=raw_response)
        elif command == 'bitsight-get-companies-guid':
            human_readable, outputs, raw_response = get_companies_guid_command(client)
            return_outputs(readable_output=human_readable, outputs=outputs, raw_response=raw_response)
        elif command == 'fetch-incidents':
            last_run = demisto.getLastRun()

            last_run_curr, events = fetch_incidents(client, last_run, params)

            if last_run != last_run_curr:
                demisto.setLastRun({'time': last_run_curr['time']})
                demisto.incidents(events)
            else:
                demisto.incidents([])

    # Log exceptions
    except Exception:
        return_error(f'Failed to execute {demisto.command()} command. Traceback: {traceback.format_exc()}')


if __name__ in ['__main__', 'builtin', 'builtins']:
    main()
