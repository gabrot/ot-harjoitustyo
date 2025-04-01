class ThemeColors:
    """Sovelluksen teemavärit"""
    PRIMARY = "#ec5f5f"
    PRIMARY_LIGHT = "#ec5f5f"
    SECONDARY = "#ec5f5f"
    BACKGROUND = "#ffffff"
    CARD_BG = "#ffffff"
    TEXT_PRIMARY = "#343a40"
    TEXT_SECONDARY = "#6c757d"
    BORDER = "#dee2e6"
    SUCCESS = "#28a745"
    ERROR = "#ec5f5f"
    INFO_BG = "#ffffff"


class ThemeFonts:
    """Sovelluksen fontit"""
    TITLE = ("Helvetica", 18, "bold")
    HEADER = ("Helvetica", 14, "bold")
    BODY = ("Helvetica", 12)
    BODY_SMALL = ("Helvetica", 10)
    BUTTON = ("Helvetica", 12)
    LABEL = ("Helvetica", 12)
    INFO = ("Helvetica", 11)


def setup_styles(style):
    """Asettaa sovelluksen tyylit
    
    Args:
        style: ttk.Style olio
    """
    # Pudotusalueen tyylit
    style.configure(
        "DropArea.TFrame", 
        background=ThemeColors.CARD_BG,
        relief="solid",
        borderwidth=1,
        bordercolor=ThemeColors.BORDER
    )
    
    style.configure(
        "DropAreaHover.TFrame", 
        background=ThemeColors.CARD_BG,
        relief="solid",
        borderwidth=1,
        bordercolor=ThemeColors.PRIMARY
    )
    
    style.configure(
        "DropText.TFrame", 
        background=ThemeColors.CARD_BG
    )
    
    style.configure(
        "DropText.TLabel", 
        background=ThemeColors.CARD_BG,
        foreground=ThemeColors.TEXT_PRIMARY,
        font=ThemeFonts.BODY
    )
    
    style.configure(
        "DropTextSecondary.TLabel", 
        background=ThemeColors.CARD_BG,
        foreground=ThemeColors.TEXT_SECONDARY,
        font=ThemeFonts.BODY_SMALL
    )
    
    style.configure(
        "Browse.TButton",
        background=ThemeColors.SECONDARY,
        foreground="white",
        font=ThemeFonts.BUTTON
    )
    # Yleiset tyylit
    style.configure(
        "TFrame", 
        background=ThemeColors.BACKGROUND
    )
    
    style.configure(
        "Main.TFrame", 
        background=ThemeColors.BACKGROUND
    )
    
    style.configure(
        "TLabel", 
        background=ThemeColors.BACKGROUND,
        foreground=ThemeColors.TEXT_PRIMARY,
        font=ThemeFonts.BODY
    )
    
    # Otsikkotyyli
    style.configure(
        "Title.TLabel", 
        font=ThemeFonts.TITLE,
        background=ThemeColors.BACKGROUND,
        foreground=ThemeColors.TEXT_PRIMARY
    )
    
    # Tiedostoinfo
    style.configure(
        "InfoFrame.TFrame", 
        background=ThemeColors.CARD_BG,
        relief="flat",
        borderwidth=1
    )
    
    style.configure(
        "FileInfo.TLabel", 
        background=ThemeColors.CARD_BG,
        foreground=ThemeColors.TEXT_PRIMARY,
        font=ThemeFonts.BODY
    )
    
    # Tilavalitsin
    style.configure(
        "ModeSelector.TFrame", 
        background=ThemeColors.BACKGROUND
    )
    
    style.configure(
        "ModeLabel.TLabel", 
        background=ThemeColors.BACKGROUND,
        foreground=ThemeColors.TEXT_PRIMARY,
        font=ThemeFonts.HEADER
    )
    
    # Tilavalitsimen painikkeet
    style.configure(
        "ModeButton.TButton",
        background=ThemeColors.CARD_BG,
        foreground=ThemeColors.TEXT_PRIMARY,
        font=ThemeFonts.BUTTON,
        relief="flat",
        borderwidth=0
    )
    
    style.configure(
        "ModeButtonActive.TButton",
        background=ThemeColors.PRIMARY,
        foreground="white",
        font=ThemeFonts.BUTTON,
        relief="flat",
        borderwidth=0
    )
    
    # Aluenäkymän tyylit
    style.configure(
        "RangesFrame.TFrame", 
        background=ThemeColors.BACKGROUND
    )
    
    style.configure(
        "RangeLabel.TLabel", 
        background=ThemeColors.BACKGROUND,
        foreground=ThemeColors.TEXT_PRIMARY,
        font=ThemeFonts.BODY
    )
    
    style.configure(
        "RangeIndex.TLabel", 
        background=ThemeColors.BACKGROUND,
        foreground=ThemeColors.TEXT_PRIMARY,
        font=ThemeFonts.HEADER
    )
    
    # Infolaatikko
    style.configure(
        "InfoBox.TFrame", 
        background=ThemeColors.INFO_BG,
        relief="flat",
        borderwidth=0
    )
    
    style.configure(
        "InfoText.TLabel", 
        background=ThemeColors.INFO_BG,
        foreground=ThemeColors.TEXT_PRIMARY,
        font=ThemeFonts.INFO
    )
    
    # Toimintopainikkeet
    style.configure(
        "Action.TButton",
        background=ThemeColors.PRIMARY,
        foreground="white",
        font=ThemeFonts.BUTTON,
        relief="flat",
        padding=10
    )
    
    style.configure(
        "AddRange.TButton",
        background=ThemeColors.CARD_BG,
        foreground=ThemeColors.PRIMARY,
        font=ThemeFonts.BODY,
        relief="flat",
        borderwidth=1
    )
    
    style.configure(
        "DeleteRange.TButton",
        background=ThemeColors.BACKGROUND,
        foreground=ThemeColors.ERROR,
        font=ThemeFonts.BODY,
        relief="flat",
        padding=0
    )
    
    # Statusnäkymä
    style.configure(
        "StatusFrame.TFrame", 
        background=ThemeColors.BACKGROUND
    )
    
    style.configure(
        "Status.TLabel", 
        background=ThemeColors.BACKGROUND,
        foreground=ThemeColors.TEXT_PRIMARY,
        font=ThemeFonts.BODY
    )
    
    # Header
    style.configure(
        "Header.TFrame", 
        background=ThemeColors.BACKGROUND
    )
    
    style.configure(
        "HeaderTitle.TLabel", 
        background=ThemeColors.BACKGROUND,
        foreground=ThemeColors.TEXT_PRIMARY,
        font=ThemeFonts.TITLE
    )
    
    style.configure(
        "HeaderSubtitle.TLabel", 
        background=ThemeColors.BACKGROUND,
        foreground=ThemeColors.TEXT_SECONDARY,
        font=ThemeFonts.BODY
    )