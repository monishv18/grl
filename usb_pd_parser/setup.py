from setuptools import setup, find_packages

setup(
    name="usb_pd_parser",
    version="1.0.0",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "usbpd-parse=parser.scripts.parse_usb_pd:main",
        ]
    }
)
