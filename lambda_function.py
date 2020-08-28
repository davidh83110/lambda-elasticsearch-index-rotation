from requests_aws4auth import AWS4Auth
import boto3
import requests
import datetime


def keep_suffix(older_than):
    today = datetime.date.today()
    keep_suffix = tuple((today - datetime.timedelta(days=o)).isoformat().replace('-', '.')
                            for o in range(0, older_than))

    return keep_suffix


def lambda_handler(event, context):

    endpoint = event.get('endpoint')
    print('The endpoint is: ', endpoint)

    region = event.get('region')
    print('The region is: ', region)

    older_than = int(event.get('older_than'))
    print('The indices older than the date will be deleted: ', older_than)

    exclude = event.get('exclude')
    print('The indices contain in the list will not be deleted: ', exclude)


    ## AWS Elasticsearch required signed requests.
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    res = requests.get(endpoint + "/_cat/indices", auth=awsauth)

    ## Use 'green' as beginning character of index informations to split.
    info_list = res.text.split('green')

    for info in info_list:
        if 'open' in info:
            index = info.split(' ')[2]
            index_time = index.split('-')[-1]

            ## Find index which older than "older_than" days and not starts with ".".
            if index_time not in keep_suffix(older_than) and not index.startswith('.'):

                for ex_index in exclude:
                    if ex_index not in index:
                        print('Going to delete index: ', index)

                        delete_res = requests.delete(endpoint+'/'+index, auth=awsauth)
                        print(delete_res)

    print('Older indices cleanup completed.')

    return 200