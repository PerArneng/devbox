from setuptools import setup, find_packages
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            rel_path = os.path.join(path, filename)
            rel_path = rel_path.replace("%s/" % directory, "")
            if rel_path.endswith('.yml'):
                paths.append(rel_path)
    return paths

extra_files = package_files('playbooks')

#for fl in extra_files:
#    print(fl)
#exit(1)

setup(name='devbox',
      version='1.0',
      description='A tool for installing a devbox',
      url='https://github.com/PerArneng/devbox',
      author='Per Arneng',
      author_email='per.arneng@scalebit.com',
      license='APACHE 2.0',
      packages=find_packages(),
      entry_points = {
            'console_scripts': ['devbox=dbox.devbox:main'],
      },
      package_data={
          "playbooks": extra_files
      },
      zip_safe=False)