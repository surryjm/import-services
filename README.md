# Import Services from CSV
This script will bulk import services from a CSV file. 

The script requires a full access API key (not read-only).

In addition, the corresponding escalation policies must already exist in your PagerDuty account.

Details regarding the PagerDuty REST API are in our Knowledge Base:

https://developer.pagerduty.com/api-reference/7062f2631b397-create-a-service

### Input Format:
To use this script, a CSV file is required with the following column headers in this format:

```csv
type,name,description,auto_resolve_timeout,escalation_policy.id,escalation_policy.type
```

In this format:
- The value for `type` should be `service` - *required*
- `name` is the name of the service - *required*
- `description` is the description of the service - value can be blank
- `auto_resolve_timeout` is the time in seconds that an incident is automatically resolved if left open for that long - value can be blank
- `escalation_policy.id` is the ID of the escalation policy to associate with the service. The ID is located at the end of the URL on the escalation policy page in question. As an example, the ID is `ABC1234` in the following URL: `https://mysubdomain.pagerduty.com/escalation_policies#ABC1234` - *required*
- The value for `escalation_policy.type` should be `escalation_policy_reference` - *required*

### Usage:
First, install dependencies (use `pip3` if `pip` does not work):
```csv
pip install -r requirements.txt
```
Then, to execute the script:
```csv
python3 create_services.py -k API_TOKEN -f PATH_TO_CSV_FILE
```

