markdowns = tuto_python_astro.md
texs = $(markdowns:.md=.tex)
pdfs = $(markdowns:.md=.pdf)

# Pandoc options --------------------------------------------------------------
tex_template = template.latex
pd_options = --toc
pd_options += --filter=latex_minted.py 

# Latex options ---------------------------------------------------------------
latex_engine = xelatex
latex_engine_opt = -shell-escape # for minted
latex_temps = *.aux *.log *.out *.toc *.pyg *.mintedcmd

# Rules -----------------------------------------------------------------------
all : pdf
pdf : $(pdfs)
tex : $(texs)

%.tex : %.md
	pandoc -s -f markdown -t latex --template=$(tex_template) $(pd_options) $< -o $@

%.aux : %.tex
	$(latex_engine) $(latex_engine_opt) $<

%.pdf : %.tex %.aux
	$(latex_engine) $(latex_engine_opt) $<

.PHONY : clean

clean :
	@echo "Removing side products..."
	@rm $(texs) $(latex_temps) 2> /dev/null || echo
	@rm -r _minted-* 2> /dev/null || echo

cleanall : clean
	@echo "Removing final products..."
	@rm $(pdfs) 2> /dev/null || echo
