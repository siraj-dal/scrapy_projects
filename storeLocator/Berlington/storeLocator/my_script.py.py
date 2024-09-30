from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # This function is called for each request
    print(f"Request URL: {flow.request.url}")

def response(flow: http.HTTPFlow) -> None:
    # This function is called for each response
    if flow.request.url == "https://www.meesho.com/new-trendy-woman-kurti-with-dupatta/p/76hjbx":
        print(f"Response URL: {flow.request.url}")
        print(f"Response Status Code: {flow.response.status_code}")
        print(f"Response Text: {flow.response.text}")  # Print the response text
