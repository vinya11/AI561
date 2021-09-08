
def getInput():
    board =list()
    blackCount =0
    whiteCount =0
    whiteKings=0
    blackKings=0
    with open("input.txt",'r') as f:
        lines = f.read().splitlines()
    gameType = lines[0]
    pieceColor = lines[1]
    timeInSecs = lines[2]
    for rows in lines[3:]:
        board.append(list(rows.rstrip(' ')))
    for r in board:
        blackCount+=r.count('b')
        blackKings+=r.count('B')
        whiteCount+=r.count('w')
        whiteKings+=r.count('W')
    
    return board,gameType,pieceColor,timeInSecs,blackCount,blackKings,whiteCount,whiteKings
def print_output(init,path,is_jump):
    char_index = "abcdefgh"
    f = open("output.txt",'w')

    init =  char_index[init[1]] + str(8-init[0])
    if is_jump:
        output_str =""
        for cells in range(0,len(path)):
            
            out1 = char_index[path[cells][1]]
            out2 = str(8-path[cells][0])
            output_str += (f"J {init} {out1}{out2}\n")
            # f.write(output_str+"\n")
            init = out1+out2
    else:
        out1 = char_index[path[1]]
        out2 = str(8-path[0])
        output_str = f"E {init} {out1}{out2}"
    f.write(output_str.rstrip("\n"))

    f.close()
            

