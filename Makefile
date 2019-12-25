md=tuto_python_astro.md
pdf=$(md:.md=.pdf)

$(pdf) : $(md)
	pandoc --pdf-engine=xelatex $< -o $@

.PHONY : clean

clean :
	rm $(pdf) 2> /dev/null
