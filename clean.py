f = open("dumb_text.txt", "r", encoding="utf-8")
list_str = f.read().splitlines()
f.close
out_list = []
for line in list_str:
    if "Wie hilfreich war dieser Beitrag?" not in line and "Bitte bewerten Sie:" not in line and "Durchschnittliche Bewertung"\
            not in line and "Geben Sie die erste Bewertung!" not in line:
        out_list.append(line)
f = open("dumb_text_close.txt", "a", encoding="utf-8")
f.write("new \n")
f.write("\n".join(out_list))