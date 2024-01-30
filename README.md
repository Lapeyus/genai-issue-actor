# genai-issue-actor

Original Author: Evan Seabrook

This project was created to explore how Generative AI could help facilitate code changes based on issues created in a repository. To explore this, I designed a workflow following roughly how code is developed today in a simple project:

1. A user submits a new issue within the GitHub repository outlining in plain language what change they would like to see.

2. A webhook configured to fire for new issues posts the details to a Cloud Function hosted within my Google Cloud project, which clones the repository.

3. Once the repo has been cloned, a new branch is created and the code is adapted using generative AI to interpret and make the requested changes.

4. The Cloud Function pushes the changes to the repository and opens a pull request referencing the original issue.

**IMPORTANT:** To prevent an influx of personal cloud costs, I have disabled the webhook. I encourage folks that are interested in this project to fork this repository and experiment with it yourselves.

## Project Structure

The project is split into several key directories/modules:

- cloud_function
  - Houses the webhook application code that handles new issues, makes code changes in `main.py` and `tests`, and pushes them to this repository + creates a pull request.
- tests
  - Houses the unit tests for `main.py`.
- main.py

## Deployment

If you are interested in experimenting with this project further, please fork it. To set up the Cloud Function on GCP, you will need to:

1. Generate a personal access token for your GitHub account (it will need write permissions for Issues in your fork).
2. Generate an RSA deploy key for your repository (it will need write access to your fork).
3. Generate an API KEY for the Gemini API.
4. cd into the infrastructure folder and run `terraform apply`.
5. Once the terraform creation process is done, add your secret versions into the secret manager.
6. Set your GitHub webhook URL to the function and choose to be notified on new issues.


Please adjust the code to fulfill the following change. Provide just the new version of the code -- Avoid using markdown formatting such as backticks and language name, the entire response string must be executable code only. if the desired changed does not affect the code, please provide the same existing code as your response:

improve README.md

## **Improved README.md**

The genai-issue-actor project explores how Generative AI can help facilitate code changes based on issues created in a repository. It follows a typical development workflow:

1. A user creates a new issue in the GitHub repository, describing the desired change in plain language.
2. A webhook triggers a Cloud Function in a Google Cloud project, which clones the repository.
3. Generative AI interprets the issue and makes the requested changes in a new branch.
4. The Cloud Function pushes the changes to the repository and opens a pull request, referencing the original issue.

**NOTE:** To prevent personal cloud costs, the webhook is currently disabled. If you want to experiment with this project, fork the repository and set up the Cloud Function on GCP.

## **Project Structure**

- cloud_function: Contains the webhook application code that handles new issues, makes code changes, and pushes them to the repository, creating a pull request.
- tests: Houses the unit tests for `main.py`.
- main.py: Handles the core logic of the project.

## **Deployment**

1. Generate a GitHub personal access token with write permissions for Issues in your fork.
2. Generate an RSA deploy key for your repository with write access to your fork.
3. Obtain an API key for the Gemini API.
4. Run `terraform apply` in the `infrastructure` folder. After the terraform creation process, add your secret versions to the secret manager.
5. Set your GitHub webhook URL to the function and choose to be notified on new issues.

## **Conclusion**

The genai-issue-actor project demonstrates the potential of Generative AI in facilitating code changes based on user requests. Experiment with the project by forking the repository and setting up the Cloud Function.