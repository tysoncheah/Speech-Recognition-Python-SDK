pip install aliyun-python-sdk-core==2.13.3

{
    "appkey": "your-appkey",
    "file_link": "https://aliyun-nls.oss-cn-hangzhou.aliyuncs.com/asr/fileASR/examples/nls-sample-16k.wav",
    "auto_split":false,
    "version": "4.0",
    "enable_words": false,
    // The valid_times parameter specifies the valid time period that truly requires speech recognition in the total length of an audio track. This parameter is optional.
    "valid_times": [
        {
            "begin_time": 200,
            "end_time":2000,
            "channel_id": 0
        }
    ]
}

# -*- coding: utf8 -*-
import json
import time
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
def fileTrans(akId, akSecret, appKey, fileLink) :
    # The constant parameters, such as the region ID. Do not modify their values.
    REGION_ID = "ap-southeast-1"
    PRODUCT = "nls-filetrans"
    DOMAIN = "filetrans.ap-southeast-1.aliyuncs.com"
    API_VERSION = "2019-08-23"
    POST_REQUEST_ACTION = "SubmitTask"
    GET_REQUEST_ACTION = "GetTaskResult"
    # The keys of request parameters.
    KEY_APP_KEY = "appkey"
    KEY_FILE_LINK = "file_link"
    KEY_VERSION = "version"
    KEY_ENABLE_WORDS = "enable_words"
    # The key that specifies whether to enable automatic track splitting.
    KEY_AUTO_SPLIT = "auto_split"
    # The keys of response parameters.
    KEY_TASK = "Task"
    KEY_TASK_ID = "TaskId"
    KEY_STATUS_TEXT = "StatusText"
    KEY_RESULT = "Result"
    # The status values.
    STATUS_SUCCESS = "SUCCESS"
    STATUS_RUNNING = "RUNNING"
    STATUS_QUEUEING = "QUEUEING"
    # Create an AcsClient instance.
    client = AcsClient(akId, akSecret, REGION_ID)
    # Create and send a recording file recognition request.
    postRequest = CommonRequest()
    postRequest.set_domain(DOMAIN)
    postRequest.set_version(API_VERSION)
    postRequest.set_product(PRODUCT)
    postRequest.set_action_name(POST_REQUEST_ACTION)
    postRequest.set_method('POST')
    # Specify the version of the recording file recognition service. If you are a new user, set this parameter to 4.0. If you use the default version 2.0, comment out this parameter.
    # Specify whether to return the recognition results of words. Default value: false. This parameter takes effect only when the version of the recording file recognition service is 4.0.
    task = {KEY_APP_KEY : appKey, KEY_FILE_LINK : fileLink, KEY_VERSION : "4.0", KEY_ENABLE_WORDS : False}
    # Specify whether to enable automatic track splitting. You can set the KEY_AUTO_SPLIT parameter to True to enable automatic track splitting.
    # task = {KEY_APP_KEY : appKey, KEY_FILE_LINK : fileLink, KEY_VERSION : "4.0", KEY_ENABLE_WORDS : False, KEY_AUTO_SPLIT : True}
    task = json.dumps(task)
    print(task)
    postRequest.add_body_params(KEY_TASK, task)
    taskId = ""
    try :
        postResponse = client.do_action_with_exception(postRequest)
        postResponse = json.loads(postResponse)
        print (postResponse)
        statusText = postResponse[KEY_STATUS_TEXT]
        if statusText == STATUS_SUCCESS :
            print ("The recording file recognition request is successful.")
            taskId = postResponse[KEY_TASK_ID]
        else :
            print ("The recording file recognition request fails.")
            return
    except ServerException as e:
        print (e)
    except ClientException as e:
        print (e)
    # Create a CommonRequest object and specify the task ID.
    getRequest = CommonRequest()
    getRequest.set_domain(DOMAIN)
    getRequest.set_version(API_VERSION)
    getRequest.set_product(PRODUCT)
    getRequest.set_action_name(GET_REQUEST_ACTION)
    getRequest.set_method('GET')
    getRequest.add_query_param(KEY_TASK_ID, taskId)
    # Send the query request for the recording file recognition result.
    # Use the polling method to query the recognition result. The polling runs until the status message that the server returns is SUCCESS, SUCCESS_WITH_NO_VALID_FRAGMENT,
    # or an error message.
    statusText = ""
    while True :
        try :
            getResponse = client.do_action_with_exception(getRequest)
            getResponse = json.loads(getResponse)
            print (getResponse)
            statusText = getResponse[KEY_STATUS_TEXT]
            if statusText == STATUS_RUNNING or statusText == STATUS_QUEUEING :
                # Continue the polling.
                time.sleep(10)
            else :
                # End the polling.
                break
        except ServerException as e:
            print (e)
        except ClientException as e:
            print (e)
    if statusText == STATUS_SUCCESS :
        print ("The recording file is recognized.")
    else :
        print ("Failed to recognize the recording file.")
    return
accessKeyId = "Your AccessKey ID"
accessKeySecret = "Your AccessKey secret"
appKey = "Your appkey"
fileLink = "https://aliyun-nls.oss-cn-hangzhou.aliyuncs.com/asr/fileASR/examples/nls-sample-16k.wav"
# Start the recording file recognition task.
fileTrans(accessKeyId, accessKeySecret, appKey, fileLink)
