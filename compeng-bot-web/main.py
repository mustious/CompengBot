def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    import random
    import dialogflow
    import string
    
    ## Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
    ## Allows GET requests from any origin with the Content-Type
        headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'}
        
        return ('', 204, headers)

    ## Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
        }

    request_json = request.get_json(force=True)

    project_id = request_json["project_id"]
    text = request_json["text"]
    language_code = request_json["lang"]

    string_len = random.randint(1, 10)
    string_list = [random.choice(string.ascii_lowercase) for i in range(0, string_len)]
    session_id = ''.join(string_list)

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    response_text = response.query_result.fulfillment_text

    return (response_text, 200, headers)