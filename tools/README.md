# Transform Tool
In the case where you have a JSON file or files for a pre-existing endpoint in Kong (service, route or plugin). This tool will read the existing JSON and transform it, meaning it will remove specific keys from the JSON that relate to a live endpoint, such as ID's, dates/times and so on, as presented by the Kong Admin API.

In doing the above, it means you can easily backup existing endpoints and use the transformed JSON to create the endpoints in another Kong instance if required.

```
Usage:
./transform.py --route-transform <input_filename> <output_filename>
./transform.py --service-transform <input_filename> <output_filename>
./transform.py --plugin-transform <input_filename> <output_filename>

Note: In the case of 'plugin-transform' the output_filename is prepended with the name of the plugin you're transforming. If multiple plugins exist, multiple prepended files will be output.