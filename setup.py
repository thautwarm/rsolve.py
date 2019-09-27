from setuptools import setup, find_packages

setup(
    name='rsolve.py',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/thautwarm/rsolve.py',
    license='MIT',
    author='thautwarm',
    python_requires='>=3.6.0',
    author_email='twshere@outlook.com',
    description='For constraint satisfaction problems in Python',
    install_requires=['prettyprinter'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    zip_safe=False,
)
