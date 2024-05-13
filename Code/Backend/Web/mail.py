from flask_mail import Message
from .packages import mail
from jinja2 import Environment, FileSystemLoader


# general function to either send mails to admin or the users 
def sendMail(RECEIVER_ADDRESS,SUBJECT,MESSAGE, creator_report=None):


    try:
       
        msg = Message(recipients=[RECEIVER_ADDRESS],
                    sender='ayshagrwl@gmail.com',
                    body=MESSAGE,
                    subject=SUBJECT)

        

        if creator_report:
            # Load the Jinja2 environment
            env = Environment(loader=FileSystemLoader('./Web/templates')) 

            # Load the HTML template
            template = env.get_template('report.html')  # Replace with your actual template file

            # Render the template with data
            rendered_html = template.render(users=creator_report)
            msg.html = rendered_html  # Set the HTML content of the email


        mail.send(msg)
        return True

    except Exception as e:
        print(e)
        return False
