from setuptools import find_packages, setup


def get_version(path):
    for line in open(path):
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError(f"Unable to find __version__ in {path}")


def get_requirements(path):
    res = []
    for line in open(path):
        line = line.split('#')[0].strip()
        if line:
            res.append(line)
    return res


setup(
    name='pyterrier-ciff',
    version=get_version('pyterrier_ciff/__init__.py'),
    author='Sean MacAvaney',
    author_email='sean.macavaney@glasgow.ac.uk',
    description="PyTerrier integrations with CIFF",
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/seanmacavaney/pyterrier-ciff',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'pyterrier.artifact': [
            'sparse_index.ciff = pyterrier_ciff:CiffIndex',
        ],
        'pyterrier.artifact.metadata_adapter': [
            'sparse_index.ciff = pyterrier_ciff._utils:_ciff_metadata_adapter',
        ],
    },
    install_requires=get_requirements('requirements.txt'),
    python_requires='>=3.10',
)
