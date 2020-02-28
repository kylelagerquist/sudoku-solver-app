import copy


class GameBoard:
    def __init__(self, cells_list):
        """
        An instance of a sudoku game board
        @param cells_list: Nested list of integers between 0 and 9. 0 represents a blank cell.
        """
        # List of cell values must have 9 rows
        if len(cells_list) != 9:
            raise ValueError('{} is an invalid row amount. Game board must have 9 rows.'.format(len(cells_list)))
        # Iterate through each row
        for row_ind in range(9):
            # Each row must have exactly 9 values, one for each column
            if len(cells_list[row_ind]) != 9:
                raise ValueError('{} is an invalid column amount in row {}. '
                                 'Rows must have 9 columns.'.format(len(cells_list[row_ind]), row_ind))

        # Change the nested list of integers into a nested list of Cells
        self.cells_list = [[Cell(cells_list[row_ind][col_ind], row_ind, col_ind)
                            for col_ind in range(9)] for row_ind in range(9)]
        # Add all possible value options for blank cells
        self.set_options()

    def __str__(self):
        """
        Overriding the default python string message to print the game board
        @return: A string representation of the game board
        """
        board_format = ""
        # Iterate through each row
        for row in self.cells_list:
            # Iterate through each cell
            for cell in row:
                # Add the cell value to the game board string
                board_format += str(cell.number) + " "
            # Add a new line after every row
            board_format += "\n"

        return board_format

    def __eq__(self, other):
        """
        Overriding the default python equivalent function for this class
        @param other: A object being compared to this game board
        @return: Whether the two objects are both game boards with all the same cell values and cell options
        """
        # Ensure the other instance is a game board
        if not isinstance(other, GameBoard):
            return False

        # Loop through each row
        for row in self.cells_list:
            # Loop through each col
            for cell in row:
                # Get the corresponding cell from the other game board
                that_cell = other.cells_list[cell.row_ind][cell.col_ind]
                # If any cell is not equal to its corresponding cell, the game boards are not equal
                if cell != that_cell:
                    return False
        return True

    def solve(self):
        """
        Solves the game board
        @return:
        """
        first_try = True
        # Create initial copy
        previous = copy.deepcopy(self)
        print(self)

        # Check if the last pass of solving changed anything
        while first_try or self != previous:
            if first_try:
                first_try = False
            # Update the copy of the board
            previous = copy.deepcopy(self)
            # Attempt to solve the board
            self.strategy_basic()

        print(self)

        if self.game_over():
            print('BOARD WAS SOLVED!')
        else:
            for row in self.cells_list:
                for cell in row:
                    print(cell.options)
            print('board was unable to be solved.')

        self.to_html()

    def set_options(self):
        """
        Sets all possible values for each cell
        @return: Void, just updates all of the options
        """
        # Loop through each row
        for row in self.cells_list:
            # Loop through each col
            for cell in row:
                # Skip this cell if it already has a value
                if not cell.filled:
                    # Loop through all possible values
                    for option in range(1, 10):
                        if cell.col_ind == 5 and cell.row_ind == 0:
                            """
                            print(option, self.val_in_row(option, cell.row_ind), self.val_in_col(option, cell.col_ind),
                                  self.val_in_region(option, cell.row_ind, cell.col_ind))
                                  """
                        # If the value is not in the current row, column, or region, add it as a possible option
                        if not self.val_in_row(option, cell.row_ind) and \
                                not self.val_in_col(option, cell.col_ind) and \
                                not self.val_in_region(option, cell.row_ind, cell.col_ind):
                            cell.add_option(option)

    def strategy_basic(self):
        """
        Fills is all of the cells that only have one possible option
        @return: Void, just updates the cell values
        """
        # Loop through each region row
        for row in self.cells_list:
            # Loop through each region col
            for cell in row:
                # continue if cell is already filled
                if not cell.filled:
                    for option in cell.options:
                        if len(cell.options) == 1:
                            self.fill_in_cell(cell, cell.options[0])
                            break
                        elif self.count_val_in_row_options(option, cell.row_ind) == 1:
                            self.fill_in_cell(cell, option)
                            break
                        elif self.count_val_in_col_options(option, cell.col_ind) == 1:
                            self.fill_in_cell(cell, option)
                            break
                        elif self.count_val_in_region_options(option, cell.row_ind, cell.col_ind) == 1:
                            self.fill_in_cell(cell, option)
                            break

    def strategy_clear_options(self, row):
        locks = []
        pairs = []
        # Loop through each region row
        for cell in row:
            if not cell.filled and len(cell.options) == 2:
                if cell.options not in pairs:
                    pairs.append(cell.options)
                else:
                    pairs.remove(cell.options)
                    locks.append(cell.options)

        for cell in row:
            if not cell.filled and cell.options not in locks:
                print(1)



    def game_over(self):
        """
        The game is over if all cells are filled
        @return: Boolean on whether there are no cells unfilled
        """
        # Loop through each row
        for row in self.cells_list:
            # Loop through each col
            for cell in row:
                if not cell.filled:
                    return False
        return True

    def unsolvable(self):
        """
        The board is unsolvable if any cell is not filled in and has no possible options remaining for it
        @return: Boolean for whether the board is unsolvable
        """
        # Loop through each row
        for row in self.cells_list:
            # Loop through each col
            for cell in row:
                if not cell.filled and len(cell.options) == 0:
                    return True
        return False

    def fill_in_cell(self, cell_to_change, new_value):
        # Set value
        cell_to_change.change_number(new_value)
        # Clear options
        cell_to_change.options = []
        # Set filled
        cell_to_change.filled = True
        # Iterate through all cells in its row
        for other_cell in self.get_row(cell_to_change.row_ind):
            # If cell is blank and this value was an option, remove it
            if not other_cell.filled and new_value in other_cell.options:
                other_cell.remove_option(new_value)
        # Iterate through all the cells in its column
        for other_cell in self.get_col(cell_to_change.col_ind):
            # If cell is blank and this value was an option, remove it
            if not other_cell.filled and new_value in other_cell.options:
                other_cell.remove_option(new_value)
        # Iterate through all the cells in its region
        for other_cell in self.get_region(cell_to_change.row_ind, cell_to_change.col_ind):
            # If cell is blank and this value was an option, remove it
            if not other_cell.filled and new_value in other_cell.options:
                other_cell.remove_option(new_value)

    def val_in_row(self, value, row_ind):
        row_values = [cell.number for cell in self.get_row(row_ind)]
        return value in row_values

    def val_in_col(self, value, col_ind):
        col_values = [cell.number for cell in self.get_col(col_ind)]
        return value in col_values

    def val_in_region(self, value, row_ind, col_ind):
        region_values = [cell.number for cell in self.get_region(row_ind, col_ind)]
        return value in region_values

    def count_val_in_row_options(self, value, row_ind):
        row_options = [cell.options.count(value) for cell in self.get_row(row_ind)]
        return row_options.count(1)

    def count_val_in_col_options(self, value, col_ind):
        col_options = [cell.options.count(value) for cell in self.get_col(col_ind)]
        return col_options.count(1)

    def count_val_in_region_options(self, value, row_ind, col_ind):
        region_options = [cell.options.count(value) for cell in self.get_region(row_ind, col_ind)]
        return region_options.count(1)

    def get_row(self, row_ind):
        if row_ind not in range(9):
            raise ValueError('Not able to get row. {} is not valid row index.'.format(row_ind))
        return self.cells_list[row_ind]

    def get_col(self, col_ind):
        if col_ind not in range(9):
            raise ValueError('Not able to get column. {} is not valid column index.'.format(col_ind))
        return [row[col_ind] for row in self.cells_list]

    def get_region(self, row_ind, col_ind, as_flat=True):
        if row_ind not in range(9) or col_ind not in range(9):
            raise ValueError('Not able to get region. {} or {} is not a valid index.'.format(row_ind, col_ind))
        region_start_row = row_ind // 3 * 3
        region_end_row = row_ind // 3 * 3 + 3
        region_start_col = col_ind // 3 * 3
        region_end_col = col_ind // 3 * 3 + 3
        region_rows = self.cells_list[region_start_row: region_end_row]
        region = [row[region_start_col: region_end_col] for row in region_rows]

        if as_flat:
            return [cell for rows in region for cell in rows]
        else:
            return region

    def to_html(self):
        html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Sudoku</title>'
        html += '<style>td.top {border-top:3pt solid black;} td.bottom {border-bottom:3pt solid black;} ' \
                'td.left {border-left:3pt solid black;} td.right {border-right:3pt solid black;} ' \
                'td.topleft {border-top:3pt solid black; border-left:3pt solid black;} ' \
                'td.topright {border-top:3pt solid black; border-right:3pt solid black;}' \
                'td.bottomleft {border-bottom:3pt solid black; border-left:3pt solid black;} ' \
                'td.bottomright {border-bottom:3pt solid black; border-right:3pt solid black;}' \
                'table {border-collapse: collapse;}</style></head><body>'
        html += '<table border="1" border-collapse="collapse">'
        for row in self.cells_list:
            row_html = '<tr>'
            for cell in row:
                if cell.filled:
                    row_html += '{}<font color="red">{}</font></td>'.format(self.to_html_helper(cell), cell.number)
                else:
                    row_html += '{}{}</td>'.format(self.to_html_helper(cell), cell.options)
            html += row_html + '</tr>'
        html += '</table></body></html>'

        html_file = open('sudoku.html','w')
        html_file.write(html)
        html_file.close()
    
    @staticmethod
    def to_html_helper(cell):
        td_class = ""
        if cell.row_ind == 0:
            td_class += 'top'
        elif cell.row_ind in (2, 5, 8):
            td_class += 'bottom'

        if cell.col_ind == 0:
            td_class += 'left'
        elif cell.col_ind in (2, 5, 8):
            td_class += 'right'

        return '<td width="50" height="50" align="center" class="{}">'.format(td_class)







class Cell:
    def __init__(self, number, row_ind, col_ind):
        if number not in range(10):
            raise ValueError('{} is not a valid cell value.'.format(number))
        if row_ind not in range(9):
            raise ValueError('{} is not a valid cell row.'.format(row_ind))
        if col_ind not in range(9):
            raise ValueError('{} is not a valid cell column.'.format(col_ind))

        self.number = number
        self.row_ind = row_ind
        self.col_ind = col_ind
        self.filled = False
        self.options = []

        if number != 0:
            self.filled = True

    def __str__(self):
        if self.filled:
            return "Number: {} | Row: {} | Column: {}".format(self.number, self.row_ind + 1, self.col_ind + 1)
        else:
            return "Blank | Options: {} | Row: {} | Column: {}".format(self.options, self.row_ind + 1, self.col_ind + 1)

    def __eq__(self, other):
        return self.number == other.number and self.options == other.options

    def change_number(self, value):
        """
        Changes
        @param value: 
        @return: 
        """
        if value not in range(1, 10):
            raise ValueError('{} is not a valid cell value.'.format(value))
        else:
            self.number = value

    def remove_option(self, value):
        """
        Removes a value from this cells list of options
        @param value: integer between 1-9 to be removed from option list
        @return: Void
        """
        if value not in self.options:
            raise ValueError('{} cannot be removed because it it not an option.'.format(value))
        else:
            self.options.remove(value)

    def add_option(self, value):
        """
        Adds a value to this cells options, throws error if it is not a valid option
        @param value: integer between 1-9 to be added to option list
        @return: Void
        """
        if value not in range(1, 10):
            raise ValueError('{} is not a valid cell value to be added as an option'.format(value))
        else:
            self.options.append(value)
            self.options.sort()


board1 = [[0, 0, 1, 9, 8, 4, 7, 6, 0],
          [6, 0, 9, 0, 5, 7, 3, 8, 0],
          [8, 2, 7, 0, 1, 0, 0, 0, 0],
          [9, 6, 0, 3, 0, 8, 1, 0, 5],
          [1, 8, 5, 0, 2, 0, 0, 7, 3],
          [3, 0, 0, 0, 0, 0, 2, 0, 8],
          [2, 1, 0, 0, 0, 0, 0, 3, 6],
          [0, 0, 0, 1, 0, 0, 0, 0, 4],
          [0, 9, 6, 0, 0, 2, 5, 1, 0]]

board2 = [[0, 1, 0, 0, 6, 0, 0, 7, 2],
          [0, 5, 0, 0, 9, 0, 0, 0, 8],
          [0, 8, 0, 0, 0, 0, 0, 0, 1],
          [0, 0, 8, 0, 1, 9, 0, 0, 0],
          [0, 0, 2, 0, 0, 4, 5, 0, 0],
          [4, 0, 0, 6, 8, 5, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 1, 7],
          [8, 0, 0, 4, 0, 0, 0, 6, 0],
          [0, 0, 6, 8, 0, 0, 0, 0, 0]]

board2 = [[0,3,0,0,0,0,0,0,0],
          [0,0,0,0,0,8,0,1,0],
          [5,0,0,0,0,0,7,3,4],
          [0,0,0,0,0,0,0,0,0],
          [0,1,0,6,0,7,0,0,0],
          [4,0,0,0,0,0,5,0,8],
          [0,0,6,8,9,0,0,0,0],
          [3,0,0,0,2,0,0,0,0],
          [0,7,1,0,0,5,9,0,6]]
game = GameBoard(board2)
game.solve()
# region_values111 = [cell.number for cell in game.get_region(4, 4)]
# print(region_values111)
