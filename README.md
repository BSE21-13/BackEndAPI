What's Here
-----------

* README.md - this file
* requirements.txt - this file is used install Python dependencies needed by the API
* /resources  - this folder contains the resources to be indexed.
* runner.py - file that's used to run the api on the Amazon EC2 instance 

Getting Started
---------------

1. Create a Python virtual environment for the project.

        $ virtualenv .venv

2. Activate the virtual environment:

<!-- For Windows -->
        $ ./.venv/Scripts/activate

<!-- For Linux -->
        $ source ./.venv/Scripts/activate

3. Install Python dependencies for the project:

        $ pip install -r requirements.txt

4. Install the Application Code into your virtual environment:

        $ python setup.py install

5. Start the Flask development server:

        $ python runner.py --port 8000

6. Open http://127.0.0.1:8000/ in a web browser to view the output of your
   service.

Project Tests?
---------------

To run your tests locally, go to the root directory of the sample code and run
the `python setup.py pytest` command, which AWS CodeBuild also runs through
your `buildspec.yml` file.
