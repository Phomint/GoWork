import setuptools
import subprocess
import os

gowork_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .strip()
)
assert "." in gowork_version

assert os.path.isfile("GoWork/version.py")
with open("GoWork/VERSION", "w", encoding="utf-8") as fh:
    fh.write(f"{gowork_version}\n")

setuptools.setup(
    name="GoWork",
    version=gowork_version,
    author="Patrick Amaral",
    author_email="patrick.dev.atom@gmail.com",
    description="Library to help track your credentials and database engines",
    url="https://github.com/Phomint/GoWork",
    packages=setuptools.find_packages(),
    package_data={"GoWork": ["VERSION"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "pandas",
        "pyspark",
        "pyathena",
        "pymysql",
        "glob2",
        "sqlalchemy"
    ],
)