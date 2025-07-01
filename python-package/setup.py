from pathlib import Path
from setuptools import setup, find_packages

cwd = Path(__file__).resolve().parent
requirements = (cwd / 'employee_events' / 'requirements.txt').read_text().splitlines()
requirements = [req for req in requirements if req and not req.startswith('#')]

setup_args = dict(
    name='employee_events',
    version='0.0',
    description='SQL Query API',
    packages=find_packages(),
    package_data={'': ['employee_events.db', 'requirements.txt']},
    install_requires=requirements,
    author="Ovidiu Mihalache",
)

if __name__ == "__main__":
    setup(**setup_args)
