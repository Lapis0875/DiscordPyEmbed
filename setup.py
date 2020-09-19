from setuptools import setup, find_packages

# Setup module
setup(
    # Module name
    name="discord.py-embed",
    # Module version
    version="1.0.0",
    # License - MIT!
    license='MIT',
    # Author (Github username)
    author="Lapis0875",
    # Author`s email.
    author_email="lapis0875@kakao.com",
    # Short description
    description="Some embed-related features for discord.py",
    # Long description in REAMDME.md
    long_description=open('README.rst').read(),
    # Project url
    url="https://github.com/Lapis0875/",
    # Include module directory 'embed_tools'
    packages=find_packages(),
    # Dependencies : This project use module 'colorlog', so add requirements.
    install_requires=["discord.py>=1.4.1"],
    # Module`s python requirement
    python_requires=">=3.6",
    # Keywords about the module
    keywords=["discord api", "discord.py", "discord embed"],
    # Tags about the module
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
