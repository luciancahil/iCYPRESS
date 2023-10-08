import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iCypress",
    version="0.10",
    author="royhe",
    package_data={'iCYPRESS': ['configs/example_custom.yaml']},
    author_email="royhe62@yahoo.ca",
    description="iCYPRESS: identifying CYtokine PREdictors of diSeaSe. A library that analyzes cytokines using Graph Neural Networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luciancahil/iCYPRESS",
    download_url = 'https://github.com/luciancahil/iCYPRESS/archive/refs/tags/v_01.tar.gz', 
    packages=setuptools.find_packages(),
    install_requires=[
        'deepsnap',
        'matplotlib',
        'networkx',
        'numpy',
        'ogb',
        'pandas',
        'PyYAML',
        'scikit_learn',
        'seaborn',
        'setuptools',
        'tensorboardX',
        'torch',
        'torch_geometric',
        'torch_scatter',
        'yacs'
    ],
    classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.9', 
  ],
    python_requires='>=3.6',
)
