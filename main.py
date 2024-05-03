import os
import streamlit as st
import requests
import json
import git
import ast
import subprocess
import nbformat, re
import random


def clone_repository(repo_url, destination_folder):
    try:
        git.Repo.clone_from(repo_url, destination_folder)
        return True
    except git.exc.GitCommandError as e:
        print(f"Error cloning repository: {e}")
        return False


def extract_python_functions_from_file(file_path):
    with open(file_path, "r") as f:
        code = f.read()
        tree = ast.parse(code)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return functions


def extract_csharp_functions_from_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        pattern = (r"(?<=\b(?:public|private|protected)\s+)(?:static\s+)?(?:async\s+)?(?:unsafe\s+)?(?:partial\s+)?("
                   r"?:delegate\s+)?\w+\s+(\w+)\s*\(")
        functions = re.findall(pattern, content)
        return functions


def extract_c_functions_from_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        pattern = r"\b(?:void|int|float|double|char|short|long|signed|unsigned)\s+\w+\s*\([^)]*\)\s*\{"
        functions = re.findall(pattern, content)
        functions = [func.split()[1] for func in functions]  # Extract function name from declaration
        return functions


def extract_javascript_functions_from_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        pattern = r"function\s+([^\s\(]+)\s*\("
        functions = re.findall(pattern, content)
        return functions


def extract_csharp_functions_from_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        pattern = r"(?<=\b(?:public|private|protected)\s+)(?:static\s+)?(?:async\s+)?(?:unsafe\s+)?(?:partial\s+)?(?:delegate\s+)?\w+\s+(\w+)\s*\("
        functions = re.findall(pattern, content)
        return functions


def extract_java_functions_from_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        # Regular expression to match Java method declarations
        pattern = r"(?<=\b(?:public|private|protected|static|final|synchronized|abstract|native|strictfp)\s+)(?:\w+\s+)*\w+\s*(?=\()"
        functions = re.findall(pattern, content)
        return functions


def extract_jupyter_functions_from_file(file_path):
    with open(file_path, "r") as f:
        nb = nbformat.read(f, as_version=4)
        functions = []
        for cell in nb.cells:
            if cell.cell_type == 'code':
                functions.extend([item for item in cell.source.split('\n') if item.startswith('def ')])
        return functions


def extract_cpp_functions_from_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        # Regular expression to match C++ function declarations
        pattern = r"(?<=\b(?:class|struct)\s+)\w+\s*(?=\{)"
        functions = re.findall(pattern, content)
        return functions


def extract_ml_models_from_file(file_path):
    ml_models = []
    encodings = ['utf-8', 'latin-1']  # Add more encodings if needed
    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                content = f.read()
                # Common machine learning library imports
                ml_libraries = ["sklearn", "tensorflow", "keras", "torch", "xgboost", "catboost", "lightgbm", "fastai"]
                for library in ml_libraries:
                    pattern = rf"import\s+{library}\.(?:.*)model"
                    matches = re.findall(pattern, content)
                    for match in matches:
                        model_name = match.split(".")[-2]
                        ml_models.append(model_name)
            # If we successfully read the file, break the loop
            break
        except UnicodeDecodeError:
            continue
    return ml_models


def get_user_repositories(username):
    repositories = []
    url = f"https://api.github.com/users/{username}/repos"

    # Initial request to get the first page of repositories
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        repositories.extend(response.json())

        # Check if there are more pages of repositories
        while 'next' in response.links.keys():
            next_url = response.links['next']['url']
            response = requests.get(next_url)

            # Extend the repositories list with repositories from the next page
            if response.status_code == 200:
                repositories.extend(response.json())
            else:
                st.error(f"Error: Unable to fetch repositories for user '{username}'.")
                return None

        return repositories
    else:
        st.error(f"Error: Unable to fetch repositories for user '{username}'.")
        return None


def home_page():
    st.title("GitHub Repository Viewer")
    video_html = """
    		<style>

    		#myVideo {
    		  position: fixed;
    		  right: 0;
    		  bottom: 0;
    		  min-width: 100%; 
    		  min-height: 100%;
    		}

    		.content {
    		  position: fixed;
    		  bottom: 0;
    		  background: rgba(0, 0, 0, 0.5);
    		  color: #f1f1f1;
    		  width: 100%;
    		  padding: 20px;
    		}

    		</style>	
    		<video autoplay muted loop id="myVideo">
    		  <source src="https://static.streamlit.io/examples/star.mp4")>
    		  Your browser does not support HTML5 video.
    		</video>
            """

    st.markdown(video_html, unsafe_allow_html=True)
    username = st.text_input("Enter a GitHub username:")
    if st.button("Fetch Repositories"):
        if username:
            repositories = get_user_repositories(username)
            if repositories:
                st.success(f"Repositories for user '{username}':")
                for repo in repositories:
                    st.write(f"- [{repo['name']}]({repo['html_url']})")

                # Save repositories to a JSON file in the "Users" folder
                folder_path = "Users"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                save_filename = os.path.join(folder_path, f"{username}_repositories.json")
                with open(save_filename, "w") as f:
                    json.dump(repositories, f, indent=4)
                st.info(f"Repositories saved to {save_filename}")
                return repositories
            else:
                st.warning("Please enter a valid GitHub username.")
        else:
            st.warning("Please enter a GitHub username.")


def about_page():
    st.write("# About Page")

    video_html = """
    		<style>

    		#myVideo {
    		  position: fixed;
    		  right: 0;
    		  bottom: 0;
    		  min-width: 100%; 
    		  min-height: 100%;
    		}

    		.content {
    		  position: fixed;
    		  bottom: 0;
    		  background: rgba(0, 0, 0, 0.5);
    		  color: #f1f1f1;
    		  width: 100%;
    		  padding: 20px;
    		}

    		</style>	
    		<video autoplay muted loop id="myVideo">
    		  <source src="https://static.streamlit.io/examples/star.mp4")>
    		  Your browser does not support HTML5 video.
    		</video>
            """

    st.markdown(video_html, unsafe_allow_html=True)

    # Initialize session state to track button presses
    if 'button_presses' not in st.session_state:
        st.session_state.button_presses = 0

    # Increment button press counter when button is pressed
    if st.button("Randomize the text!"):
        st.session_state.button_presses += 1

    fonts = [
        "Arial", "Helvetica", "Times New Roman", "Courier New", "Verdana", "Georgia", "Palatino", "Garamond",
        "Comic Sans MS", "Impact", "Lucida Sans Unicode", "Tahoma", "Trebuchet MS", "Arial Black", "Arial Narrow",
        "Book Antiqua", "Century Gothic", "Franklin Gothic Medium", "Geneva", "Lucida Console", "Lucida Sans",
        "MS Sans Serif",
        "MS Serif", "Palatino Linotype", "System", "Arial Rounded MT Bold", "Bookman Old Style", "Candara", "Consolas",
        "Constantia", "Corbel", "Copperplate Gothic Bold", "Copperplate Gothic Light", "Elephant", "Futura",
        "Gloucester MT Extra Condensed",
        "Goudy Old Style", "High Tower Text", "Lucida Bright", "Monotype Corsiva", "Perpetua", "Rockwell", "Segoe UI",
        "Stencil",
        "Tw Cen MT", "Agency FB", "Bodoni MT", "Wide Latin", "Vivaldi"
    ]

    description = ("I am a human although im not always thought to be one. I love playing with data and am "
                   "hilariously"
                   "broke. For real, if you have any money i can have, I will not complain. I need to buy a new pc cuz"
                   "I accidentally blew up my last one because of some experimental research. Additionally, I despise "
                   "front-end"
                   "The only reason this text looks as gay as it is, is because of a game I wanted to implement and I"
                   "had nothing"
                   "better to show for when it came to the front end part of my project")

    # Split the description into words
    words = description.split()

    # Generate HTML code with random fonts and colors for each word
    html_code = ""
    for word in words:
        font = random.choice(fonts)
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))  # Generate random hex color code
        html_code += f'<span style="font-family: {font}; color: {color};">{word}</span> '

    # Display the random description
    st.markdown(html_code, unsafe_allow_html=True)

    # Check if the user pressed the button 10 times
    if st.session_state.button_presses >= 10:
        # Load the game script
        game_script_path = "game.py"
        if os.path.exists(game_script_path):
            st.write("Loading the game...")
            # Execute the game script
            subprocess.Popen(["streamlit", "run", game_script_path])
        else:
            st.error("Game script not found!")


def contact_page():
    st.write("# Contact Page")
    st.write("You can contact us through the following methods:")

    video_html = """
    		<style>

    		#myVideo {
    		  position: fixed;
    		  right: 0;
    		  bottom: 0;
    		  min-width: 100%; 
    		  min-height: 100%;
    		}

    		.content {
    		  position: fixed;
    		  bottom: 0;
    		  background: rgba(0, 0, 0, 0.5);
    		  color: #f1f1f1;
    		  width: 100%;
    		  padding: 20px;
    		}

    		</style>	
    		<video autoplay muted loop id="myVideo">
    		  <source src="https://static.streamlit.io/examples/star.mp4")>
    		  Your browser does not support HTML5 video.
    		</video>
            """

    st.markdown(video_html, unsafe_allow_html=True)

    # GitHub icon with hyperlink
    st.markdown(
        '[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)]('
        'https://github.com/Ibzie)')

    # LinkedIn icon with hyperlink
    st.markdown(
        "[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"
        ")](https://www.linkedin.com/in/ibrahim-akhtar-ab543823b/)")


def parser_page():
    st.title("Repository Parser")
    st.write("Select a user to view their repositories:")

    # List all JSON files in the "Users" folder
    folder_path = "Users"
    json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

    if len(json_files) == 0:
        st.warning("No repositories JSON files found in the 'Users' folder.")
        return

    # Allow user to select a JSON file
    selected_file = st.selectbox("Select JSON file", json_files)

    # Load selected JSON file
    with open(os.path.join(folder_path, selected_file), "r") as f:
        repositories = json.load(f)

    # Display repository names as clickable objects
    st.write("Click on a repository name to view its contents:")
    selected_repo_name = st.selectbox("Select a repository", [repo['name'] for repo in repositories])

    # Find the selected repository
    selected_repo = next((repo for repo in repositories if repo['name'] == selected_repo_name), None)

    # Display detailed information about the selected repository
    if selected_repo:
        st.write(f"Repository Name: {selected_repo['name']}")
        st.write(f"Description: {selected_repo['description']}")
        st.write(f"Language: {selected_repo['language']}")
        st.write(f"Created At: {selected_repo['created_at']}")
        st.write(f"Last Updated At: {selected_repo['updated_at']}")
        st.write(f"URL: [{selected_repo['html_url']}]({selected_repo['html_url']})")

        # Clone the repository locally
        repo_folder = os.path.join("Repositories", selected_repo['name'])
        clone_repository(selected_repo['html_url'], repo_folder)

        st.write("Functions and Machine Learning Models in the repository:")
        for root, _, files in os.walk(repo_folder):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".py"):
                    functions = extract_python_functions_from_file(file_path)
                elif file.endswith(".cpp"):
                    functions = extract_cpp_functions_from_file(file_path)
                elif file.endswith(".ipynb"):
                    functions = extract_jupyter_functions_from_file(file_path)
                elif file.endswith(".js"):
                    functions = extract_javascript_functions_from_file(file_path)
                elif file.endswith(".c"):
                    functions = extract_c_functions_from_file(file_path)
                elif file.endswith(".cs"):
                    functions = extract_csharp_functions_from_file(file_path)
                elif file.endswith(".java"):
                    functions = extract_java_functions_from_file(file_path)
                else:
                    functions = []  # Handle other file types

                ml_models = extract_ml_models_from_file(file_path)

                if functions or ml_models:
                    st.write(f"File: {file_path}")
                    if functions:
                        st.write("Functions:")
                        for function in functions:
                            st.write(f"- {function}")
                    if ml_models:
                        st.write("Machine Learning Models:")
                        for model in ml_models:
                            st.write(f"- {model}")

    else:
        st.warning("Repository not found.")


def main():
    st.sidebar.title("Pick Your Poison")
    page = st.sidebar.radio("Go to", ["Home", "Parser", "About", "Contact"])

    if page == "Home":
        home_page()
    elif page == "Parser":
        parser_page()
    elif page == "About":
        about_page()
    elif page == "Contact":
        contact_page()


if __name__ == "__main__":
    main()
