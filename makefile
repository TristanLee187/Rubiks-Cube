run:
	@python3 main.py $(ARGS)

help:
	@echo Hello there!
	@echo This virtual Rubik\'s Cube supports the following:
	@echo 1: Scrambling:
	@echo "   generate a random scramble. prints the resulting scramble as well:"
	@echo "      make ARGS=\"random n\", where n is the length of the desired scramble"
	@echo "   feed a scramble in cube notation from a text file. prints the scramble as well:"
	@echo "      make ARGS=\"read filename\""
	@echo "   feed the colors of each of the cube\'s stickers in a flat layout from a text file:"
	@echo "      make ARGS=\"see filename\""
	@echo "   After the scramble is processed, the resulting cube is printed in a flat layout"
	@echo