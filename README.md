# FastAPI: User Authentication and Authorization Demo 

This project demonstrates:

1) Implementation of the API endpoints using FastAPI
2) User authentication (Oauth2 flow + JWT Token)
3) Role based authentication
4) Client logging
5) Unit testing of FastAPI application, and test coverage statistics
 

### 1. Running Project Locally

```
uvicorn app.main:app --reload
```


###  2. Running Tests

```
python -m pytest tests/ -svv
```


### 3. Running Tests with Test Coverage Statistics

```
python -m pytest --cov=app tests/
```

It is possible to generate coverage report in .html format.
Run from the commandline: "$ coverage html" command. It will create
a folder **htmlcov** with an **index.html** inside. Open the **index.html**
file in your web browser and view the report.


### 4. Debugging

For debug purposes I have created a file called *start_local_server.py*.
The file contains a script starting the application locally. It is equivalent to
launching the command:

```
$ uvicorn app.main:app <hos>:<port>
```

The script gives us more flexibility to run the server and use it when debugging locally.

Because we are running the Uvicorn server directly from the code, we can call
our FastAPI application directly from the debugger.

#### 4.1 Debugging in PyCharm
- Open the **Run** menu
- Select the option **Debug**
- Add breakpoints to the code
- Select the file to debug (in our case *start_local_server.py*)

#### 4.2 Debugging Tests

There is a file *start_running_tests.py*, that you can use for debugging of tests. 


### 5. References

- More on debugging in PyCharm: https://www.jetbrains.com/help/pycharm/debugging-your-first-python-application.html

- More on working with FastAPI in PyCharm: https://www.jetbrains.com/help/pycharm/fastapi-project.html