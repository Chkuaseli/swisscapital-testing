# swisscapital-testing
swisscapital-testing
ვალიდაციები:
1) საქართველოს კონსტიტუციის მიხედვით არასრულწლოვან მომხმარებლებზე პირადობის დამადასტურებელი მოწმობა გაიცემა 4 წლის ვადით ხოლო თუ მომხმარგებელი სრულწლოვანია 10 წლის ვადით სწორედ ამის მიხედვით არის მომხმარებლის ასაკი და პერსონალური ბარათის გაცემისა და მოქმედების ვადები დამოკიდებული ერთმანეთზე.
2) პერსონალური ბარათის პირადი ნომერი უნდა შედგებოდეს 11 რიცხვისაგან;
3) პერსონალური ბარათის კოდის იგრძე უნდა იყოს 9-ის ტოლი რომელთაგან 3-4 ელემენტები ლათინური ციფრებისაგან შედგება დანარჩენი კი რიცხვებისაგან;
4) პერსონალური ბარათის ხელმოწერა შესაძლებელია სურათის ატვირთვით რომელსაც აქვს მხოლოდ სურათის ატვირთვის უფლება:FileAllowed ['jpg','png','jpeg','gif']
5) პერსონალური ბარათის მომხმარებლის სურათის მითითება სურათი ატვირთვით არის შესაძლებელი: FileAllowed ['jpg','png','jpeg','gif']
6) პერსონალური ბარათის მომხმარებლის ასაკის მითითება შესაძლებელია 1900 წლიდან დღევანდელ დღემდე;

EDIT:
რაც შეეხება განახლებას უნიკალური ინფორმაციის განახლება ავტორიზაციის გარეშე შორს წაგვიყვანს ამიტომ ასეთი მონაცემების განახლებისას აუცილებლად უნდა ვიყოთ ავტორიზირებული რადგნაც არსებულ მონაცემს ვერაფერს გავუტოლებთ სესიაში არარსებული იუზერით: პერსონალური ბარათის მომხმარებლის პირადი ნომრის და პერსონალური ბარათის კოდის რედაქტირება ავტორიზირებული სესიში მყოფი მომხმარებლისთვის მისი განახლება ამ ლოგიკის იქნება მაგალითად: 
     # card = User.query.filter_by(card_no = card_no.data).first()
        # if card != current_user.user.card_no:
        #     raise ValidationError('This Card ID already exist! 2')
        
        
        
 Project demonstracion on heroku server:
 >>>  https://swisscapital.herokuapp.com   <<<
