# versatile

How To Run:
1. clone the repo
2. cd into folder versatile
3. activate virtual (if it's fit otherwise create yours)
4. if need - install dependencies from requirement.txt
5. config env variables: 
  HTTP_PORT, DEVICES_JSON, CRANES_JSON
  (server will not start with missing params)
6. run main.py
7. to run tests with pytest:
  run pytest
  (pay attention to #region test add instructions)

architecture:
backend:
  python
  fastapi(handle many concurrent requests) + uvicorn (which handle gracefull SIGTERM- running with the default value)
  tests - pytest
