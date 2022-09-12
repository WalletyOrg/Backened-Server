import requests
from keys import *



# join ###############################################################################################################################################################################

def joinForm(form_name, form_role, form_email, form_project, form_website, form_net, form_comments):

    def submit_form_telegram(form_name, form_role, form_email, form_project, form_website, form_net, form_comments):
        message = f'** NEW PROJECT SUBMISSION **\n\nTeam Name: {form_project}\nWebsite: {form_website}\nNet: {form_net}\n' \
                  f'Name: {form_name}\nRole: {form_role}\nEmail: {form_email}\nComments: {form_comments}'
        requests.get(f'https://api.telegram.org/bot{telegram_api_key}/sendMessage?chat_id={telegram_chat_id_core}&text={message}')
        return None
    submit_form_telegram(form_name, form_role, form_email, form_project, form_website, form_net, form_comments)

    def submit_form_email(form_name, form_email, form_project):
        try:
            body = f'\nHello {form_name} !\n\n' \
                   f'Thank you very much for being interested in {form_project} joining Wallety.org, if we are ' \
                   f'interested in going further we will email you back ASAP with a time to meet.\n' \
                   f'\nWe hope you have a great day and thanks again, \nWallety.org Auto Reply'
            subject = f'Wallety.org | {form_project}'
            import smtplib
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(email_user, email_pass)
            header = 'To:' + form_email + '\n' + 'From: ' + email_user + '\n' + f'Subject:{subject} \n'
            msg = header + f'{body}'
            smtpserver.sendmail(email_user, form_email, msg)
            smtpserver.quit()
            return None
        except:
            return None
            pass
    submit_form_email(form_name, form_email, form_project)





# suggestion ###############################################################################################################################################################################

def suggestion(message, network, email, suggest_type):
    user_message = message
    message = f'** NEW {suggest_type} **\n\nNetwork: {network}\n' \
              f'Type: {suggest_type}\n' \
              f'Email: {email}\n' \
              f'Suggestion: {message}'
    requests.get(f'https://api.telegram.org/bot{telegram_api_key}/sendMessage?chat_id={telegram_chat_id_core}&text={message}')

    def suggest_email(email, suggest_type, user_message):
        try:
            body = f'\nHey there !\n\n' \
                   f'Thank you very much for reporting the {suggest_type}:\n\n' \
                   f'\"{user_message}\"\n\n' \
                   f'We have been notified and will look into it.\n' \
                   f'\nWe hope you have a great day and thanks again, \nWallety.org Auto Reply'
            subject = f'Wallety.org | {suggest_type}'
            import smtplib
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(email_user, email_pass)
            header = 'To:' + email + '\n' + 'From: ' + email_user + '\n' + f'Subject:{subject} \n'
            msg = header + f'{body}'
            smtpserver.sendmail(email_user, email, msg)
            smtpserver.quit()
            return None
        except:
            return None
            pass

    if email != False:
        suggest_email(email, suggest_type, user_message)
    return None




# api apply ###############################################################################################################################################################################

def apiApply(name, email, comments):
    message_clean = f'New API apply\n\nName: {name}\nEmail: {email}\nComments: {comments}'
    requests.get(f'https://api.telegram.org/bot{telegram_api_key}/sendMessage?chat_id={telegram_chat_id_api}&text={message_clean}')

    def api_email(name, email):
        try:
            body = f'\nHey {name} !\n\n' \
                   f'Thank you very much for applying for our API, we will let you know once it is live !\n' \
                   f'\nWe hope you have a great day and thanks again, \nWallety.org Auto Reply'
            subject = 'Wallety.org | API'
            import smtplib
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(email_user, email_pass)
            header = 'To:' + email + '\n' + 'From: ' + email_user + '\n' + f'Subject:{subject} \n'
            msg = header + f'{body}'
            smtpserver.sendmail(email_user, email, msg)
            smtpserver.quit()
            return None
        except:
            return None
            pass

    api_email(name, email)
