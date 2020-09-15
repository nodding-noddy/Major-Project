'''
REPLACE THE DIRECTORY NAME AS PER YOUR COMPUTER
'''
import qrcode

def gen(name,branch):
    image = qrcode.make(name[0])
    name = name[0]
    image.save(f"/home/{REPLACE THIS WITH YOUR COMPUTER'S DIRECTORY}/Project Stud/stud/register/static/downloadable/{branch.lower()}/{name}.png","PNG")
