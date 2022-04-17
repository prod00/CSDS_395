f = open("departments.sql", "w")

departmentList = """Accounting
African/African Amer Studies
Akkadian 
American Studies 
Anatomy 
Ancient Near East and Egypt
Anesthesiology 
Anthropology 
Arabic 
Art History 
Art 
Asian Studies 
Astronomy 
Banking & Finance 
Bioethics 
Biochemistry 
Biology 
Biosciences 
Business Law 
Biomedical Sciences Training Program 
Business Technology
Business Analytics & Intelligence
Chemistry
Chinese 
Childhood Studies Program 
Cell Biology 
Classics 
Clinical medicine - CCLCM 
Cancer Center 
Cognitive Science 
Patient Based Clinicl Cmprhnsv 
Communication Sciences 
Clinical Research Scholars Prg 
Computer and Data Sciences
Dance 
Doctor of Business Administration
Dentistry - Faculty 
Dentistry 
Design & Innovation 
Endodontics 
Oral Medicine 
Pediatric Dentistry 
Periodontics 
Dental Public Health 
Orthodontics 
Applied Data Science 
Disease Process 
Disease & Restoration of Hlth 
Biomedical Engineering 
Chemical Engineering 
Civil Engineering 
Economics 
Electrical, Computer, and Systems Engineering
Executive Doctor of Management 
Education
Earth, Environ & Planetary Sci 
Expanded Function Dental Aux 
Macromolecular/Polymer Science 
Mechanical & Aerospace Engr 
Executive MBA 
Materials Science & Engineering 
English 
Engineering Science 
Entrepreneurship 
Pract Oriented Engr Mast Prog 
Environmental Studies 
Ethnic Studies 
Examination Master/Ph.D.
Finance
French 
First Seminar Academic English 
First Seminar Common Curric 
First Seminar Cont Semester 
First Seminar Natural World 
First Seminar Social World 
First Seminar Symbolic World 
First Seminar Transfer Supplem 
Genetics 
Gerontological Studies 
Greek 
German 
Hebrew 
Health & Well-Being 
History & Philosophy of Sci
Health Systems Management 
History 
Humanities 
Health Disease and Processes 
Integrated Biological Sciences 
Integrated Biological Studies 
Interdisciplinary Health Sci
Inst for Integr of Mgmt & Engr 
Inquiry 
International Health 
International Studies 
Italian 
Japanese 
Judaic Studies 
Latin 
Law 
Leadership 
Lead Excel and Achievement Program
Law - Financial Integrity
Linguistics 
Maintenance of Health 
Mathematics 
MBA Core 
MBA Part Time Cohort 
Molecular Biol & Microbiology 
Management 
Schl of Med Graduate Education 
Information Systems 
Marketing 
Modern Foreign Lit & Mod Lang 
Military Science 
Molecular Medicine 
Public Health 
Positive Organizational Devel 
Med Scientist Training Program 
Applied Music 
Music, Audio Recording 
Music, Composition 
Music, Dalcroze/Eurhythmics 
Music, Education 
Music, Ensembles 
Music, General/Misc 
Music History 
Music Literature
Music, Pedagogy
Music, Repertoire
Music, Secondary Performance
Music Theory 
Molecular Virology Train Prog 
Neurosciences 
Nutrition 
Nursing Anesthesiology 
Nursing Education 
Master of Nursing 
Doctor of Nursing 
Nurse Practitioner 
Nursing 
Oral & Maxillofacial Surgery 
Operations Management 
Operations Research 
Organizational Behavior 
Origins 
Physician Assistant Studies 
Pathology 
Physical Education 
Philosophy 
Physiology & Biophysics 
Pharmacology 
Physics 
Management Policy 
Portuguese 
Political Science 
Population & Quant Health Sci 
Psychology 
Restoration of Health 
Restoration & Mainten of Hlth 
Regenerative Med Entrprnrshp 
Religious Studies 
Graduate Summer Research
Russian 
School of Applied Soc Sciences 
Supply Chain Management
Social Justice 
Sociology 
Spanish 
Statistics 
Systems Biology and Bioinform 
Theater Arts 
SAGES Capstone Experience 
University Studies 
Think About The Natural World 
Think About The Social World 
Think About The Symbolic World 
Washington Semester 
Women's & Gender Studies 
World Literature"""

import io
s = io.StringIO(departmentList)
for line in s:
    f.write("insert into applicase_departments values " + "(" + '\"' + line.strip() + '\"' + ")" + ";\n")
f.close()