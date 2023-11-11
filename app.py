import requests
import json
from flask import Flask, request
import imghdr

# the server has an api "/tests" that accepts a get request with parameters "task", "host", "port", and "api"
app = Flask(__name__)

@app.route("/tests", methods=['GET'])
def tests():
    if request.method == 'GET':
        #gets the request body
        body = request.args
        host = body.get("host")
        port = body.get("port")
        api = body.get("API")
        task = body.get("task")
        assert host != None, "host is not provided"
        assert port != None, "port is not provided"
        assert task != None, "task is not provided"
        if (api == None):
            api = ""
        #opens the test files located on the server
        image = open("test_im.png","rb").read() # For detection and segmentation, we only have this image
        files = None
        if(task == "inpainting"):
            mask = open("test_mask.png","rb").read() # For inpainting, we have this image and a mask
            # put the image and mask in a multipart/form-data
            files = {'image': image, 'mask': mask}
        else:
            files = {'image': image}
        # send a post request to the detect endpoint
        response = requests.post("http://" + host + ":" + port + "/" + api, files=files) # "/detections" is the API for YOLO. Here we want to let the test server receive an api from a get requests's parameter.
                                                              # the API, as far as I remember, includes "/" and "detections".
        # TODO: check the response status code
        status = response.status_code
        if(status != 200):
            return{
                'result' : 'false',
                'code': 1,
                'error' : "Incorrect status code", 
                'message' : status
            }
    
        # TODO: check the format of the response
        # the response should be a PNG image encoded as a binary string
        try:
            # open("result.png", "wb").write(response.content)
            content = response.content
            # check if the content is a binary string
            if(isinstance(content, str)):
                return{
                    'result' : 'false',
                    'code': 2,
                    'error' : "Incorrect encoding in response content"
                }
            # check the format of the image
            format = imghdr.what(None, h=image)
            if(format != "png"):
                return{
                    'result' : 'false',
                    'code': 3,
                    'error' : "Incorrect format for PNG",
                    'message' : format
                }
        except:
            return{
                'result' : 'false',
                'code': 4,
                'error' : "Error when checking the response content",
                'message' : response.content
            }
        return {
            'result' : 'true',
            'code': 0
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)