import bottle
from model import Sudoku


sudoku = Sudoku()

@bottle.get('/')
def zacetna_stran():
    sudoku = sudoku()
    return bottle.template('zacetna_stran', sudoku=sudoku)
    #napisemo ali bi igrali





bottle.run(debug=True, reloader=True)


