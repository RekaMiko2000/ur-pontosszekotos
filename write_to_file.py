
def write_to_file(coords_to_write:dict,filename):
    # base_x -> 1.ponté
    # base y -> 1. ponté
    # line x y z sorok
    # és itt nem is kell majd felemelni a filcet az egyes mozdulatok után, csak a legvégén
    # meg persze le kell vinni az elején
    # legyen először -0.1 a z, mert elv akkor még nem ér le a filc a lapra és így le lehet csekkolni jó helyen mozog-e egyeltalán
    file=open(filename,"w")
    file.write("time 3\n")
    file.write("x 0.158\n")
    file.write("y -0.2139\n")
    first=[]
    for x in coords_to_write:
        # először oda kell menni az első pont fölé a filccel azért szükséges ez a lépés
        if x==list(coords_to_write)[0]:
            first=coords_to_write[x]
            file.write(f"line {str(coords_to_write[x][0])} {str(coords_to_write[x][1])} -0.1\n")
        #ezután pedig már a lenti magasságban jöhet a rajzolás
        file.write(f"line {str(coords_to_write[x][0])} {str(coords_to_write[x][1])} -0.123\n") #később át kell írni z-t -0.116-ra
        if x==list(coords_to_write)[-1]:
            file.write(f"line {str(first[0])} {str(first[1])} -0.123\n")
            # fel kell emelni a tollat az utolsónál
            file.write(f"line {str(coords_to_write[x][0])} {str(coords_to_write[x][1])} -0.1\n")