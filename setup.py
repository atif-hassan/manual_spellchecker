import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    
setuptools.setup(
     name = 'manual_spellchecker',  
     version = '1.1',
     author = "Atif Hassan",
     author_email = "atif.hit.hassan@gmail.com",
     description = "A manual spell checker built on pyenchant that allows you to swiftly correct misspelled words.",
     long_description = long_description,
     long_description_content_type = "text/markdown",
     url = "https://github.com/atif-hassan/manual_spellchecker",
     py_modules = ["manual_spellchecker"],
     package_dir = {'': 'src'},
     install_requires = ["tqdm", "pyenchant", "numpy"],
     include_package_data = True,
     classifiers = [
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.6",
         "Programming Language :: Python :: 3.7",
         "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
         "Operating System :: OS Independent",
     ]
 )
