import setuptools

install_requires = [
    'pandas',
    'pybit==2.3.0',
    'python-binance==1.0.16',
]

setuptools.setup(
    name='cryptodataapi',
    version='0.0.1',
    author='Futurism Labs',
    author_email='futurismteam@gmail.com',
    py_modules=['cryptodataapi'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requires,
)