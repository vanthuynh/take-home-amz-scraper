# Project Brief: Automated Price Drop Notification for iPad on Amazon.com

## Objective:
An application that monitors the price of the iPad on Amazon.com and sends an automated notification whenever there's a price drop

## Available Features:

## Project Scopes:

- [X] Handling changes in the webpage structure
- [X] Scripts run at reasonable interval to effectively monitor price changes
- [ ] Data Processing:  Implement logic to compare the current price against the previously recorded price to detect a price drop.
- [ ] Notification: Upon detecting a price drop, trigger an automated notification
- [ ] Logging: Maintain a log of price changes and notification events

## Installations Required
- Install Chromedriver: [click here](https://googlechromelabs.github.io/chrome-for-testing/#stable)

-

## How To Run Application
1. Install `virtualenv`:
```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:
```
$ python -m venv venv
```

3. Then run the command:
```
$ .\venv\Scripts\activate (for Powershell/CMD)
or
$ source venv/Scripts/activate (for GitBash)
```

4. Then install the dependencies:
```
$ (env) pip install -r requirements.txt
```

5. Make change to the `headers` variable by replacing value of `User-Agent` :

```
visit [WhatIsMyBrowser.com](https://www.whatismybrowser.com/detect/what-is-my-user-agent/) then copy & paste the User-Agent header
```

6. Finally start the web server:
```
$ (env) python app.py
```

---

### How the application works
- Web Crawler:
- Frontend:
- Backend:
- Database:

### Overcome Challenges
- Couldn't request from  amazon page --> fixed by adding proxies parameter
- Using generic/hard-coded User-agent for headers doesn't work as well as environ.get()
- Naive-processing prices eventually encounter difference in posted prices ($1,199 vs $459)
-
### Testing Performed
