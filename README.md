# Introduction
I created Kong Tool to satisfy a requirement that a client had. Although there are other tools to manage Kong, I wanted to create something a little more bespoke for various reasons I won't go into here.

## What does this tool do?
This tool can be used to do the following:
- Create, amend, list and delete service endpoints
- Create, amend, list and delete routes
- Create, amend, list and delete plugins

## Compatibility
There are some small API differences between Kong 1.x and 2.x versions but I wanted it to be as compatible as possible. I have tested this with Kong 1.3 and Kong 2.0.

As a result of attempting to keep compatibility between the versions, I opted to use API endpoints/methods that were present in both the Kong 1.3 and Kong 2.0 API versions. This means that the code may not be as optimal as it could have been had I only wanted it to work with Kong 2.0.

## Requirements

This has been tested with Python 3.8.

## Usage
To get started, point this tool at Kong's admin API by editing `config.ini` to give it the correct URL to use.

You can list out the help documentation by running `./kongtool -h` which will give you a list of options.

When creating or amending resources in Kong, you'll need to present the Kong Tool with a JSON file to read and send as the payload to the API endpoint. I've put together a number of examples in the `templates_json` folder. So long as you follow the structure defined on the API page of the Kong API documentation, you should be good to go.

There is also JSON validation at the point of running the tool which should give you an error message if you make a mistake in your JSON file.

Adding a service endpoint is easy, see example below (example JSON in templates_json/service-example.json):

`./kongtool.py --create-service-endpoint example-service service-example.json`

Now, add a route to the service (example JSON in templates_json/route-example.json):

`./kongtool.py --add-route-to-service example-service route-example.json`

Optionally, if you wish to add a plugin to a service, you can do so by running the following (example JSON in templates_json/iprestriction-example.json):

`./kongtool.py --add-plugins example-service iprestriction-example.json`

## Other useful information
The Kong API documentation has been invaluable whilst creating this tool. You can find it below:

https://docs.konghq.com/2.0.x/admin-api/