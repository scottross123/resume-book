import gspread

gc = gspread.service_account(filename='../../secrets.json')

internships = gc.open('Resumes').worksheet("Internship")
fulltime = gc.open('Resumes').worksheet("Full-Time")

internships.append_row(['bruh', 'bruh2', 'bruh3', 'bruh4'])
