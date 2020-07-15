from setuptools import setup

setup(
    name="ipython-bg",
    version="0.2",
    packages=["ipython_bg"],
    license="MIT",
    author="Dror Speiser",
    url="http://www.github.com/drorspei/ipython-bg",
    description="IPython magic to run jobs in background",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="ipython bg jobs",
    install_requires = ['ipython'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Framework :: IPython",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)