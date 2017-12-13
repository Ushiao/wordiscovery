"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
#with open(path.join(here, 'README.md')) as f:
    #long_description = f.read()
long_description = """
词频、互信息、信息熵发现中文新词
================================

**新词发现**\ 任务是中文自然语言处理的重要步骤。\ **新词**\ 有“新”就有“旧”，属于一个相对个概念，在相对的领域（金融、医疗），在相对的时间（过去、现在）都存在新词。\ `文本挖掘 <https://zh.wikipedia.org/wiki/文本挖掘>`__\ 会先将文本\ `分词 <https://zh.wikipedia.org/wiki/中文自动分词>`__\ ，而通用分词器精度不过，通常需要添加\ **自定义字典**\ 补足精度，所以发现新词并加入字典，成为文本挖掘的一个重要工作。

`单词 <https://zh.wikipedia.org/wiki/單詞>`__\ 的定义，来自维基百科的定义如下：

    在语言学中，\ **单词**\ （又称为词、词语、单字；英语对应用语为“word”）是能独立运用并含有语义内容或语用内容（即具有表面含义或实际含义）的最小单位。单词的集合称为词汇、术语，例如：所有中文单词统称为“中文词汇”，医学上专用的词统称为“医学术语”等。词典是为词语提供音韵、词义解释、例句、用法等等的工具书，有的词典只修录特殊领域的词汇。

单从语义角度，“苹果“的法语是”pomme”，而“土豆”的法语是“pomme de
terre”，若按上面的定义，“土豆”是要被拆的面目全非，但“pomme de
terre”是却是表达“土豆”这个语义的最小单位；在机构名中，这类问题出现的更频繁，“Paris
3”是“巴黎第三大学”的简称，如果“Paris”和“3”分别表示地名和数字，那这两个就无法表达“巴黎第三大学”的语义。而中文也有类似的例子，“北京大学”的”北京“和”大学“都可以作为一个最小单位来使用，分别表示”地方名“和“大学”，如果这样分词，那么就可以理解为“北京的大学”了，所以“北京大学”是一个表达语义的最小单位。前几年有部电影《夏洛特烦恼》，我们是要理解为“夏洛特
烦恼“还是”夏洛 特 烦恼“，这就是很经典的分词问题。

但是从语用角度，这些问题似乎能被解决，我们知道“pomme de
terre”在日常生活中一般作为“土豆”而不是“土里的苹果”，在巴黎学习都知道“Paris
3”，就像我们提到“北京大学”特指那所著名的高等学府一样。看过电影《夏洛特烦恼》的观众很容易的就能区分这个标题应该看为“夏洛
特 烦恼”。

发现新词的方法，《\ `互联网时代的社会语言学：基于SNS的文本数据挖掘 <http://www.matrix67.com/blog/archives/5044%5D>`__
》一文，里面提到的给每一个文本串计算\ **文本片段**\ 的\ **凝固程度**\ 和文本串对外的使用\ **自由度**\ ，通过设定阈值来将文本串分类为词和非词两类。原文给了十分通俗易懂的例子来解释凝固度和自动度。这里放上计算方法。这个方法还有许多地方需要优化，在之后的实践中慢慢调整了。

环境
----

::

    python >= 3.5

安装
----

.. code:: bash

    python setup.py install

使用说明
--------

.. code:: python

    import wordiscovery as wd

    text = "新词发现任务是中文自然语言处理的重要步骤。
    新词有新就有旧，属于一个相对个概念，在相对的领域（金融、医疗），
    在相对的时间（过去、现在）都存在新词。文本挖掘会先将文本分词，
    而通用分词器精度不过，通常需要添加自定义字典补足精度，
    所以发现新词并加入字典，成为文本挖掘的一个重要工作。
    "

    f = wd.Wordiscovery()

    # 解析过程默认参数, 根据文本自由调节这几个阈值
    # 最小信息熵0.01
    # 最小互信息4
    # 最小词频2
    f.parse(text)  # f.parse(text, 0.01, 4, 2)
    # {'分词': (2, 5.18271944179699, 0.6931471805599453),
    # '字典': (2, 6.2813317304651, 0.6931471805599453),
    # '文本': (3, 4.895037369345209, 0.6365141682948128),
    # '文本挖掘': (2, 5.588184549905154, 0.6931471805599453),
    # '新词': (4, 4.371789225580661, 1.0397207708399179),
    # '相对': (3, 4.3842117455792184, 0.6365141682948128),
    # '精度': (2, 6.2813317304651, 0.6931471805599453),
    # '通常': (2, 5.18271944179699, 0.6931471805599453),
    # '重要': (2, 5.028568761969732, 0.6931471805599453),
    # '需要': (2, 5.028568761969732, 0.6931471805599453),
    # '领域': (2, 6.2813317304651, 0.6931471805599453)}

详细说明
--------

`wordicovery解释 <https://github.com/Ushiao/wordiscovery/blob/master/docs/wordiscovery.ipynb>`__
"""

setup(
    name='wordiscovery',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.4.6',

    description='A Chinese new word discovery',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/ushiao/wordiscovery',

    # Author details
    author='Kun JIN',
    author_email='jin.kun@flykun.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%4Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='NLP, new word discorvery',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    #packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    #packages=["wordiscovery"],
    py_modules=["wordiscovery"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    #install_requires=[
    #        'six==1.11.0'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
#     package_data={
    #    'tagword': ['*.*', 
    #                'tokenizer/*', 
    #                'tokenizer/models/*', 
    #                'tokenizer/data/*', 
    #                ],
    #},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
#    data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
#    entry_points={
#        'console_scripts': [
#            '=sample:main',
#        ],
#    },
)
