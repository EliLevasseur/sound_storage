from db import add_user, view_users

new_user = input("Please enter your username: ")
user_email = input("Please enter your email: ")

add_user(new_user, user_email)
view_users()