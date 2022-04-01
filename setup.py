import setuptools
import subprocess
import codecs

gowork_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .strip()
)

setuptools.setup(
    name="gowork",
    version=gowork_version,
    author="Patrick Amaral",
    author_email="patrick.dev.atom@gmail.com",
    description="Library to help track your credentials and database engines",
    long_description=codecs.open('README.md', encoding='utf-8').read(),
    url="https://github.com/Phomint/GoWork",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license='GPLv3',
    keywords=['databases', 'athena', 'mysql'],
    install_requires=[
        "numpy",
        "pandas",
        "pyathena",
        "pymysql",
        "glob2",
        "sqlalchemy"
    ],
)