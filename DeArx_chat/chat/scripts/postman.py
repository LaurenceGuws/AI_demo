import json
import requests

def run_postman_collection(collection):
    # Load the collection JSON
    collection_json = json.loads(collection)

    # Open the output file with utf-8 encoding
    with open("output.txt", "w", encoding="utf-8") as outfile:
        # Iterate over the items in the collection
        for item in collection_json["item"]:
            for request_item in item["item"]:
                # Extract the request details
                request = request_item["request"]
                method = request["method"]
                url = request["url"]["raw"]

                # Extract the request headers
                headers = {header["key"]: header["value"] for header in request.get("header", [])}

                # Extract the request body
                body = json.loads(request.get("body", {}).get("raw", "{}"))

                # Send the request
                response = requests.request(method, url, headers=headers, json=body)

                # Write the heading, request, response, and payload (if present) to the output file
                outfile.write(f"---- {request_item['name']} ----\n")
                outfile.write(f"Request: {method} {url}\n")
                if method == "POST":
                    outfile.write(f"Payload: {json.dumps(body, indent=4)}\n")
                outfile.write(f"Response: {response.status_code} {response.text}\n\n")

def main():
    # Your Postman collection JSON as a string
    collection = r"""
    {
        "info": {
            "_postman_id": "394e02c3-dab1-4640-8ed3-d2fd8cd2819e",
            "name": "Fask_DeArx_chat",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
            "_exporter_id": "20963231"
        },
        "item": [
            {
                "name": "POST",
                "item": [
                    {
                        "name": "send a message",
                        "request": {
                            "method": "POST",
                            "header": [],
                            "body": {
                                "mode": "raw",
                                "raw": "{\r\n    \"message\": {\r\n        \"content\": \"hi\"\r\n    }\r\n}\r\n",
                                "options": {
                                    "raw": {
                                        "language": "json"
                                    }
                                }
                            },
                            "url": {
                                "raw": "http://localhost:30000/message",
                                "protocol": "http",
                                "host": [
                                    "localhost"
                                ],
                                "port": "30000",
                                "path": [
                                    "message"
                                ]
                            }
                        },
                        "response": []
                    },
                    {
                        "name": "upload a file",
                        "request": {
                            "method": "POST",
                            "header": [],
                            "url": {
                                "raw": "http://localhost:30000/upload",
                                "protocol": "http",
                                "host": [
                                    "localhost"
                                ],
                                "port": "30000",
                                "path": [
                                    "upload"
                                ]
                            }
                        },
                        "response": []
                    },
                    {
                        "name": "change the active model",
                        "request": {
                            "method": "POST",
                            "header": [],
                            "body": {
                                "mode": "raw",
                                "raw": "{\r\n    \"model_name\": \"test\"\r\n}\r\n",
                                "options": {
                                    "raw": {
                                        "language": "json"
                                    }
                                }
                            },
                            "url": {
                                "raw": "http://localhost:30000/change_model",
                                "protocol": "http",
                                "host": [
                                    "localhost"
                                ],
                                "port": "30000",
                                "path": [
                                    "change_model"
                                ]
                            }
                        },
                        "response": []
                    },
                    {
                        "name": "save custom instructions",
                        "request": {
                            "method": "POST",
                            "header": [],
                            "body": {
                                "mode": "raw",
                                "raw": "{\r\n    \"example_request\": \"Your example request here\",\r\n    \"example_response\": \"Your example response here\"\r\n}",
                                "options": {
                                    "raw": {
                                        "language": "json"
                                    }
                                }
                            },
                            "url": {
                                "raw": "http://localhost:30000/custom_instructions",
                                "protocol": "http",
                                "host": [
                                    "localhost"
                                ],
                                "port": "30000",
                                "path": [
                                    "custom_instructions"
                                ]
                            }
                        },
                        "response": []
                    }
                ]
            },
            {
                "name": "GET",
                "item": [
                    {
                        "name": "get all the conversation names",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "http://localhost:30000/conversations",
                                "protocol": "http",
                                "host": [
                                    "localhost"
                                ],
                                "port": "30000",
                                "path": [
                                    "conversations"
                                ]
                            }
                        },
                        "response": []
                    },
                    {
                        "name": "check if the server is running",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "http://localhost:30000/",
                                "protocol": "http",
                                "host": [
                                    "localhost"
                                ],
                                "port": "30000",
                                "path": [
                                    ""
                                ]
                            }
                        },
                        "response": []
                    },
                    {
                        "name": "get messages of a conversation",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "http://localhost:30000/conversations/hi",
                                "protocol": "http",
                                "host": [
                                    "localhost"
                                ],
                                "port": "30000",
                                "path": [
                                    "conversations",
                                    "hi"
                                ]
                            }
                        },
                        "response": []
                    },
                    {
                        "name": "get all the model names",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "http://localhost:30000/get_models",
                                "protocol": "http",
                                "host": [
                                    "localhost"
                                ],
                                "port": "30000",
                                "path": [
                                    "get_models"
                                ]
                            }
                        },
                        "response": []
                    },
                    {
                        "name": "restart the server",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "http://localhost:30000/restartServer",
                                "protocol": "http",
                                "host": [
                                    "localhost"
                                ],
                                "port": "30000",
                                "path": [
                                    "restartServer"
                                ]
                            }
                        },
                        "response": []
                    },
                    {
                        "name": "download the database ZIP file",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "http://localhost:30000/downloadDB",
                                "protocol": "http",
                                "host": [
                                    "localhost"
                                ],
                                "port": "30000",
                                "path": [
                                    "downloadDB"
                                ]
                            }
                        },
                        "response": []
                    }
                ]
            }
        ]
    }
    """

    run_postman_collection(collection)

if __name__ == "__main__":
    main()
