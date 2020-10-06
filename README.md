# lambda-elasticsearch-index-rotation
Automatically delete older indics on AWS Elasticsearch.


## Environment
- Python 3
- Lambda function and execution role
- Make sure the Lambda role has been added in AWS Elasticsearch's allow list on the access policy
- Cloudwatch Event Rule



## Build
```bash
$ pip install -r requirements.txt -t ./
$ zip -r artifact.zip ./*
```


## Parameters (Configure on Cloudwatch Event)
- endpoint (string)
    - The endpoint of AWS Elasticsearch with "https://" and without "/" on the suffix.
- region (string)
    - The region of AWS Elasticsearch.
- older_than (int)
    - The rotation days of index.
- exclude (list)
    - The keyword contains in index names which will not be deleted.


Example
```json
{
    "endpoint":"https://search-test-es-wrr22fsafafwe2.ap-northeast-1.es.amazonaws.com", 
    "region": "ap-northeast-1", 
    "older_than": "1",
    "exclude": ["testapi", "testaudit"]
},
{
    "endpoint":"https://searchwewqewqewqewqewqefwe2.ap-northeast-1.es.amazonaws.com", 
    "region": "us-west-1", 
    "older_than": "1",
    "exclude": [""]
}
```


## TODO
- Terraform