git clone --depth 1 https://github.com/lacus-w/spark-page.git .
git fetch origin --force --prune --prune-tags --depth 50
cat .readthedocs.yaml
asdf global python 3.8.18
python -mvirtualenv $READTHEDOCS_VIRTUALENV_PATH
python -m pip install --upgrade --no-cache-dir pip setuptools
python -m pip install --upgrade --no-cache-dir sphinx readthedocs-sphinx-ext
python -m pip install --upgrade --upgrade-strategy only-if-needed --no-cache-dir .

# rst to myst
pip install "rst-to-myst[sphinx]"
rst2myst convert docs/**/*.rst
rst2myst convert --config myst.yaml docs/**/*.rst

# md to myst
python -m pip install myst_parser
pip install myst-parser

pip install sphinx-book-theme
