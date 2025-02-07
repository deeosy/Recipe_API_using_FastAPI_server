# Setup

## Python

Python is a versatile, high-level programming language known for its simplicity, readability, and extensive libraries, making it ideal for a wide range of applications, from web development to data science.

To run this project you'll need a way to run python within these version constraints: 3.8 - 3.12

### Managing versions of Python

To safely install and run different python versions without interfering with your system, it's recommended that you use a python version manager such as [pyenv](https://github.com/pyenv/pyenv).

Pyenv is a lightweight tool that simplifies the management of multiple Python versions by allowing users to easily switch between versions, set global or project-specific defaults, and install different Python distributions without interfering with the system Python.

Once you have pyenv setup you can choose to install a version of python that is compatible with this project. The commands might look like:

```
pyenv install 3.11.10
cd fastAPI-server-1
pyenv local 3.11.10
```

At this point you should have installed python version 3.11.10, and you have activated a local python environment where it is safe to install the dependencies for the project.

## Managing dependencies within the Python Project

Now that you have a python *environment* ready, you can install the dependencies of this project. This project uses a tool called [Poetry](https://python-poetry.org/docs/#installation) to manage the project dependencies, and you can follow the instructions: https://python-poetry.org/docs/#installation to install Poetry within your pyenv environment.

## Installing the project dependencies

Now that you have a python environment setup, have installed a dependency manager, you're now ready to install the dependencies themselveC:\Users\<YourUsername>\AppData\Roaming\Python\Scriptss.

To do this `cd` into the directory where the `pyproject.toml` is located then run `poetry install`

## Running the Project

1. [UNIX]: Run the FastAPI server via poetry with the bash script: `poetry run ./run.sh`
2. [WINDOWS]: Run the FastAPI server via poetry with the Python command: `poetry run python app/main.py`
3. Open http://localhost:8001/

If this has all worked, you should see:
```
{"msg":"Hello, World!"}
```
### Remember to Breathe 😮‍💨

One of the useful aspects of FastAPI is that it automatically generates OpenAPI documentation by analyzing the Python type hints and annotations used in your code.

If your project is running, you can check out the auto-generated docs at: http://localhost:8001/docs/

If you get stuck, you might find help in the [troubleshooting readme](./troubleshooting/README.md)

# Take Home Task

## Task One

Your product owner is keen to provide a richer set of front-end *search* options on the recipes search API. Currently there are requirements to extend the /search/ API to allow ordering of results:

1. Using the label field (Alphabetically)
2. Using the date field (By time)

Implement a mechanism to allow a front-end client to request that the search results are ordered either alphabetically, or by date. Consider how you might extend this functionality in the future.

## Task Two

We want to introduce a concept of 'Users' into the data scheme.
* Some recipes will be *private* to individual users, and should only be served to users who created them.
* Some recipes will be *public*, and can be returned to all users.

Update the hardcoded `RECIPES` data model in recipe_data.py to facilitate this use case.

Update the search API so that:
* For an *Authenticated* User, you return both the *public* and all the *user's private* recipes in the search results. 
* For an *Unauthenticated* request, you return only the *public* recipes in the search results. 

If you want to learn more about FastAPI security, please read here: https://fastapi.tiangolo.com/tutorial/security/. Feel free to go ahead and implement such a system if you're interested however, it's not essential for this task.

For this task, a simple hardcoded method to get the current user could be implemented like this:

```
def get_current_user() -> Optional[User]:
    # Insert your authentication logic here.
    
    # For illustration purposes:
    token = None # "Some" # None  # Replace this with logic to extract token from the request.
    if token:  # You would validate and decode the token here.
        # Return a User instance (this is just an example)
        return User(id=1, name="John Doe", email="john.doe@example.com")
    return None  # No valid user found
```

It's OK to keep all the data hardcoded for now, but please consider how this would work in a real-world use case. For example, you will be asked to describe how a front-end client should securely provide an Authorization credential to a back-end environment.

