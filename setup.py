import setuptools

with open("/home/halowens/Documents/Python/Alpaca/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PatchQuant",
    version="0.1.1",
    author="Hal and Carson",
    author_email="owens155@purdue.edu",
    description="Backtesting platform built around Alpaca Exchange",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Patch-Traders/BackTester",
    packages=setuptools.find_packages(),
    package_data={'path_quant': ['path_quant.py']},
    keywords=['backtesting', 'trading',
              'quantitative finance', 'finance'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License"
    ],
    entry_points={
        'console_scripts': [
            'parser=path_quant:pathc_quant.py'
        ]
    },
    python_requires='>=3.6',
)