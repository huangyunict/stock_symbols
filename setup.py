from distutils.core import setup
import setuptools

setup(
    name='stock_symbols',
    version='0.5.2',
    packages=['stock_symbols'],
    author='Yun Huang',
    author_email='huangyunict@gmail.com',
    description='Retrieves list of all symbols present in SP500, NASDAQ, AMEX and NYSE',
    url='https://github.com/huangyunict/stock_symbols',
    download_url='http://pypi.python.org/pypi/stock_symbols',
    keywords='stocks stockmarket yahoo finance SP500 NASDAQ AMEX NYSE'.split(),
    license='GNU LGPLv2+',
    install_requires=[
        "beautifulsoup4 >= 4.2.1"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial :: Investment',
    ]
)
