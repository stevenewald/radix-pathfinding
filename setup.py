import setuptools

#with open("README.md", "r", encoding="utf-8") as fh:
#    long_description = fh.read()

from unittest import TestLoader
def my_test_suite():
    test_loader = TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite
if(__name__=='__main__'):
    setuptools.setup(
        name="pyradix-stevenewald",
        version="0.0.1",
        author="Steven Ewald",
        author_email="steve@steve.ee",
        description="Python implementation of Radix Tree: memory and speed optimized language detection",
        long_description="",
        long_description_content_type="text/markdown",
        url="https://github.com/stevenewald/pyradix",
        project_urls={
            "Bug Tracker": "https://github.com/stevenewald/pyradix/issues",
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        package_dir={"": "src"},
        packages=setuptools.find_packages(where="src"),
        python_requires=">=3.6",
        test_suite='setup.my_test_suite',
    )