import requests
import subprocess
import os
import json
import time


class Ask:
    @staticmethod
    def generateHMAC(method, host, path, params):
        exec_params = ["java", "-cp", os.getcwd() + "/AskSignature/", "Main", method, host, path]
        for key in params:
            exec_params.append(key)
            exec_params.append(params[key])
        key = subprocess.check_output(exec_params).strip("\n").strip("\r")
        return "HMAC " + key

    @staticmethod
    def getUrlParamsForGetRequest(params):
        url = "?"
        first = True
        for key in params:
            if first:
                url = url + "" + key + "=" + params[key]
                first = False
            else:
                url = url + "&" + key + "=" + params[key]
        return url

    def sendGetRequest(self, path, params):
        hmac = self.generateHMAC("GET", "api.ask.fm:443", path, params)
        res = self.sess.get("https://api.ask.fm" + path + self.getUrlParamsForGetRequest(params),
                            headers={'Authorization': hmac},
                            verify=False)
        self.rt += 1
        return json.loads(res.text)

    def sendPostRequest(self, path, jsonparams):
        params = {'json': json.dumps(jsonparams, sort_keys=True, separators=(',', ':'))}
        hmac = self.generateHMAC("POST", "api.ask.fm:443", path, params)
        res = self.sess.post("https://api.ask.fm" + path,
                             headers={'Authorization': hmac,
                                      'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8"},
                             data=params,
                             verify=False)
        self.rt += 1
        return json.loads(res.text)

    def getQuestions(self, offset=0):
        if self.debug:
            print "Fetching 25 questions from offset " + str(offset)
        limit = 25
        params = {'limit': str(limit),
                  'offset': str(offset),
                  'rt': str(self.rt),
                  'ts': str(int(time.time()))
                  }
        return self.sendGetRequest("/my/questions", params)

    def postAnswer(self, answer, question_type, question_id):
        if self.debug:
            print "Posting answer: " + answer + " (question_id: " + str(question_id) + ")"
        sendjson = {"answer": {"body": answer,
                               "sharing": [],
                               "type": "text"},
                    "qid": str(question_id),
                    "rt": str(self.rt),
                    "ts": "1472125581",
                    "type": question_type}
        return self.sendPostRequest("/my/questions/answer", sendjson)

    def sendQuestion(self, anonymous, question, recipients):
        if self.debug:
            print "Sending question: " + question + " (recipients :" + str(recipients) + ")"
        sendjson = {"question": {"type": "anonymous" if anonymous else "user",
                                 "body": question},
                    "rt": str(self.rt),
                    "ts": str(int(time.time())),
                    "users": recipients}
        resjson = self.sendPostRequest("/users/questions", sendjson)
        if self.debug:
            print "Question sent. Result: " + json.dumps(resjson)
        return resjson

    def getQuestionLikesUsernames(self, question_id, username):
        has_more = True
        offset = 0
        limit = 25
        users = []
        while has_more:
            if self.debug:
                print "Fetching " + str(limit) + " new users (" + str(len(users)) + " already fetched)"
            params = {'limit': str(limit),
                      'offset': str(offset),
                      'qid': question_id,
                      'rt': str(self.rt),
                      'ts': str(int(time.time())),
                      'uid': username}
            resjson = self.sendGetRequest("/users/answers/likes", params)
            for user in resjson['users']:
                users.append(user['uid'])
            if not resjson['hasMore']:
                has_more = False
            else:
                offset += limit
        if self.debug:
            print "Fetched " + str(len(users)) + " users in total."
        return users

    def getQuestionLikesUsernamesNoDisabledAccounts(self, question_id, username):
        has_more = True
        offset = 0
        limit = 25
        users = []
        while has_more:
            if self.debug:
                print "Getting " + str(limit) + " new users (" + str(len(users)) + " already fetched)"
            params = {'limit': str(limit),
                      'offset': str(offset),
                      'qid': question_id,
                      'rt': str(self.rt),
                      'ts': str(int(time.time())),
                      'uid': username}
            resjson = self.sendGetRequest("/users/answers/likes", params)
            for user in resjson['users']:
                if user['active']:
                    users.append(user['uid'])
            if not resjson['hasMore']:
                has_more = False
            else:
                offset += limit
        if self.debug:
            print "Fetched " + str(len(users)) + " users in total."
        return users

    def login(self, username, password):
        if self.debug:
            print "Logging in on Ask.FM for user: " + username
        sendjson = {'did': self.deviceId,
                    'guid': self.deviceId,
                    'pass': password,
                    'rt': str(self.rt),
                    'ts': str(int(time.time())),
                    'uid': username}
        resjson = self.sendPostRequest("/authorize", sendjson)
        self.accessToken = resjson['accessToken']
        self.sess.headers.update({'X-Access-Token': self.accessToken})
        print "Logged in. Final access token: " + self.accessToken

    def setManualLoginToken(self, token):
        self.accessToken = token
        self.sess.headers.update({'X-Access-Token': self.accessToken})

    def __init__(self, device_id, debug=False):
        self.sess = requests.session()
        self.deviceId = device_id
        self.rt = 2
        self.debug = debug
        self.sess.headers.update({'X-Api-Version': '0.8',
                                  'Host': 'api.ask.fm:443',
                                  'X-Client-Type': 'android_3.8.1',
                                  'Accept': 'application/json; charset=utf-8',
                                  'Accept-Encoding': 'identity',
                                  'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; GT-N7100 Build/MOB30R)'})
        params = {'did': self.deviceId,
                  'rt': str(self.rt),
                  'ts': str(int(time.time()))}
        resjson = self.sendGetRequest("/token", params)
        self.accessToken = resjson['accessToken']
        print "Got initial access token: " + self.accessToken
        self.sess.headers.update({'X-Access-Token': self.accessToken})
