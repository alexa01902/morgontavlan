
def log_mood():
    humör = mood_combobox.get()
    with open(FIL, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()},{humör}\n")

    update_mood_plot()



  # Variabel för att hålla referensen till det nuvarande diagrammet
 

 
 
def las_data(filnamn):
    """Läser csv-filen.
 
    Excel på svenska sparar csv med semikolon som avgränsare och decimalkomma,
    därför sep=";" och decimal=",". Om åäö blir konstiga tecken, prova
    encoding="cp1252" (Windows) i stället för standardvärdet utf-8.
    """
    return pd.read_csv(filnamn, sep=",")
 
 
def skapa_stapeldiagram(df):
    """Bygger ett stapeldiagram och returnerar figuren.
    
    
    KOLUMN = "mood"
 
    Vi använder Figure direkt och inte plt.subplots(). Då hamnar diagrammet
    bara i vårt tkinter-fönster och matplotlib försöker inte öppna ett eget.
    """
    figur = Figure(figsize=(7, 4), dpi=100)
    ax = figur.add_subplot(111)
    ax.bar(df[KOLUMN].value_counts().index, df[KOLUMN].value_counts().values, color="#FCE8E6"   )
 
    ax.set_title("Humörfördelning")
    ax.set_xlabel("Humör")
    ax.set_ylabel("Antal")
    figur.tight_layout()
    return figur

def update_mood_plot():
    try:

        df = las_data(FIL)

        # Rita om diagrammet baserat på den nya datan
        figur = skapa_stapeldiagram(df)

        # Uppdatera canvas
        canvas = FigureCanvasTkAgg(figur, master=canvas_frame)
        tk_widget = canvas.get_tk_widget()
        tk_widget.grid(row=0, column=0,  padx=20, pady=20, sticky="nsew")

    except FileNotFoundError:
        print(f"Hittade inte filen {FIL}.")

