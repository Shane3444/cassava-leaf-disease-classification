import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

__version__ = "0.0.0"

REPO_NAME = "cassava-leaf-disease-classification"
AUTHOR_USER_NAME = "Shane3444"
SRC_REPO = "cnnClassifier"
AUTHOR_EMAIL = "shourya3444@gmail.com"

setuptools.setup(
    name = SRC_REPO,
    version = __version__,
    author = AUTHOR_USER_NAME,
    author_email = AUTHOR_EMAIL,
    description = "Python package for CNN classification",
    long_description = long_description,
    url = f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls = {
        "Bug Tracker" : f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir = {"" : "src"},
    packages = setuptools.find_packages(where = "src")
)