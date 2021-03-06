CADISE Backend API
What's Here
-----------

* README.md - this file
* requirements.txt - this file is used install Python dependencies needed by the API
* /resources  - this folder contains the resources to be indexed.

Getting Started
---------------

1. Create a Python virtual environment for the project.

        $ virtualenv .venv

2. Activate the virtual environment:

        a) For Windows
        $ ./.venv/Scripts/activate

        b) For Linux
        $ source ./.venv/Scripts/activate

3. Install Python dependencies for the project:

        $ pip install -r requirements.txt

        $ python -m spacy download en_core_web_md

        $ python -m nltk.downloader wordnet

        $ python -m nltk.downloader omw


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

