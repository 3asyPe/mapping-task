# mapping-task
Test project for pulling and parsing articles from the provided API every 5 minutes

To start the application, please install the dependencies using pipenv:
```
pipenv shell
pipenv install
```
Then run the application by running the following command in the src folder:
```
python main.py
```

*The results are printed in the console*

# File structure
src folder - The main folder with all the code
- main.py - A startup file with a recurring task
- services.py - Business logic
- models.py - Given file with the pydantic models
