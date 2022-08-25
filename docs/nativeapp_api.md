### 1. Start Password Demo - Secure Mode

Starts password Demo in secure mode on local Client.

Example return:

{  
"message": "Successfully started the Demo.",  
"success": true  
}

***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://localhost:5000/orchestration/start/demo/password
```

***Body:***

```js
{"secureMode":true, "language": "en"}
```

### 7. Status Password Demo

Returns actual status of the password demonstration.

Ether

{ "password_webserver": "running"}

or

{ "password_webserver": "not found"}

***Endpoint:***

```bash
Method: GET
Type: 
URL: http://localhost:5000/orchestration/status/demo/password
```


### 13. Stop Password Demo

Stops password Demonstration on local Client

Example return:

{ "message": "Stopped all remaining Demos.", "success": **true**}

***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://localhost:5000/orchestration/stop/demo/password
```
