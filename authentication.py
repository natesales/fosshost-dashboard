import bcrypt

passwd = b's$cret12'

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd, salt)

print(salt)
print(hashed)



def login(self, email, password):
    userdoc = self.users.find_one({"email": email})

    if userdoc:
        return bcrypt.checkpw(password.encode(), userdoc["hash"])
    else:
        return False
