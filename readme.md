# GitHub Repository Viewer

This application is a GitHub Repository Viewer built using Python and Streamlit. It allows users to view repositories of a specified GitHub user and parse the repositories to extract information about functions and machine learning models.

## Features

1. **Home Page**: Enter a GitHub username to fetch and display their repositories. The repositories are also saved to a JSON file.

2. **Parser Page**: Select a user from the saved JSON files to view their repositories. Click on a repository to view its contents, including functions and machine learning models.

3. **About Page**: Displays a random description with randomized text styles.

4. **Contact Page**: Provides contact information.

## Functions

The application includes several functions to extract information from different types of files:

- `clone_repository(repo_url, destination_folder)`: Clones a repository from a specified URL to a destination folder.

- `extract_python_functions_from_file(file_path)`: Extracts Python functions from a file.

- `extract_csharp_functions_from_file(file_path)`: Extracts C# functions from a file.

- `extract_c_functions_from_file(file_path)`: Extracts C functions from a file.

- `extract_javascript_functions_from_file(file_path)`: Extracts JavaScript functions from a file.

- `extract_java_functions_from_file(file_path)`: Extracts Java functions from a file.

- `extract_jupyter_functions_from_file(file_path)`: Extracts functions from a Jupyter notebook file.

- `extract_cpp_functions_from_file(file_path)`: Extracts C++ functions from a file.

- `extract_ml_models_from_file(file_path)`: Extracts machine learning models from a file.

- `get_user_repositories(username)`: Fetches repositories of a specified GitHub user.

## How to Run

To run this application, use the following command:

```bash
streamlit run main.py