from django.shortcuts import render
# from django.core.mail import send_mail
from utils.email_utils import send_email
from django.conf import settings

def feedback(request):
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        message = "Phone :"+phone+"\n"+"Email :"+email+"\n"+"Message :"+request.POST["message"]
        print(send_email(f"Feedback Request from {name}", message,["accm8783@gmail.com"], use_secondary=False))
    
    return render(request, "support/feedback.html")


def team(request):
    print(request.method)
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        message = "Phone :"+phone+"\n"+"Email :"+email+"\n"+"Message :"+request.POST["message"]
        print(message)
        print(send_email(f"Support Request from {name}", message,["accm8783@gmail.com"], use_secondary=False))
    
    return render(request, "support/team.html")



# from django.shortcuts import render

# # from django.core.mail import send_mail

# from utils.email_utils import send_email

# from django.conf import settings



# def feedback(request):

#     if request.method == "POST":

#         name = request.POST["name"]

#         phone = request.POST["phone"]

#         email = request.POST["email"]

#         message = request.POST["message"]

#         send_email(f"Support Request from {name}", message,["accm8783@gmail.com"], use_secondary=True)

    

#     return render(request, "support/feedback.html")





# def team(request):

#     if request.method == "POST":

#         name = request.POST["name"]

#         phone = request.POST["phone"]

#         email = request.POST["email"]

#         message = request.POST["message"]

#         send_email(f"Support Request from {name}", message,["accm8783@gmail.com"], use_secondary=True)

    

#     return render(request, "support/team.html")


