from pathlib import Path
p=Path('out/write_reading.py');s=p.read_text();s=s.replace('21,27,33,39,45','21,27,(1133,2836.5,6,\'Quarter-circle crossed by 25-psi and .08-in gridlines; exposed outline supplies center.\'),39,45');s=s.replace('fitted v=1582.26','fitted v=1582.34');p.write_text(s)
