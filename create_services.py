#!/usr/bin/env python
import sys
import requests
import chardet
import argparse
import csv


def exit_program():
    """ Exit program """
    print("Goodbye!")
    sys.exit()


def ask_user_to_confirm(field_name, row):
    """ While loop asking user to confirm continuing or exiting """
    while True:
        user_input = ask_question(f"Regarding row: \n{row}\n{field_name} is blank. Continue? [Y/N] --> ")
        answer = user_input.upper()
        if answer == "Y":
            print(f"Your response: {answer}\n")
            break
        elif answer == "N":
            print(f"Your response: {answer}")
            exit_program()
        else:
            print("\nInvalid response, please try again\n")
    return answer


def ask_question(prompt):
    """ One function for user input """
    answer = input(prompt)
    return answer


def read_rows(args):
    """ Read the rows in CSV file """
    key = args.api_key
    filename = args.filename
    file_data = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not row["type"]:
                    ask_user_to_confirm("Type", row)
                elif not row["name"]:
                    ask_user_to_confirm("Name", row)
                elif not row["description"]:
                    ask_user_to_confirm("Description", row)
                elif not row["auto_resolve_timeout"]:
                    ask_user_to_confirm("Auto Resolve Timeout", row)
                elif not row["escalation_policy.id"]:
                    ask_user_to_confirm("Escalation Policy ID", row)
                elif not row["escalation_policy.type"]:
                    ask_user_to_confirm("Escalation Policy Type", row)
                try:
                    service_dict = {"service": {"type": row["type"], "name": row["name"],
                                                "description": row["description"],
                                                "auto_resolve_timeout": row["auto_resolve_timeout"],
                                                "escalation_policy": {"id": row["escalation_policy.id"],
                                                                      "type": row["escalation_policy.type"]}}}
                    file_data.append(service_dict)
                except KeyError as err:
                    print(f'Missing column in file: {err}')

    except KeyError as err:
        print(f"CSV file is required, error: {err}")
    import_services(key, file_data)


def import_services(key, file_data):
    """ Import services from CSV file """
    url = 'https://api.pagerduty.com/services'
    headers = {'Accept': 'application/vnd.pagerduty+json;version=2',
               'Content-Type': 'application/json',
               'Authorization': f'Token token={key}'}
    for row in file_data:
        payload = row
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 201:
                print(f'Statuscode: {response.status_code}, the following was imported successfully: \n{payload}\n')
            response_dict = response.json()
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if response.status_code == 400:
                print(f'Statuscode: {response.status_code}, the following was NOT imported: \n{payload}\n'
                      f'Caller provided invalid arguments. Retrying with the same arguments will not work, {err}\n')
            elif response.status_code == 401:
                print(f'Statuscode: {response.status_code}, the following was NOT imported: \n{payload}\n'
                      f'Caller did not supply credentials or did not provide the correct credentials. '
                      f'If you are using an API key, it may be invalid or your Authorization header '
                      f'may be malformed, {err}\n')
            elif response.status_code == 402:
                print(f'Statuscode: {response.status_code}, the following was NOT imported: \n{payload}\n'
                      f'Account does not have the abilities to perform the action. '
                      f'You can also use the Abilities API to determine what features are available to your account, '
                      f'{err}\n')
            elif response.status_code == 403:
                print(f'Statuscode: {response.status_code}, the following was NOT imported: \n{payload}\n'
                      f'Caller is not authorized to view the requested resource. '
                      f'While your authentication is valid, the authenticated user or token does not have '
                      f'permission to perform this action, {err}\n')
        except requests.exceptions.ConnectionError as err:
            print(f'A Connection error occurred, {err}')
        except requests.exceptions.Timeout as err:
            print(f'The request timed out, {err}')
        except requests.exceptions.RequestException as err:
            print(f'There was an ambiguous exception that occurred while handling your request, {err}')


def main():
    """ Grab the API key and file name from script execution """
    parser = argparse.ArgumentParser(description='Bulk import of services from CSV file')
    parser.add_argument('-k', '--api-key', required=True, help='Global REST API key')
    parser.add_argument('-f', '--filename', required=True, help='CSV file of services to import')
    args = parser.parse_args()
    read_rows(args)


if __name__ == '__main__':
    main()
