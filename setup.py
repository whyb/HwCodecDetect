from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("VERSION") as f:
    version = f.read().strip()

with open("src/HwCodecDetect/version.py", "w") as f:
    f.write(f'__version__ = "{version}"\n')

setup(
    name="HwCodecDetect",
    version=version,
    author="whyb",
    author_email="whyber@outlook.com",
    description="A cross-platform tool to automatically detect and test hardware video decoders/encoders using FFmpeg.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/whyb/HwCodecDetect",
    project_urls={
        "Homepage": "https://github.com/whyb/HwCodecDetect",
        "Issues": "https://github.com/whyb/HwCodecDetect/issues",
    },
    license="BSD-3-Clause",
    license_files=["LICENSE"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Video",
        "Topic :: System :: Installation/Setup",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=["colorama", "tqdm"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "hwcodecdetect=HwCodecDetect.run_tests:run_all_tests"
        ]
    },
    include_package_data=True,
    zip_safe=True,
)
