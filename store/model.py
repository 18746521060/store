from exts import db

auth_dict = {
    1: "普通用户权限" ,
    100: "高级用户权限"
}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    auth = db.Column(db.Integer, default=1)

    def __repr__(self):
        return "User(id:%s,username:%s,password:%s,auth:%s)"%(self.id, self.username,self.password, auth_dict.get(self.auth))
