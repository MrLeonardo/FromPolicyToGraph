class ManageError:

    def __init__(self):
        self.GENERIC_ERROR = 1
        self.FILE_NOT_FOUND = 2
        self.FIREWALL_NOT_FOUND = 3
        self.ALGORITHM_NOT_FOUND = 4
        self.EMPTY_WIDTH = 5
        self.EMPTY_HEIGHT = 6

        self.errors = {
            self.GENERIC_ERROR: 'Si è verificato un errore',
            self.FILE_NOT_FOUND: 'Selezionare un file',
            self.FIREWALL_NOT_FOUND: 'Selezionare un firewall',
            self.ALGORITHM_NOT_FOUND: 'Selezionare un algoritmo',
            self.EMPTY_WIDTH: 'Inserire la larghezza',
            self.EMPTY_HEIGHT: 'Inserire l\'altezza'
        }

    def get(self, codeError):
        return self.errors[codeError]
