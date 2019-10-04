SPHINXOPTS	?=
SPHINXBUILD	?= sphinx-build
SOURCEDIR	= ./
BUILDDIR	= _build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# https://github.com/GaretJax/sphinx-autobuild#user-content-makefile-integration
livehtml:
	sphinx-autobuild -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
